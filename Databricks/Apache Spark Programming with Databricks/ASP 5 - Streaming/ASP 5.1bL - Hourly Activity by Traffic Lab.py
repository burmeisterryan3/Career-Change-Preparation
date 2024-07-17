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
# ## Hourly Activity by Traffic Lab
# Process streaming data to display the total active users by traffic source with a 1 hour window.
# 1. Cast to timestamp and add watermark for 2 hours
# 2. Aggregate active users by traffic source for 1 hour windows
# 3. Execute query with **`display`** and plot results
# 5. Use query name to stop streaming query

#
#
# ### Setup
# Run the cells below to generate hourly JSON files of event data for July 3, 2020.

# %run ../Includes/Classroom-Setup-5.1b

# +
schema = "device STRING, ecommerce STRUCT<purchase_revenue_in_usd: DOUBLE, total_item_quantity: BIGINT, unique_items: BIGINT>, event_name STRING, event_previous_timestamp BIGINT, event_timestamp BIGINT, geo STRUCT<city: STRING, state: STRING>, items ARRAY<STRUCT<coupon: STRING, item_id: STRING, item_name: STRING, item_revenue_in_usd: DOUBLE, price_in_usd: DOUBLE, quantity: BIGINT>>, traffic_source STRING, user_first_touch_timestamp BIGINT, user_id STRING"

# Directory of hourly events logged from the BedBricks website on July 3, 2020
hourly_events_path = f"{DA.paths.datasets}/ecommerce/events/events-2020-07-03.json"

df = (spark.readStream
           .schema(schema)
           .option("maxFilesPerTrigger", 1)
           .json(hourly_events_path))
# -

#
#
# ### 1. Cast to timestamp and add watermark for 2 hours
# - Add a **`createdAt`** column by dividing **`event_timestamp`** by 1M and casting to timestamp
# - Set a watermark of 2 hours on the **`createdAt`** column
#
# Assign the resulting DataFrame to **`events_df`**.

from pyspark.sql.functions import col
events_df = (df.withColumn("createdAt", (col("event_timestamp") / 1e6).cast("timestamp"))
               .withWatermark("createdAt", "2 hours")
)

#
#
#
# **1.1: CHECK YOUR WORK**

DA.tests.validate_1_1(events_df.schema)

#
#
# ### 2. Aggregate active users by traffic source for 1 hour windows
#
# - Set the default shuffle partitions to the number of cores on your cluster
# - Group by **`traffic_source`** with 1-hour tumbling windows based on the **`createdAt`** column
# - Aggregate the approximate count of distinct users per **`user_id`** and alias the resulting column to **`active_users`**
# - Select **`traffic_source`**, **`active_users`**, and the **`hour`** extracted from **`window.start`** with an alias of **`hour`**
# - Sort by **`hour`** in ascending order
# Assign the resulting DataFrame to **`traffic_df`**.

# +
from pyspark.sql.functions import hour, approx_count_distinct, window

spark.conf.set("spark.sql.shuffle.partitions", spark.sparkContext.defaultParallelism)

traffic_df = (events_df.groupBy("traffic_source", window("createdAt", "1 hour"))
                        .agg(approx_count_distinct("user_id").alias("active_users"))
                        .select("traffic_source", "active_users", hour(col("window.start")).alias("hour"))
                        .orderBy(col("hour").asc())
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
# - Use **`display`** to start **`traffic_df`** as a streaming query and display the resulting memory sink
#   - Assign "hourly_traffic" as the name of the query by setting the **`streamName`** parameter of **`display`**
# - Plot the streaming query results as a bar graph
# - Configure the following plot options:
#   - Keys: **`hour`**
#   - Series groupings: **`traffic_source`**
#   - Values: **`active_users`**

display(traffic_df, streamName="hourly_traffic")

#
#
#
# **3.1: CHECK YOUR WORK**
#
# - The bar chart should plot **`hour`** on the x-axis and **`active_users`** on the y-axis
# - Six bars should appear at every hour for all traffic sources
# - The chart should stop at hour 23

#
#
# ### 4. Manage streaming query
# - Iterate over SparkSession's list of active streams to find one with name "hourly_traffic"
# - Stop the streaming query

# +
# TODO
DA.block_until_stream_is_ready("hourly_traffic")

for s in spark.streams.active:
  if s.name == "hourly_traffic":
    print("Stopping stream")
    s.stop()
# -

#
#
#
# **4.1: CHECK YOUR WORK**
# Print all active streams to check that "hourly_traffic" is no longer there

DA.tests.validate_4_1()

#
#
# ### Classroom Cleanup
# Run the cell below to clean up resources.

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
