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
# # Ingesting Data Lab
#
# Read in CSV files containing products data.
#
# ##### Tasks
# 1. Read with infer schema
# 2. Read with user-defined schema
# 3. Read with schema as DDL formatted string
# 4. Write using Delta format

# %run ../Includes/Classroom-Setup

#
#
# ### 1. Read with infer schema
# - View the first CSV file using DBUtils method **`fs.head`** with the filepath provided in the variable **`single_product_cs_file_path`**
# - Create **`products_df`** by reading from CSV files located in the filepath provided in the variable **`products_csv_path`**
#   - Configure options to use first line as header and infer schema

# +
# TODO
single_product_csv_file_path = f"{DA.paths.datasets}/products/products.csv/part-00000-tid-1663954264736839188-daf30e86-5967-4173-b9ae-d1481d3506db-2367-1-c000.csv"
print(dbutils.fs.head(single_product_csv_file_path))

products_csv_path = f"{DA.paths.datasets}/products/products.csv"
products_df = spark.read.csv(products_csv_path, header=True, inferSchema=True)

products_df.printSchema()
# -

#
#
#
# **1.1: CHECK YOUR WORK**

assert(products_df.count() == 12)
print("All test pass")

#
#
# ### 2. Read with user-defined schema
# Define schema by creating a **`StructType`** with column names and data types

# +
# TODO
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

user_defined_schema = StructType([
  StructField("item_id", StringType(), True),
  StructField("name", StringType(), True),
  StructField("price", DoubleType(), True)
])

products_df2 = spark.read.csv(products_csv_path, header=True, schema=user_defined_schema)
# -

#
#
#
# **2.1: CHECK YOUR WORK**

assert(user_defined_schema.fieldNames() == ["item_id", "name", "price"])
print("All test pass")

# +
from pyspark.sql import Row

expected1 = Row(item_id="M_STAN_Q", name="Standard Queen Mattress", price=1045.0)
result1 = products_df2.first()

assert(expected1 == result1)
print("All test pass")
# -

#
#
# ### 3. Read with DDL formatted string

# +
# TODO
ddl_schema = "item_id STRING, name STRING, price DOUBLE"

products_df3 = spark.read.csv(products_csv_path, header=True, schema=ddl_schema)
# -

#
#
#
# **3.1: CHECK YOUR WORK**

assert(products_df3.count() == 12)
print("All test pass")

#
#
#
# ### 4. Write to Delta
# Write **`products_df`** to the filepath provided in the variable **`products_output_path`**

# TODO
products_output_path = f"{DA.paths.working_dir}/delta/products"
products_df.write.format("delta").mode("overwrite").save(products_output_path)

#
#
#
# **4.1: CHECK YOUR WORK**

display(dbutils.fs.ls(products_output_path))

# +
verify_files = dbutils.fs.ls(products_output_path)
verify_delta_format = False
verify_num_data_files = 0
for f in verify_files:
    if f.name == "_delta_log/":
        verify_delta_format = True
    elif f.name.endswith(".parquet"):
        verify_num_data_files += 1

assert verify_delta_format, "Data not written in Delta format"
assert verify_num_data_files > 0, "No data written"
del verify_files, verify_delta_format, verify_num_data_files
print("All test pass")
# -

#
#
# ### Clean up classroom

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
