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
# # Aggregation
#
# ##### Objectives
# 1. Group data by specified columns
# 1. Apply grouped data methods to aggregate data
# 1. Apply built-in functions to aggregate data
#
# ##### Methods
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html" target="_blank">DataFrame</a>: **`groupBy`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/grouping.html" target="_blank" target="_blank">Grouped Data</a>: **`agg`**, **`avg`**, **`count`**, **`max`**, **`sum`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html" target="_blank">Built-In Functions</a>: **`approx_count_distinct`**, **`avg`**, **`sum`**

# %run ../Includes/Classroom-Setup

#
#
#
# Let's use the BedBricks events dataset.

df = spark.read.format("delta").load(DA.paths.events)
display(df)

#
#
#
# ### Grouping data
#
# <img src="https://files.training.databricks.com/images/aspwd/aggregation_groupby.png" width="60%" />

#
#
#
# ### groupBy
# Use the DataFrame **`groupBy`** method to create a grouped data object. 
#
# This grouped data object is called **`RelationalGroupedDataset`** in Scala and **`GroupedData`** in Python.

df.groupBy("event_name")

df.groupBy("geo.state", "geo.city")

#
#
#
# ### Grouped data methods
# Various aggregation methods are available on the <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/grouping.html" target="_blank">GroupedData</a> object.
#
#
# | Method | Description |
# | --- | --- |
# | agg | Compute aggregates by specifying a series of aggregate columns |
# | avg | Compute the mean value for each numeric columns for each group |
# | count | Count the number of rows for each group |
# | max | Compute the max value for each numeric columns for each group |
# | mean | Compute the average value for each numeric columns for each group |
# | min | Compute the min value for each numeric column for each group |
# | pivot | Pivots a column of the current DataFrame and performs the specified aggregation |
# | sum | Compute the sum for each numeric columns for each group |

event_counts_df = df.groupBy("event_name").count()
display(event_counts_df)

#
#
#
# Here, we're getting the average purchase revenue for each.

avg_state_purchases_df = df.groupBy("geo.state").avg("ecommerce.purchase_revenue_in_usd")
display(avg_state_purchases_df)

#
#
# And here the total quantity and sum of the purchase revenue for each combination of state and city.

city_purchase_quantities_df = df.groupBy("geo.state", "geo.city").sum("ecommerce.total_item_quantity", "ecommerce.purchase_revenue_in_usd")
display(city_purchase_quantities_df)

#
#
# ## Built-In Functions
# In addition to DataFrame and Column transformation methods, there are a ton of helpful functions in Spark's built-in <a href="https://docs.databricks.com/spark/latest/spark-sql/language-manual/sql-ref-functions-builtin.html" target="_blank">SQL functions</a> module.
#
# In Scala, this is <a href="https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/functions$.html" target="_blank">**`org.apache.spark.sql.functions`**</a>, and <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql.html#functions" target="_blank">**`pyspark.sql.functions`**</a> in Python. Functions from this module must be imported into your code.

#
#
# ### Aggregate Functions
#
# Here are some of the built-in functions available for aggregation.
#
# | Method | Description |
# | --- | --- |
# | approx_count_distinct | Returns the approximate number of distinct items in a group |
# | avg | Returns the average of the values in a group |
# | collect_list | Returns a list of objects with duplicates |
# | corr | Returns the Pearson Correlation Coefficient for two columns |
# | max | Compute the max value for each numeric columns for each group |
# | mean | Compute the average value for each numeric columns for each group |
# | stddev_samp | Returns the sample standard deviation of the expression in a group |
# | sumDistinct | Returns the sum of distinct values in the expression |
# | var_pop | Returns the population variance of the values in a group |
#
# Use the grouped data method <a href="https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.GroupedData.agg.html#pyspark.sql.GroupedData.agg" target="_blank">**`agg`**</a> to apply built-in aggregate functions
#
# This allows you to apply other transformations on the resulting columns, such as <a href="https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.Column.alias.html" target="_blank">**`alias`**</a>.

# +
from pyspark.sql.functions import sum

# agg() function is required due to aliasing desired
state_purchases_df = df.groupBy("geo.state").agg(sum("ecommerce.total_item_quantity").alias("total_purchases"))
display(state_purchases_df)
# -

#
#
#
# Apply multiple aggregate functions on grouped data

# +
from pyspark.sql.functions import avg, approx_count_distinct

# agg() also used if multiple different functions are used
state_aggregates_df = (df
                       .groupBy("geo.state")
                       .agg(avg("ecommerce.total_item_quantity").alias("avg_quantity"),
                            approx_count_distinct("user_id").alias("distinct_users"))
                      )

display(state_aggregates_df)
# -

#
#
# ### Math Functions
# Here are some of the built-in functions for math operations.
#
# | Method | Description |
# | --- | --- |
# | ceil | Computes the ceiling of the given column. |
# | cos | Computes the cosine of the given value. |
# | log | Computes the natural logarithm of the given value. |
# | round | Returns the value of the column e rounded to 0 decimal places with HALF_UP round mode. |
# | sqrt | Computes the square root of the specified float value. |

# +
from pyspark.sql.functions import cos, sqrt

display(spark.range(10)  # Create a DataFrame with a single column called "id" with a range of integer values
        .withColumn("sqrt", sqrt("id"))
        .withColumn("cos", cos("id"))
       )
# -

#
#
# ### Clean up classroom

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
