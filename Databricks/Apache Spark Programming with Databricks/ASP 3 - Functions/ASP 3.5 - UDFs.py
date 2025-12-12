# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.3
# ---

#
# <div style="text-align: center; line-height: 0; padding-top: 9px;">
#   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
# </div>

#
#
# # User-Defined Functions
#
# ##### Objectives
# 1. Define a function
# 1. Create and apply a UDF
# 1. Register the UDF to use in SQL
# 1. Create and register a UDF with Python decorator syntax
# 1. Create and apply a Pandas (vectorized) UDF
#
# ##### Methods
# - <a href="https://docs.databricks.com/spark/latest/spark-sql/udf-python.html" target="_blank">UDF Registration (**`spark.udf`**)</a>: **`register`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.udf.html?highlight=udf#pyspark.sql.functions.udf" target="_blank">Built-In Functions</a>: **`udf`**
# - <a href="https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.functions.udf.html" target="_blank">Python UDF Decorator</a>: **`@udf`**
# - <a href="https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.functions.pandas_udf.html" target="_blank">Pandas UDF Decorator</a>: **`@pandas_udf`**

# %run ../Includes/Classroom-Setup

#
#
# ### User-Defined Function (UDF)
# A custom column transformation function
#
# - Can’t be optimized by Catalyst Optimizer
# - Function is serialized and sent to executors
# - Row data is deserialized from Spark's native binary format to pass to the UDF, and the results are serialized back into Spark's native format
# - For Python UDFs, additional interprocess communication overhead between the executor and a Python interpreter running on each worker node

#
#
#
# For this demo, we're going to use the sales data.

sales_df = spark.read.format("delta").load(DA.paths.sales)
display(sales_df)


#
#
#
# ### Define a function
#
# Define a function (on the driver) to get the first letter of a string from the **`email`** field.

# +
def first_letter_function(email):
    return email[0]

first_letter_function("annagray@kaufman.com")
# -

#
#
# ### Create and apply UDF
# Register the function as a UDF. This serializes the function and sends it to executors to be able to transform DataFrame records.

first_letter_udf = udf(first_letter_function)

#
#
#
# Apply the UDF on the **`email`** column.

# +
from pyspark.sql.functions import col

# Python UDF:  Ran in 3.73 seconds
display(sales_df.select(first_letter_udf(col("email"))))
# -

#
#
#
# ### Register UDF to use in SQL
# Register the UDF using **`spark.udf.register`** to also make it available for use in the SQL namespace.

# +
sales_df.createOrReplaceTempView("sales") # Create a temporary view from a DataFrame to use in SQL queries

first_letter_udf = spark.udf.register("sql_udf", first_letter_function)

# +
# You can still apply the UDF from Python

# Python SQL UDF:  1.43 seconds
display(sales_df.select(first_letter_udf(col("email"))))

# +
# %sql
-- You can now also apply the UDF from SQL

-- SQL UDF:  Ran in 1.24 seconds
SELECT sql_udf(email) AS first_letter FROM sales


# -

#
#
# ### Use Decorator Syntax (Python Only)
#
# Alternatively, you can define and register a UDF using <a href="https://realpython.com/primer-on-python-decorators/" target="_blank">Python decorator syntax</a>. The **`@udf`** decorator parameter is the Column datatype the function returns.
#
# You will no longer be able to call the local Python function (i.e., **`first_letter_udf("annagray@kaufman.com")`** will not work).
#
# <img src="https://files.training.databricks.com/images/icon_note_32.png" alt="Note"> This example also uses <a href="https://docs.python.org/3/library/typing.html" target="_blank">Python type hints</a>, which were introduced in Python 3.5. Type hints are not required for this example, but instead serve as "documentation" to help developers use the function correctly. They are used in this example to emphasize that the UDF processes one record at a time, taking a single **`str`** argument and returning a **`str`** value.

# Our input/output is a string
@udf("string") # registers "first_letter_udf" with the Python interpreter
def first_letter_udf(email: str) -> str: 
    return email[0]


#
#
#
# And let's use our decorator UDF here.

# +
from pyspark.sql.functions import col

sales_df = spark.read.format("delta").load(DA.paths.sales)

# Should be around the same performance as the Vanilla Python UDF; Ran in 2.02 seconds compared to 3.73 seconds
display(sales_df.select(first_letter_udf(col("email"))))
# -

#
#
# ### Pandas/Vectorized UDFs
#
# Pandas UDFs are available in Python to improve the efficiency of UDFs. Pandas UDFs utilize Apache Arrow to speed up computation.
#
# * <a href="https://databricks.com/blog/2017/10/30/introducing-vectorized-udfs-for-pyspark.html" target="_blank">Blog post</a>
# * <a href="https://spark.apache.org/docs/latest/api/python/user_guide/sql/arrow_pandas.html?highlight=arrow" target="_blank">Documentation</a>
#
# <img src="https://databricks.com/wp-content/uploads/2017/10/image1-4.png" alt="Benchmark" width ="500" height="1500">
#
# The user-defined functions are executed using: 
# * <a href="https://arrow.apache.org/" target="_blank">Apache Arrow</a>, an in-memory columnar data format that is used in Spark to efficiently transfer data between JVM and Python processes with near-zero (de)serialization cost
# * Pandas inside the function, to work with Pandas instances and APIs
#
# <img src="https://files.training.databricks.com/images/icon_warn_32.png" alt="Warning"> As of Spark 3.0, you should **always** define your Pandas UDF using Python type hints.

# +
import pandas as pd
from pyspark.sql.functions import pandas_udf

# We have a string input/output
@pandas_udf("string")
def vectorized_udf(email: pd.Series) -> pd.Series:
    return email.str[0]

# Alternatively
# def vectorized_udf(email: pd.Series) -> pd.Series:
#     return email.str[0]
# vectorized_udf = pandas_udf(vectorized_udf, "string")


# -

# Should be faster than the Python UDF (Vanilla or Decorator) b/c it uses Apache Arrow; Ran in 1.72 seconds compared to 2.02 seconds
display(sales_df.select(vectorized_udf(col("email"))))

#
#
#
# We can also register these Pandas UDFs to the SQL namespace.

spark.udf.register("sql_vectorized_udf", vectorized_udf)

# +
# %sql
-- Use the Pandas UDF from SQL

-- Ran in 1.45 seconds
SELECT sql_vectorized_udf(email) AS firstLetter FROM sales
# -

#
#
# ### Clean up classroom

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
