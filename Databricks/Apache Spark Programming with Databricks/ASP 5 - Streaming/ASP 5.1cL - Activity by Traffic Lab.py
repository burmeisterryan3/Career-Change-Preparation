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
# # Activity by Traffic Lab
# Process streaming data to display total active users by traffic source.
#
# ##### Objectives
# 1. Read data stream
# 2. Get active users by traffic source
# 3. Execute query with display() and plot results
# 4. Execute the same streaming query with DataStreamWriter
# 5. View results being updated in the query table
# 6. List and stop all active streams
#
# ##### Classes
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/api/pyspark.sql.streaming.DataStreamReader.html" target="_blank">DataStreamReader</a>
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/api/pyspark.sql.streaming.DataStreamWriter.html" target="_blank">DataStreamWriter</a>
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/api/pyspark.sql.streaming.StreamingQuery.html" target="_blank">StreamingQuery</a>

#
#
# ### Setup
# Run the cells below to generate data and create the **`schema`** string needed for this lab.

# %run ../Includes/Classroom-Setup-5.1c

# +
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, ArrayType

events_schema_1 = StructType([
    StructField("device", StringType(), True),
    StructField("ecommerce", StructType([
        StructField("purchaseRevenue", DoubleType(), True),
        StructField("total_item_quantity", LongType(), True),
        StructField("unique_items", LongType(), True)
    ]), True),
    StructField("event_name", StringType(), True),
    StructField("event_previous_timestamp", LongType(), True),
    StructField("event_timestamp", LongType(), True),
    StructField("geo", StructType([
        StructField("city", StringType(), True),
        StructField("state", StringType(), True)
    ]), True),
    StructField("items", ArrayType(
        StructType([
            StructField("coupon", StringType(), True),
            StructField("item_id", StringType(), True),
            StructField("item_name", StringType(), True),
            StructField("item_revenue_in_usd", DoubleType(), True),
            StructField("price_in_usd", DoubleType(), True),
            StructField("quantity", LongType(), True)
        ])
    ), True),
    StructField("traffic_source", StringType(), True),
    StructField("user_first_touch_timestamp", LongType(), True),
    StructField("user_id", StringType(), True)
])
# -

events_schema_2 = "device STRING,ecommerce STRUCT<purchase_revenue_in_usd: DOUBLE, total_item_quantity: BIGINT, unique_items: BIGINT>,event_name STRING,event_previous_timestamp BIGINT,event_timestamp BIGINT,geo STRUCT<city: STRING, state: STRING>,items ARRAY<STRUCT<coupon: STRING, item_id: STRING, item_name: STRING, item_revenue_in_usd: DOUBLE, price_in_usd: DOUBLE, quantity: BIGINT>>,traffic_source STRING,user_first_touch_timestamp BIGINT,user_id STRING"

#
#
# ### 1. Read data stream
# - Set to process 1 file per trigger
# - Read from Delta with filepath stored in **`DA.paths.events`**
#
# Assign the resulting Query to **`df`**.

# TODO
df = (spark
      .readStream
      .format("delta")
      .option("maxFilesPerTrigger", 1)
      .load(DA.paths.events)
)

#
#
#
# **1.1: CHECK YOUR WORK**

DA.tests.validate_1_1(df)

#
#
# ### 2. Get active users by traffic source
# - Set default shuffle partitions to number of cores on your cluster (not required, but runs faster)
# - Group by **`traffic_source`**
#   - Aggregate the approximate count of distinct users and alias with "active_users"
# - Sort by **`traffic_source`**

# +
from pyspark.sql.functions import approx_count_distinct
spark.conf.set("spark.sql.shuffle.partitions", sc.defaultParallelism) # sc is an alias for spark.sparkContext

traffic_df = (df.groupBy("traffic_source")
                .agg(approx_count_distinct("user_id").alias("active_users"))
                .orderBy("traffic_source")
)
# -

#
#
#
# **2.1: CHECK YOUR WORK**

DA.tests.validate_2_1(traffic_df.schema)

#
#
# ### 3. Execute query with display() and plot results
# - Execute results for **`traffic_df`** using display()
# - Plot the streaming query results as a bar graph

display(traffic_df)

#
#
#
# **3.1: CHECK YOUR WORK**
# - You bar chart should plot **`traffic_source`** on the x-axis and **`active_users`** on the y-axis
# - The top three traffic sources in descending order should be **`google`**, **`facebook`**, and **`instagram`**.

#
#
# ### 4. Execute the same streaming query with DataStreamWriter
# - Name the query "active_users_by_traffic"
# - Set to "memory" format and "complete" output mode
# - Set a trigger interval of 1 second

# TODO
traffic_query = (traffic_df
                 .writeStream
                 .outputMode("complete")
                 .format("memory")
                 .queryName("active_users_by_traffic")
                 .trigger(processingTime="1 second")
                 .option("checkpointLocation", f"{DA.paths.checkpoints}/traffic_stream")
                 .start(f"{DA.paths.checkpoints}/traffic_stream/output")
)

#
#
#
# **4.1: CHECK YOUR WORK**

DA.tests.validate_4_1(traffic_query)

#
#
# ### 5. View results being updated in the query table
# Run a query in a SQL cell to display the results from the **`active_users_by_traffic`** table

# %sql
SELECT *
FROM active_users_by_traffic;

#
#
#
# **5.1: CHECK YOUR WORK**
# Your query should eventually result in the following values.
#
# |traffic_source|active_users|
# |---|---|
# |direct|438886|
# |email|281525|
# |facebook|956769|
# |google|1781961|
# |instagram|530050|
# |youtube|253321|

#
#
# ### 6. List and stop all active streams
# - Use SparkSession to get list of all active streams
# - Iterate over the list and stop each query

for s in spark.streams.active:
  s.stop()
  #if s.name == "active_users_by_traffic":
  #  print("Stopping stream")
  #  s.stop()

#
#
#
# **6.1: CHECK YOUR WORK**

DA.tests.validate_6_1(traffic_query)

#
#
# ### Classroom Cleanup
# Run the cell below to clean up resources.

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
