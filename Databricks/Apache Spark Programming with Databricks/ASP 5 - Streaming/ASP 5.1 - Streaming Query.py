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
# # Streaming Query
#
# ##### Objectives
# 1. Build streaming DataFrames
# 1. Display streaming query results
# 1. Write streaming query results
# 1. Monitor streaming query
#
# ##### Classes
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/api/pyspark.sql.streaming.DataStreamReader.html" target="_blank">DataStreamReader</a>
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/api/pyspark.sql.streaming.DataStreamWriter.html" target="_blank">DataStreamWriter</a>
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/api/pyspark.sql.streaming.StreamingQuery.html" target="_blank">StreamingQuery</a>

# %run ../Includes/Classroom-Setup

#
#
# ### Build streaming DataFrames
#
# Obtain an initial streaming DataFrame from a Delta-format file source.

# +
# No action has been taken, so nothing will start yet
df = (spark
      .readStream
      .option("maxFilesPerTrigger", 1)
      .format("delta")
      .load(DA.paths.events)
     )

# Will return True for streaming DataFrames
df.isStreaming

# +
# Trigger action by running below
# display(df)
# -

#
#
# Apply some transformations, producing new streaming DataFrames.

# +
from pyspark.sql.functions import col, approx_count_distinct, count

email_traffic_df = (df
                    .filter(col("traffic_source") == "email")
                    .withColumn("mobile", col("device").isin(["iOS", "Android"]))
                    .select("user_id", "event_timestamp", "mobile")
                   )

email_traffic_df.isStreaming

# +
# Trigger action by running below
# display(email_traffic_df)
# -

#
#
# ### Write streaming query results
#
# Take the final streaming DataFrame (our result table) and write it to a file sink in "append" mode.

# +
checkpoint_path = f"{DA.paths.checkpoints}/email_traffic"
output_path = f"{DA.paths.working_dir}/email_traffic/output"

devices_query = (email_traffic_df
                 .writeStream
                 .outputMode("append") # default, kept for pedagogical purposes
                 .format("delta") # default, kept for pedagogical purposes
                 .queryName("email_traffic")
                 .trigger(processingTime="1 second")
                 .option("checkpointLocation", checkpoint_path) # Mandatory to ensure fault tolerance
                 .start(output_path)
                )
# -

#
#
# ### Monitor streaming query
#
# Use the streaming query "handle" to monitor and control it.

devices_query.id

devices_query.status

devices_query.lastProgress

# +
import time
# Run for 10 more seconds
time.sleep(10) 

devices_query.stop()
# -

devices_query.awaitTermination()

#
#
# ### Classroom Cleanup
# Run the cell below to clean up resources.

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
