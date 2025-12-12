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
# # Additional Functions
#
# ##### Objectives
# 1. Apply built-in functions to generate data for new columns
# 1. Apply DataFrame NA functions to handle null values
# 1. Join DataFrames
#
# ##### Methods
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.join.html#pyspark.sql.DataFrame.join" target="_blank">DataFrame Methods </a>: **`join`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameNaFunctions.html#pyspark.sql.DataFrameNaFunctions" target="_blank">DataFrameNaFunctions</a>: **`fill`**, **`drop`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html" target="_blank">Built-In Functions</a>:
#   - Aggregate: **`collect_set`**
#   - Collection: **`explode`**
#   - Non-aggregate and miscellaneous: **`col`**, **`lit`**

# %run ../Includes/Classroom-Setup

from pyspark.sql.functions import *

sales_df = spark.read.format("delta").load(DA.paths.sales)
display(sales_df)

#
#
# ### Non-aggregate and Miscellaneous Functions
# Here are a few additional non-aggregate and miscellaneous built-in functions.
#
# | Method | Description |
# | --- | --- |
# | col / column | Returns a Column based on the given column name. |
# | lit | Creates a Column of literal value |
# | isnull | Return true iff the column is null |
# | rand | Generate a random column with independent and identically distributed (i.i.d.) samples uniformly distributed in [0.0, 1.0) |

#
#
#
# We could select a particular column using the **`col`** function

# +
gmail_accounts = sales_df.filter(col("email").endswith("gmail.com"))

display(gmail_accounts)
# -

#
#
#
# **`lit`** can be used to create a column out of a value, which is useful for appending columns.

display(gmail_accounts.select("email", lit(True).alias("gmail user")))

#
#
# ### DataFrameNaFunctions
# <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameNaFunctions.html#pyspark.sql.DataFrameNaFunctions" target="_blank">DataFrameNaFunctions</a> is a DataFrame submodule with methods for handling null values. Obtain an instance of DataFrameNaFunctions by accessing the **`na`** attribute of a DataFrame.
#
# | Method | Description |
# | --- | --- |
# | drop | Returns a new DataFrame omitting rows with any, all, or a specified number of null values, considering an optional subset of columns |
# | fill | Replace null values with the specified value for an optional subset of columns |
# | replace | Returns a new DataFrame replacing a value with another value, considering an optional subset of columns |

#
#
# Here we'll see the row count before and after dropping rows with null/NA values.

print(sales_df.count())
print(sales_df.na.drop().count())

#
#
# Since the row counts are the same, we have the no null columns.  We'll need to explode items to find some nulls in columns such as items.coupon.

sales_exploded_df = sales_df.withColumn("items", explode(col("items")))
display(sales_exploded_df.select("items.coupon"))
print(sales_exploded_df.select("items.coupon").count())
print(sales_exploded_df.select("items.coupon").na.drop().count())

#
#
#
# We can fill in the missing coupon codes with **`na.fill`**

display(sales_exploded_df.select("items.coupon").na.fill("NO COUPON"))

#
#
# ### Joining DataFrames
# The DataFrame <a href="https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.DataFrame.join.html?highlight=join#pyspark.sql.DataFrame.join" target="_blank">**`join`**</a> method joins two DataFrames based on a given join expression. 
#
# Several different types of joins are supported:
#
# Inner join based on equal values of a shared column called "name" (i.e., an equi join)<br/>
# **`df1.join(df2, "name")`**
#
# Inner join based on equal values of the shared columns called "name" and "age"<br/>
# **`df1.join(df2, ["name", "age"])`**
#
# Full outer join based on equal values of a shared column called "name"<br/>
# **`df1.join(df2, "name", "outer")`**
#
# Left outer join based on an explicit column expression<br/>
# **`df1.join(df2, df1["customer_name"] == df2["account_name"], "left_outer")`**

#
#
# We'll load in our users data to join with our gmail_accounts from above.

users_df = spark.read.format("delta").load(DA.paths.users)
display(users_df)

joined_df = gmail_accounts.join(other=users_df, on='email', how = "inner")
display(joined_df)

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
