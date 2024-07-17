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
# # Purchase Revenues Lab
#
# Prepare dataset of events with purchase revenue.
#
# ##### Tasks
# 1. Extract purchase revenue for each event
# 2. Filter events where revenue is not null
# 3. Check what types of events have revenue
# 4. Drop unneeded column
#
# ##### Methods
# - DataFrame: **`select`**, **`drop`**, **`withColumn`**, **`filter`**, **`dropDuplicates`**
# - Column: **`isNotNull`**

# %run ../Includes/Classroom-Setup

events_df = spark.read.format("delta").load(DA.paths.events)
display(events_df)

#
#
# ### 1. Extract purchase revenue for each event
# Add new column **`revenue`** by extracting **`ecommerce.purchase_revenue_in_usd`**

from pyspark.sql.functions import col

# TODO
revenue_df = events_df.withColumn("revenue", col("ecommerce.purchase_revenue_in_usd"))
display(revenue_df)

#
#
#
#
# **1.1: CHECK YOUR WORK**

# +
from pyspark.sql.functions import col
expected1 = [5830.0, 5485.0, 5289.0, 5219.1, 5180.0, 5175.0, 5125.0, 5030.0, 4985.0, 4985.0]
result1 = [row.revenue for row in revenue_df.sort(col("revenue").desc_nulls_last()).limit(10).collect()]

assert(expected1 == result1)
print("All test pass")
# -

#
#
# ### 2. Filter events where revenue is not null
# Filter for records where **`revenue`** is not **`null`**

# TODO
purchases_df = revenue_df.filter(col("revenue").isNotNull())
display(purchases_df)

#
#
#
# **2.1: CHECK YOUR WORK**

assert purchases_df.filter(col("revenue").isNull()).count() == 0, "Nulls in 'revenue' column"
print("All test pass")

#
#
# ### 3. Check what types of events have revenue
# Find unique **`event_name`** values in **`purchases_df`** in one of two ways:
# - Select "event_name" and get distinct records
# - Drop duplicate records based on the "event_name" only
#
# <img src="https://files.training.databricks.com/images/icon_hint_32.png" alt="Hint"> There's only one event associated with revenues

# TODO
#distinct_df = purchases_df.select("event_name").distinct()
distinct_df = purchases_df.dropDuplicates(["event_name"]).select("event_name")
display(distinct_df)

#
#
# ### 4. Drop unneeded column
# Since there's only one event type, drop **`event_name`** from **`purchases_df`**.

# TODO
final_df = purchases_df.drop("event_name")
display(final_df)

#
#
#
# **4.1: CHECK YOUR WORK**

expected_columns = {"device", "ecommerce", "event_previous_timestamp", "event_timestamp",
                    "geo", "items", "revenue", "traffic_source",
                    "user_first_touch_timestamp", "user_id"}
assert(set(final_df.columns) == expected_columns)
print("All test pass")

#
#
#
# ### 5. Chain all the steps above excluding step 3

# +
# TODO
final_df = (events_df
  .drop("event_name")
  .withColumn("revenue", col("ecommerce.purchase_revenue_in_usd"))
  .filter(col("revenue").isNotNull())
)

display(final_df)
# -

#
#
#
# **5.1: CHECK YOUR WORK**

assert(final_df.count() == 180678)
print("All test pass")

expected_columns = {"device", "ecommerce", "event_previous_timestamp", "event_timestamp",
                    "geo", "items", "revenue", "traffic_source",
                    "user_first_touch_timestamp", "user_id"}
assert(set(final_df.columns) == expected_columns)
print("All test pass")

#
#
#
# ### Clean up classroom

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
