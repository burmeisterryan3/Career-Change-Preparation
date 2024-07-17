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
# # Revenue by Traffic Lab
# Get the 3 traffic sources generating the highest total revenue.
# 1. Aggregate revenue by traffic source
# 2. Get top 3 traffic sources by total revenue
# 3. Clean revenue columns to have two decimal places
#
# ##### Methods
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html" target="_blank">DataFrame</a>: **`groupBy`**, **`sort`**, **`limit`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/column.html" target="_blank">Column</a>: **`alias`**, **`desc`**, **`cast`**, **`operators`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html" target="_blank">Built-in Functions</a>: **`avg`**, **`sum`**

# %run ../Includes/Classroom-Setup

#
#
# ### Setup
# Run the cell below to create the starting DataFrame **`df`**.

# +
from pyspark.sql.functions import col

# Purchase events logged on the BedBricks website
df = (spark.read.format("delta").load(DA.paths.events)
      .withColumn("revenue", col("ecommerce.purchase_revenue_in_usd"))
      .filter(col("revenue").isNotNull())
      .drop("event_name")
     )

display(df)
# -

#
#
# ### 1. Aggregate revenue by traffic source
# - Group by **`traffic_source`**
# - Get sum of **`revenue`** as **`total_rev`**. 
# - Get average of **`revenue`** as **`avg_rev`**
#
# Remember to import any necessary built-in functions.

from pyspark.sql.functions import sum, avg

# +
# TODO

traffic_df = (df.groupBy("traffic_source")
                .agg(sum("revenue").alias("total_rev"),
                     avg("revenue").alias("avg_rev"))
)

display(traffic_df)
# -

#
#
#
# **1.1: CHECK YOUR WORK**

# +
from pyspark.sql.functions import round

expected1 = [(12704560.0, 1083.175), (78800000.3, 983.2915), (24797837.0, 1076.6221), (47218429.0, 1086.8303), (16177893.0, 1083.4378), (8044326.0, 1087.218)]
test_df = traffic_df.sort("traffic_source").select(round("total_rev", 4).alias("total_rev"), round("avg_rev", 4).alias("avg_rev"))
result1 = [(row.total_rev, row.avg_rev) for row in test_df.collect()]

assert(expected1 == result1)
print("All test pass")
# -

#
#
# ### 2. Get top three traffic sources by total revenue
# - Sort by **`total_rev`** in descending order
# - Limit to first three rows

# +
# TODO
top_traffic_df = (traffic_df.orderBy(col("total_rev").desc()).limit(3))

display(top_traffic_df)
# -

#
#
#
# **2.1: CHECK YOUR WORK**

# +
expected2 = [(78800000.3, 983.2915), (47218429.0, 1086.8303), (24797837.0, 1076.6221)]
test_df = top_traffic_df.select(round("total_rev", 4).alias("total_rev"), round("avg_rev", 4).alias("avg_rev"))
result2 = [(row.total_rev, row.avg_rev) for row in test_df.collect()]

assert(expected2 == result2)
print("All test pass")
# -

#
#
# ### 3. Limit revenue columns to two decimal places
# - Modify columns **`avg_rev`** and **`total_rev`** to contain numbers with two decimal places
#   - Use **`withColumn()`** with the same names to replace these columns
#   - To limit to two decimal places, multiply each column by 100, cast to long, and then divide by 100

# +
# TODO
final_df = (top_traffic_df.withColumn("avg_rev", (col("avg_rev")*100).cast("long")/100).withColumn("total_rev", (col("total_rev")*100).cast("long")/100))

display(final_df)
# -

#
#
#
# **3.1: CHECK YOUR WORK**

# +
expected3 = [(78800000.29, 983.29), (47218429.0, 1086.83), (24797837.0, 1076.62)]
result3 = [(row.total_rev, row.avg_rev) for row in final_df.collect()]

assert(expected3 == result3)
print("All test pass")
# -

#
#
# ### 4. Bonus: Rewrite using a built-in math function
# Find a built-in math function that rounds to a specified number of decimal places

# +
# NOTE: col() is not requried within round()
bonus_df = (top_traffic_df.withColumn("avg_rev", round("avg_rev", 2)).withColumn("total_rev", round(col("total_rev"), 2)))

display(bonus_df)
# -

#
#
#
# **4.1: CHECK YOUR WORK**

# +
expected4 = [(78800000.3, 983.29), (47218429.0, 1086.83), (24797837.0, 1076.62)]
result4 = [(row.total_rev, row.avg_rev) for row in bonus_df.collect()]

assert(expected4 == result4)
print("All test pass")
# -

#
#
# ### 5. Chain all the steps above

# +
# TODO
chain_df = (df.groupBy("traffic_source")
              .agg(sum("revenue").alias("total_rev"),
                   avg("revenue").alias("avg_rev"))
              .orderBy(col("total_rev").desc()).limit(3)
              .withColumn("avg_rev", round("avg_rev", 2))
              .withColumn("total_rev", round(col("total_rev"), 2))
)

display(chain_df)
# -

#
#
#
# **5.1: CHECK YOUR WORK**

# +
method_a = [(78800000.3,  983.29), (47218429.0, 1086.83), (24797837.0, 1076.62)]
method_b = [(78800000.29, 983.29), (47218429.0, 1086.83), (24797837.0, 1076.62)]
result5 = [(row.total_rev, row.avg_rev) for row in chain_df.collect()]

assert result5 == method_a or result5 == method_b
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
