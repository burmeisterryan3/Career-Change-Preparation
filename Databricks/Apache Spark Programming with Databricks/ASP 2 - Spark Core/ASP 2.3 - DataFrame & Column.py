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
# # DataFrame & Column
# ##### Objectives
# 1. Construct columns
# 1. Subset columns
# 1. Add or replace columns
# 1. Subset rows
# 1. Sort rows
#
# ##### Methods
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html" target="_blank">DataFrame</a>: **`select`**, **`selectExpr`**, **`drop`**, **`withColumn`**, **`withColumnRenamed`**, **`filter`**, **`distinct`**, **`limit`**, **`sort`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/column.html" target="_blank">Column</a>: **`alias`**, **`isin`**, **`cast`**, **`isNotNull`**, **`desc`**, operators

# %run ../Includes/Classroom-Setup

#
#
#
# Let's use the BedBricks events dataset.

events_df = spark.read.format("delta").load(DA.paths.events)
display(events_df)

#
#
#
# ## Column Expressions
#
# A <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/column.html" target="_blank">Column</a> is a logical construction that will be computed based on the data in a DataFrame using an expression
#
# Construct a new Column based on existing columns in a DataFrame

# +
from pyspark.sql.functions import col

print(events_df.device)
print(events_df["device"])
print(col("device"))
# -

#
#
# Scala supports an additional syntax for creating a new Column based on existing columns in a DataFrame

# %scala
$"device"

#
#
#
# ### Column Operators and Methods
# | Method | Description |
# | --- | --- |
# | \*, + , <, >= | Math and comparison operators |
# | ==, != | Equality and inequality tests (Scala operators are **`===`** and **`=!=`**) |
# | alias | Gives the column an alias |
# | cast, astype | Casts the column to a different data type |
# | isNull, isNotNull, isNan | Is null, is not null, is NaN |
# | asc, desc | Returns a sort expression based on ascending/descending order of the column |

#
#
#
# Create complex expressions with existing columns, operators, and methods.

col("ecommerce.purchase_revenue_in_usd") + col("ecommerce.total_item_quantity")
col("event_timestamp").desc()
(col("ecommerce.purchase_revenue_in_usd") * 100).cast("int")

#
#
# Here's an example of using these column expressions in the context of a DataFrame

# +
rev_df = (events_df
         .filter(col("ecommerce.purchase_revenue_in_usd").isNotNull())
         .withColumn("purchase_revenue", (col("ecommerce.purchase_revenue_in_usd") * 100).cast("int"))
         .withColumn("avg_purchase_revenue", col("ecommerce.purchase_revenue_in_usd") / col("ecommerce.total_item_quantity"))
         .sort(col("avg_purchase_revenue").desc())
        )

display(rev_df)
# -

#
#
# ## DataFrame Transformation Methods
# | Method | Description |
# | --- | --- |
# | **`select`** | Returns a new DataFrame by computing given expression for each element |
# | **`drop`** | Returns a new DataFrame with a column dropped |
# | **`withColumnRenamed`** | Returns a new DataFrame with a column renamed |
# | **`withColumn`** | Returns a new DataFrame by adding a column or replacing the existing column that has the same name |
# | **`filter`**, **`where`** | Filters rows using the given condition |
# | **`sort`**, **`orderBy`** | Returns a new DataFrame sorted by the given expressions |
# | **`dropDuplicates`**, **`distinct`** | Returns a new DataFrame with duplicate rows removed |
# | **`limit`** | Returns a new DataFrame by taking the first n rows |
# | **`groupBy`** | Groups the DataFrame using the specified columns, so we can run aggregation on them |

#
#
# ### Subset columns
# Use DataFrame transformations to subset columns

#
#
# #### **`select()`**
# Selects a list of columns or column based expressions

devices_df = events_df.select("user_id", "device")
display(devices_df)

# +
from pyspark.sql.functions import col

locations_df = events_df.select(
    "user_id", 
    col("geo.city").alias("city"), 
    col("geo.state").alias("state")
)
display(locations_df)
# -

#
#
# #### **`selectExpr()`**
# Selects a list of SQL expressions

apple_df = events_df.selectExpr("user_id", "device in ('macOS', 'iOS') as apple_user")
display(apple_df)

#
#
# #### **`drop()`**
# Returns a new DataFrame after dropping the given column, specified as a string or Column object
#
# Use strings to specify multiple columns

anonymous_df = events_df.drop("user_id", "geo", "device")
display(anonymous_df)

no_sales_df = events_df.drop(col("ecommerce"))
display(no_sales_df)


#
#
# ### Add or replace columns
# Use DataFrame transformations to add or replace columns

#
#
#
# #### **`withColumn()`**
# Returns a new DataFrame by adding a column or replacing an existing column that has the same name.

mobile_df = events_df.withColumn("mobile", col("device").isin("iOS", "Android"))
display(mobile_df)

purchase_quantity_df = events_df.withColumn("purchase_quantity", col("ecommerce.total_item_quantity").cast("int"))
purchase_quantity_df.printSchema()

#
#
#
# #### **`withColumnRenamed()`**
# Returns a new DataFrame with a column renamed.

location_df = events_df.withColumnRenamed("geo", "location")
display(location_df)

#
#
#
# ### Subset Rows
# Use DataFrame transformations to subset rows

#
#
#
# #### **`filter()`**
# Filters rows using the given SQL expression or column based condition.
#
# ##### Alias: **`where`**

purchases_df = events_df.filter("ecommerce.total_item_quantity > 0")
display(purchases_df)

revenue_df = events_df.filter(col("ecommerce.purchase_revenue_in_usd").isNotNull())
display(revenue_df)

android_df = events_df.filter((col("traffic_source") != "direct") & (col("device") == "Android"))
display(android_df)

#
#
# #### **`dropDuplicates()`**
# Returns a new DataFrame with duplicate rows removed, optionally considering only a subset of columns.
#
# ##### Alias: **`distinct`**

display(events_df.distinct())

distinct_users_df = events_df.dropDuplicates(["user_id"])
display(distinct_users_df)

#
#
# #### **`limit()`**
# Returns a new DataFrame by taking the first n rows.

limit_df = events_df.limit(100)
display(limit_df)

#
#
# ### Sort rows
# Use DataFrame transformations to sort rows

#
#
# #### **`sort()`**
# Returns a new DataFrame sorted by the given columns or expressions.
#
# ##### Alias: **`orderBy`**

increase_timestamps_df = events_df.sort("event_timestamp")
display(increase_timestamps_df)

decrease_timestamp_df = events_df.sort(col("event_timestamp").desc())
display(decrease_timestamp_df)

increase_sessions_df = events_df.orderBy(["user_first_touch_timestamp", "event_timestamp"])
display(increase_sessions_df)

decrease_sessions_df = events_df.sort(col("user_first_touch_timestamp").desc(), col("event_timestamp"))
display(decrease_sessions_df)

#
#
# ### Clean up classroom

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
