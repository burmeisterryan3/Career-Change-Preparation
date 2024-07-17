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
# # Partitioning
# ##### Objectives
# 1. Get partitions and cores
# 1. Repartition DataFrames
# 1. Configure default shuffle partitions
#
# ##### Methods
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html" target="_blank">DataFrame</a>: **`repartition`**, **`coalesce`**, **`rdd.getNumPartitions`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.SparkConf.html" target="_blank">SparkConf</a>: **`get`**, **`set`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.html" target="_blank">SparkSession</a>: **`spark.sparkContext.defaultParallelism`**
#
# ##### SparkConf Parameters
# - **`spark.sql.shuffle.partitions`**, **`spark.sql.adaptive.enabled`**

# %run ../Includes/Classroom-Setup

#
#
# ### Get partitions and cores
#
# Use the **`rdd`** method **`getNumPartitions`** to get the number of DataFrame partitions.

df = spark.read.format("delta").load(DA.paths.events)
df.rdd.getNumPartitions()

#
#
#
# Access **`SparkContext`** through **`SparkSession`** to get the number of cores or slots.
#
# Use the **`defaultParallelism`** attribute to get the number of cores in a cluster.

print(spark.sparkContext.defaultParallelism)

#
#
#
# **`SparkContext`** is also provided in Databricks notebooks as the variable **`sc`**.

print(sc.defaultParallelism)

#
#
# ### Repartition DataFrame
#
# There are two methods available to repartition a DataFrame: **`repartition`** and **`coalesce`**.

#
#
# #### **`repartition`**
# Returns a new DataFrame that has exactly **`n`** partitions.
#
# - Wide transformation
# - Pro: Evenly balances partition sizes  
# - Con: Requires shuffling all data

# Lazy Evaluation... no jobs spawned until action is taken in next cell
repartitioned_df = df.repartition(8)

repartitioned_df.rdd.getNumPartitions()

#
#
# #### **`coalesce`**
# Returns a new DataFrame that has exactly **`n`** partitions, when fewer partitions are requested.
#
# If a larger number of partitions is requested, it will stay at the current number of partitions.
#
# - Narrow transformation, some partitions are effectively concatenated
# - Pro: Requires no shuffling
# - Cons:
#   - Is not able to increase # partitions
#   - Can result in uneven partition sizes

coalesce_df = df.coalesce(8)

# Remains at 4 partitions because that is what was initially set & coalesce can not increase the # of partitions
coalesce_df.rdd.getNumPartitions()

coalesce_df = df.coalesce(2)
coalesce_df.rdd.getNumPartitions()

#
#
# ### Configure default shuffle partitions
#
# Use the SparkSession's **`conf`** attribute to get and set dynamic Spark configuration properties. The **`spark.sql.shuffle.partitions`** property determines the number of partitions that result from a shuffle. Let's check its default value:

spark.conf.get("spark.sql.shuffle.partitions")

#
#
#
# Assuming that the data set isn't too large, you could configure the default number of shuffle partitions to match the number of cores:

# defaultParallelism is the number of cores on your cluster
spark.conf.set("spark.sql.shuffle.partitions", spark.sparkContext.defaultParallelism)
print(spark.conf.get("spark.sql.shuffle.partitions"))

#
#
# ### Partitioning Guidelines
# - Make the number of partitions a multiple of the number of cores
# - Target a partition size of ~200MB
# - Size default shuffle partitions by dividing largest shuffle stage input by the target partition size (e.g., 4TB / 200MB = 20,000 shuffle partition count)
#
# <img src="https://files.training.databricks.com/images/icon_note_32.png" alt="Note"> When writing a DataFrame to storage, the number of DataFrame partitions determines the number of data files written. (This assumes that <a href="https://sparkbyexamples.com/apache-hive/hive-partitions-explained-with-examples/" target="_blank">Hive partitioning</a> is not used for the data in storage. A discussion of DataFrame partitioning vs Hive partitioning is beyond the scope of this class.)

#
#
# ### Adaptive Query Execution
#
# <img src="https://files.training.databricks.com/images/aspwd/partitioning_aqe.png" width="60%" />
#
# In Spark 3, <a href="https://spark.apache.org/docs/latest/sql-performance-tuning.html#adaptive-query-execution" target="_blank">AQE</a> is now able to <a href="https://databricks.com/blog/2020/05/29/adaptive-query-execution-speeding-up-spark-sql-at-runtime.html" target="_blank"> dynamically coalesce shuffle partitions</a> at runtime. This means that you can set **`spark.sql.shuffle.partitions`** based on the largest data set your application processes and allow AQE to reduce the number of partitions automatically when there is less data to process.
#
# The **`spark.sql.adaptive.enabled`** configuration option controls whether AQE is turned on/off.

spark.conf.get("spark.sql.adaptive.enabled")

#
#
# ### Clean up classroom

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
