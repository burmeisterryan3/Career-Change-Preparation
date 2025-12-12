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
#
# # Delta Lake Lab
# ##### Tasks
# 1. Write sales data to Delta
# 1. Modify sales data to show item count instead of item array
# 1. Rewrite sales data to same Delta path
# 1. Create table and view version history
# 1. Time travel to read previous version

# %run ../Includes/Classroom-Setup

sales_df = spark.read.parquet(f"{DA.paths.datasets}/ecommerce/sales/sales.parquet")
delta_sales_path = f"{DA.paths.working_dir}/delta-sales"

#
#
#
# ### 1. Write sales data to Delta
# Write **`sales_df`** to **`delta_sales_path`**

sales_df.write.format("delta").mode("overwrite").save(delta_sales_path)

#
#
#
# **1.1: CHECK YOUR WORK**

assert len(dbutils.fs.ls(delta_sales_path)) > 0

#
#
# ### 2. Modify sales data to show item count instead of item array
# Replace values in the **`items`** column with an integer value of the items array size.
# Assign the resulting DataFrame to **`updated_sales_df`**.

# +
from pyspark.sql.functions import size

updated_sales_df = sales_df.withColumn("items", size("items"))
display(updated_sales_df)
# -

#
#
#
# **2.1: CHECK YOUR WORK**

# +
from pyspark.sql.types import IntegerType

assert updated_sales_df.schema[6].dataType == IntegerType()
print("All test pass")
# -

#
#
# ### 3. Rewrite sales data to same Delta path
# Write **`updated_sales_df`** to the same Delta location **`delta_sales_path`**.
#
# <img src="https://files.training.databricks.com/images/icon_hint_32.png" alt="Hint"> This will fail without an option to overwrite the schema.

updated_sales_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").save(delta_sales_path)

#
#
#
# **3.1: CHECK YOUR WORK**

assert spark.read.format("delta").load(delta_sales_path).schema[6].dataType == IntegerType()
print("All test pass")

#
#
# ### 4. Create table and view version history
# Run SQL queries by writing SQL inside of `spark.sql()` to perform the following steps.
# - Drop table **`sales_delta`** if it exists
# - Create **`sales_delta`** table using the **`delta_sales_path`** location
# - List version history for the **`sales_delta`** table
#
# An example of a SQL query inside of `spark.sql()` would be something like ```spark.sql("SELECT * FROM sales_data")```

spark.sql("DROP TABLE IF EXISTS sales_delta")
spark.sql(f"CREATE TABLE sales_delta USING DELTA LOCATION '{delta_sales_path}'")

# %sql
DESCRIBE HISTORY sales_delta

#
#
#
# **4.1: CHECK YOUR WORK**

sales_delta_df = spark.sql("SELECT * FROM sales_delta")
assert sales_delta_df.count() == 210370
assert sales_delta_df.schema[6].dataType == IntegerType()
print("All test pass")

#
#
# ### 5. Time travel to read previous version
# Read delta table at **`delta_sales_path`** at version 0.
# Assign the resulting DataFrame to **`old_sales_df`**.

old_sales_df = spark.read.format("delta").option("versionAsOf", 0).load(delta_sales_path)
display(old_sales_df)

# %sql
-- Shorthand version if reading from a SQL table
SELECT * FROM sales_delta@v0;

#
#
#
# **5.1: CHECK YOUR WORK**

# +
from pyspark.sql.functions import col

assert old_sales_df.select(size(col("items"))).first()[0] == 1
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
