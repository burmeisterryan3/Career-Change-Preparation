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
# # Delta Lake
#
# ##### Objectives
# 1. Create a Delta Table
# 1. Understand the transaction Log
# 1. Read data from your Delta Table
# 1. Update data in your Delta Table
# 1. Access previous versions of table using time travel
# 1. Vacuum
#
# ##### Documentation
# - <a href="https://docs.delta.io/latest/quick-start.html#create-a-table" target="_blank">Delta Table</a> 
# - <a href="https://databricks.com/blog/2019/08/21/diving-into-delta-lake-unpacking-the-transaction-log.html" target="_blank">Transaction Log</a> 
# - <a href="https://databricks.com/blog/2019/02/04/introducing-delta-time-travel-for-large-scale-data-lakes.html" target="_blank">Time Travel</a>

# %run ../Includes/Classroom-Setup

#
#
# ### Create a Delta Table
# Let's first read the Parquet-format BedBricks events dataset.

dbutils.fs.ls(f"{DA.paths.datasets}/ecommerce/events")

events_df = spark.read.format("parquet").load(f"{DA.paths.datasets}/ecommerce/events/events.parquet")
display(events_df)

#
#
# Write the data in Delta format to the directory given by **`delta_path`**.

delta_path = f"{DA.paths.working_dir}/delta-events"
events_df.write.format("delta").mode("overwrite").save(delta_path)

#
#
# Write the data in Delta format as a managed table in the metastore.

events_df.write.format("delta").mode("overwrite").saveAsTable("delta_events")

#
#
#
# As with other file formats, Delta supports partitioning your data in storage using the unique values in a specified column (often referred to as "Hive partitioning").
#
# Let's **overwrite** the Delta dataset in the **`delta_path`** directory to partition by state. This can accelerate queries that filter by state.

# +
from pyspark.sql.functions import col

state_events_df = events_df.withColumn("state", col("geo.state"))

state_events_df.write.format("delta").mode("overwrite").partitionBy("state").option("overwriteSchema", "true").save(delta_path)
# -

#
#
# ### Understand the Transaction Log
# We can see how Delta stores the different state partitions in separate directories.
#
# Additionally, we can also see a directory called **`_delta_log`**, which is the transaction log.
#
# When a Delta Lake dataset is created, its transaction log is automatically created in the **`_delta_log`** subdirectory.

display(dbutils.fs.ls(delta_path))

#
#
#
# When changes are made to that table, these changes are recorded as ordered, atomic commits in the transaction log.
#
# Each commit is written out as a JSON file, starting with 00000000000000000000.json.
#
# Additional changes to the table generate subsequent JSON files in ascending numerical order.
#
# <div style="img align: center; line-height: 0; padding-top: 9px;">
#   <img src="https://user-images.githubusercontent.com/20408077/87174138-609fe600-c29c-11ea-90cc-84df0c1357f1.png" width="500"/>
# </div>

display(dbutils.fs.ls(f"{delta_path}/_delta_log/"))

#
#
#
# Next, let's take a look at a transaction log File.
#
#
# The <a href="https://docs.databricks.com/delta/delta-utility.html" target="_blank">four columns</a> each represent a different part of the very first commit to the Delta Table, creating the table.
# - The **`add`** column has statistics about the DataFrame as a whole and individual columns.
# - The **`commitInfo`** column has useful information about what the operation was (WRITE or READ) and who executed the operation.
# - The **`metaData`** column contains information about the column schema.
# - The **`protocol`** version contains information about the minimum Delta version necessary to either write or read to this Delta Table.

display(spark.read.json(f"{delta_path}/_delta_log/00000000000000000000.json"))

#
#
#
# One key difference between these two transaction logs is the size of the JSON file, this file has 206 rows compared to the previous 7.
#
# To understand why, let's take a look at the **`commitInfo`** column. We can see that in the **`operationParameters`** section, **`partitionBy`** has been filled in by the **`state`** column. Furthermore, if we look at the add section on row 3, we can see that a new section called **`partitionValues`** has appeared. As we saw above, Delta stores partitions separately in memory, however, it stores information about these partitions in the same transaction log file.

display(spark.read.json(f"{delta_path}/_delta_log/00000000000000000001.json"))

#
#
#
# Finally, let's take a look at the files inside one of the state partitions. The files inside corresponds to the partition commit (file 01) in the _delta_log directory.

display(dbutils.fs.ls(f"{delta_path}/state=CA/"))

#
#
#
# ### Read from your Delta table

df = spark.read.format("delta").load(delta_path)
display(df)

#
#
#
# ### Update your Delta Table
#
# Let's filter for rows where the event takes place on a mobile device.

df_update = state_events_df.filter(col("device").isin(["Android", "iOS"]))
display(df_update)

df_update.write.format("delta").mode("overwrite").save(delta_path)

df = spark.read.format("delta").load(delta_path)
display(df)

#
#
#
# Let's look at the files in the California partition post-update. Remember, the different files in this directory are snapshots of your DataFrame corresponding to different commits.

display(dbutils.fs.ls(f"{delta_path}/state=CA/"))

#
#
# ### Access previous versions of table using Time  Travel

#
#
#
# Oops, it turns out we actually we need the entire dataset! You can access a previous version of your Delta Table using Time Travel. Use the following two cells to access your version history. Delta Lake will keep a 30 day version history by default, but if necessary, Delta can store a version history for longer.

spark.sql("DROP TABLE IF EXISTS train_delta")
spark.sql(f"CREATE TABLE train_delta USING DELTA LOCATION '{delta_path}'")

# %sql
DESCRIBE HISTORY train_delta

#
#
#
# Using the **`versionAsOf`** option allows you to easily access previous versions of our Delta Table.

df = spark.read.format("delta").option("versionAsOf", 0).load(delta_path)
display(df)

#
#
#
# You can also access older versions using a timestamp.
#
# Replace the timestamp string with the information from your version history. 
#
# <img src="https://files.training.databricks.com/images/icon_note_32.png"> Note: You can use a date without the time information if necessary.

# +
# TODO

time_stamp_string = "2024-06-23T04:24:09.000+00:00"
df = spark.read.format("delta").option("timestampAsOf", time_stamp_string).load(delta_path)
display(df)
# -

#
#
# ### Vacuum 
#
# Now that we're happy with our Delta Table, we can clean up our directory using **`VACUUM`**. Vacuum accepts a retention period in hours as an input.

#
#
#
# It looks like our code doesn't run! By default, to prevent accidentally vacuuming recent commits, Delta Lake will not let users vacuum a period under 7 days or 168 hours. Once vacuumed, you cannot return to a prior commit through time travel, only your most recent Delta Table will be saved.

# +
# from delta.tables import *

# delta_table = DeltaTable.forPath(spark, delta_path)
# delta_table.vacuum(0)
# -

#
#
#
# We can workaround this by setting a spark configuration that will bypass the default retention period check.

# +
from delta.tables import *

spark.conf.set("spark.databricks.delta.retentionDurationCheck.enabled", "false")
delta_table = DeltaTable.forPath(spark, delta_path)
delta_table.vacuum(0)
# -

#
#
#
# Let's take a look at our Delta Table files now. After vacuuming, the directory only holds the partition of our most recent Delta Table commit.

display(dbutils.fs.ls(delta_path + "/state=CA/"))

#
#
#
# Since vacuuming deletes files referenced by the Delta Table, we can no longer access past versions. 
#
# The code below should throw an error.
#
# Uncomment it and give it a try.

df = spark.read.format("delta").option("versionAsOf", 0).load(delta_path)
display(df)

#
#
#
# ### Clean up classroom

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
