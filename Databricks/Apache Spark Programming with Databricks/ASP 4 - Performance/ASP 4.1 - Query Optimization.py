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
# # Query Optimization
#
# We'll explore query plans and optimizations for several examples including logical optimizations and exanples with and without predicate pushdown.
#
# ##### Objectives
# 1. Logical optimizations
# 1. Predicate pushdown
# 1. No predicate pushdown
#
# ##### Methods 
# - <a href="https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.DataFrame.explain.html#pyspark.sql.DataFrame.explain" target="_blank">DataFrame</a>: **`explain`**

#
#
#
# Let’s run our set up cell, and get our initial DataFrame stored in the variable **`df`**. Displaying this DataFrame shows us events data.

# %run ../Includes/Classroom-Setup

df = spark.read.format("delta").load(DA.paths.events)
display(df)

#
#
# ### Logical Optimization
#
# **`explain(..)`** prints the query plans, optionally formatted by a given explain mode. Compare the following logical plan & physical plan, noting how Catalyst handled the multiple **`filter`** transformations.

# +
from pyspark.sql.functions import col

limit_events_df = (df
                   .filter(col("event_name") != "reviews")
                   .filter(col("event_name") != "checkout")
                   .filter(col("event_name") != "register")
                   .filter(col("event_name") != "email_coupon")
                   .filter(col("event_name") != "cc_info")
                   .filter(col("event_name") != "delivery")
                   .filter(col("event_name") != "shipping_info")
                   .filter(col("event_name") != "press")
                  )

limit_events_df.explain(True)
# -

#
#
# Of course, we could have written the query originally using a single **`filter`** condition ourselves. Compare the previous and following query plans.

# +
better_df = (df
             .filter((col("event_name").isNotNull()) &
                     (col("event_name") != "reviews") &
                     (col("event_name") != "checkout") &
                     (col("event_name") != "register") &
                     (col("event_name") != "email_coupon") &
                     (col("event_name") != "cc_info") &
                     (col("event_name") != "delivery") &
                     (col("event_name") != "shipping_info") &
                     (col("event_name") != "press"))
            )

better_df.explain(True)
# -

#
#
# Of course, we wouldn't write the following code intentionally, but in a long, complex query you might not notice the duplicate filter conditions. Let's see what Catalyst does with this query.

# +
stupid_df = (df
             .filter(col("event_name") != "finalize")
             .filter(col("event_name") != "finalize")
             .filter(col("event_name") != "finalize")
             .filter(col("event_name") != "finalize")
             .filter(col("event_name") != "finalize")
            )

stupid_df.explain(True)
# -

#
#
# ### Caching
#
# By default the data of a DataFrame is present on a Spark cluster only while it is being processed during a query -- it is not automatically persisted on the cluster afterwards. (Spark is a data processing engine, not a data storage system.) You can explicity request Spark to persist a DataFrame on the cluster by invoking its **`cache`** method.
#
# If you do cache a DataFrame, you should always explictly evict it from cache by invoking **`unpersist`** when you no longer need it.
#
# <img src="https://files.training.databricks.com/images/icon_best_32.png" alt="Best Practice"> Caching a DataFrame can be appropriate if you are certain that you will use the same DataFrame multiple times, as in:
#
# - Exploratory data analysis
# - Machine learning model training
#
# <img src="https://files.training.databricks.com/images/icon_warn_32.png" alt="Warning"> Aside from those use cases, you should **not** cache DataFrames because it is likely that you'll *degrade* the performance of your application.
#
# - Caching consumes cluster resources that could otherwise be used for task execution
# - Caching can prevent Spark from performing query optimizations, as shown in the next example

#
#
# ### Predicate Pushdown
#
# Here is example reading from a JDBC source, where Catalyst determines that *predicate pushdown* can take place.

# %scala
// Ensure that the driver class is loaded
Class.forName("org.postgresql.Driver")

# +
jdbc_url = "jdbc:postgresql://server1.training.databricks.com/training"

# Username and Password w/read-only rights
conn_properties = {
    "user" : "training",
    "password" : "training"
}

pp_df = (spark
         .read
         .jdbc(url=jdbc_url,                 # the JDBC URL
               table="training.people_1m",   # the name of the table
               column="id",                  # the name of a column of an integral type that will be used for partitioning
               lowerBound=1,                 # the minimum value of columnName used to decide partition stride
               upperBound=1000000,           # the maximum value of columnName used to decide partition stride
               numPartitions=8,              # the number of partitions/connections
               properties=conn_properties    # the connection properties
              )
         .filter(col("gender") == "M")   # Filter the data by gender
        )

pp_df.explain(True)
# -

#
#
#
# Note the lack of a **Filter** and the presence of a **PushedFilters** in the **Scan**. The filter operation is pushed to the database and only the matching records are sent to Spark. This can greatly reduce the amount of data that Spark needs to ingest.

#
#
# ### No Predicate Pushdown
#
# In comparison, caching the data before filtering eliminates the possibility for the predicate push down.

# +
cached_df = (spark
            .read
            .jdbc(url=jdbc_url,
                  table="training.people_1m",
                  column="id",
                  lowerBound=1,
                  upperBound=1000000,
                  numPartitions=8,
                  properties=conn_properties
                 )
            )

cached_df.cache()
filtered_df = cached_df.filter(col("gender") == "M")

filtered_df.explain(True)
# -

#
#
#
# In addition to the **Scan** (the JDBC read) we saw in the previous example, here we also see the **InMemoryTableScan** followed by a **Filter** in the explain plan.
#
# This means Spark had to read ALL the data from the database and cache it, and then scan it in cache to find the records matching the filter condition.

#
#
# Remember to clean up after ourselves!

cached_df.unpersist()

#
#
# ### Clean up classroom

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
