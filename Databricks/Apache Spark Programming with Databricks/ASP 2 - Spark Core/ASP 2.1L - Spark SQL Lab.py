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
# # Spark SQL Lab
#
# ##### Tasks
# 1. Create a DataFrame from the **`events`** table
# 1. Display the DataFrame and inspect its schema
# 1. Apply transformations to filter and sort **`macOS`** events
# 1. Count results and take the first 5 rows
# 1. Create the same DataFrame using a SQL query
#
# ##### Methods
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/spark_session.html" target="_blank">SparkSession</a>: **`sql`**, **`table`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html" target="_blank">DataFrame</a> transformations: **`select`**, **`where`**, **`orderBy`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.sql.DataFrame.html" target="_blank">DataFrame</a> actions: **`select`**, **`count`**, **`take`**
# - Other <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html" target="_blank">DataFrame</a> methods: **`printSchema`**, **`schema`**, **`createOrReplaceTempView`**

# %run ../Includes/Classroom-Setup-SQL

#
#
# ### 1. Create a DataFrame from the **`events`** table
# - Use SparkSession to create a DataFrame from the **`events`** table

events_df = spark.table('events')

#
#
# ### 2. Display DataFrame and inspect schema
# - Use methods above to inspect DataFrame contents and schema

display(events_df.limit(10))

events_df.printSchema()

#
#
# ### 3. Apply transformations to filter and sort **`macOS`** events
# - Filter for rows where **`device`** is **`macOS`**
# - Sort rows by **`event_timestamp`**
#
# <img src="https://files.training.databricks.com/images/icon_hint_32.png" alt="Hint"> Use single and double quotes in your filter SQL expression

# TODO
mac_df = (events_df
          .where("device = 'macOS'")
          .orderBy("event_timestamp")
         )

#
#
# ### 4. Count results and take first 5 rows
# - Use DataFrame actions to count and take rows

# TODO
num_rows = mac_df.count()
rows = mac_df.take(5)

#
#
#
# **4.1: CHECK YOUR WORK**

# +
from pyspark.sql import Row

assert(num_rows == 1938215)
assert(len(rows) == 5)
assert(type(rows[0]) == Row)
print("All test pass")
# -

#
#
#
# ### 5. Create the same DataFrame using SQL query
# - Use SparkSession to run a SQL query on the **`events`** table
# - Use SQL commands to write the same filter and sort query used earlier

# +
# TODO
mac_sql_df = spark.sql("""
                       SELECT *
                       FROM events
                       WHERE device = 'macOS'
                       ORDER BY event_timestamp;
                       """)

display(mac_sql_df)
# -

#
#
#
# # MAGIC **5.1: CHECK YOUR WORK**
# - You should only see **`macOS`** values in the **`device`** column
# - The fifth row should be an event with timestamp **`1592539226602157`**

mac_sql_df.take(5)

verify_rows = mac_sql_df.take(5)
assert (mac_sql_df.select("device").distinct().count() == 1 and len(verify_rows) == 5 and verify_rows[0]['device'] == "macOS"), "Incorrect filter condition"
assert (verify_rows[4]['event_timestamp'] == 1592539226602157), "Incorrect sorting"
del verify_rows
print("All test pass")

#
#
# ### Classroom Cleanup

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
