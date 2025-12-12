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
# # Sort Day Lab
#
# ##### Tasks
# 1. Define a UDF to label the day of week
# 1. Apply the UDF to label and sort by day of week
# 1. Plot active users by day of week as a bar graph

# %run ../Includes/Classroom-Setup

#
#
#
# Start with a DataFrame of the average number of active users by day of week.
#
# This was the resulting **`df`** in a previous lab.

# +
from pyspark.sql.functions import approx_count_distinct, avg, col, date_format, to_date

df = (spark
      .read
      .format("delta")
      .load(DA.paths.events)
      .withColumn("ts", (col("event_timestamp") / 1e6).cast("timestamp"))
      .withColumn("date", to_date("ts"))
      .groupBy("date").agg(approx_count_distinct("user_id").alias("active_users"))
      .withColumn("day", date_format(col("date"), "E"))
      .groupBy("day").agg(avg(col("active_users")).alias("avg_users"))
     )

display(df)


# -

#
#
# ### 1. Define UDF to label day of week
#
# Use the **`label_day_of_week`** function provided below to create the UDF **`label_dow_udf`**

def label_day_of_week(day: str) -> str:
    dow = {"Mon": "1", "Tue": "2", "Wed": "3", "Thu": "4",
           "Fri": "5", "Sat": "6", "Sun": "7"}
    return dow.get(day) + "-" + day


# TODO
label_dow_udf = udf(label_day_of_week)

#
#
# ### 2. Apply UDF to label and sort by day of week
# - Update the **`day`** column by applying the UDF and replacing this column
# - Sort by **`day`**
# - Plot as a bar graph

# +
# TODO
final_df = (df.withColumn("day_of_week", label_dow_udf(df["day"]))
              .orderBy("day_of_week")
)

display(final_df)
# -

#
#
# ### Clean up classroom

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
