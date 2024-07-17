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
# # Complex Types
#
# Explore built-in functions for working with collections and strings.
#
# ##### Objectives
# 1. Apply collection functions to process arrays
# 1. Union DataFrames together
#
# ##### Methods
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html" target="_blank">DataFrame</a>:**`union`**, **`unionByName`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html" target="_blank">Built-In Functions</a>:
#   - Aggregate: **`collect_set`**
#   - Collection: **`array_contains`**, **`element_at`**, **`explode`**
#   - String: **`split`**

# %run ../Includes/Classroom-Setup

from pyspark.sql.functions import *

# +
df = spark.read.format("delta").load(DA.paths.sales)

display(df)
# -

# You will need this DataFrame for a later exercise
details_df = (df
              .withColumn("items", explode("items")) # Make each struct within the array itself a row
              .select("email", "items.item_name")
              .withColumn("details", split(col("item_name"), " "))
             )
display(details_df)

#
#
# ### String Functions
# Here are some of the built-in functions available for manipulating strings.
#
# | Method | Description |
# | --- | --- |
# | translate | Translate any character in the src by a character in replaceString |
# | regexp_replace | Replace all substrings of the specified string value that match regexp with rep |
# | regexp_extract | Extract a specific group matched by a Java regex, from the specified string column |
# | ltrim | Removes the leading space characters from the specified string column |
# | lower | Converts a string column to lowercase |
# | split | Splits str around matches of the given pattern |

#
#
# For example: let's imagine that we need to parse our **`email`** column. We're going to use the **`split`** function  to split domain and handle.

from pyspark.sql.functions import split

display(df.select(split(df.email, '@', 0).alias('email_handle')))

#
#
# ### Collection Functions
#
# Here are some of the built-in functions available for working with arrays.
#
# | Method | Description |
# | --- | --- |
# | array_contains | Returns null if the array is null, true if the array contains value, and false otherwise. |
# | element_at | Returns element of array at given index. Array elements are numbered starting with **1**. |
# | explode | Creates a new row for each element in the given array or map column. |
# | collect_set | Returns a set of objects with duplicate elements eliminated. |

mattress_df = (details_df
               .filter(array_contains(col("details"), "Mattress"))
               .withColumn("size", element_at(col("details"), 2)))
display(mattress_df)

#
#
# ### Aggregate Functions
#
# Here are some of the built-in aggregate functions available for creating arrays, typically from GroupedData.
#
# | Method | Description |
# | --- | --- |
# | collect_list | Returns an array consisting of all values within the group. |
# | collect_set | Returns an array consisting of all unique values within the group. |

#
#
#
# Let's say that we wanted to see the sizes of mattresses ordered by each email address. For this, we can use the **`collect_set`** function

# +
size_df = mattress_df.groupBy("email").agg(collect_set("size").alias("size options"))

display(size_df)
# -

# ## Union and unionByName
#
# <img src="https://files.training.databricks.com/images/icon_warn_32.png" alt="Warning"> The DataFrame <a href="https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.DataFrame.union.html" target="_blank">**`union`**</a> method resolves columns by position, as in standard SQL. You should use it only if the two DataFrames have exactly the same schema, including the column order. In contrast, the DataFrame <a href="https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.DataFrame.unionByName.html" target="_blank">**`unionByName`**</a> method resolves columns by name.  This is equivalent to UNION ALL in SQL.  Neither one will remove duplicates.  
#
# Below is a check to see if the two dataframes have a matching schema where **`union`** would be appropriate

mattress_df.schema==size_df.schema

#
#
#
# If we do get the two schemas to match with a simple **`select`** statement, then we can use a **`union`**

# +
union_count = mattress_df.select("email").union(size_df.select("email")).count()

mattress_count = mattress_df.count()
size_count = size_df.count()

mattress_count + size_count == union_count
# -

#
#
# ### Clean up classroom
#
# And lastly, we'll clean up the classroom.

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
