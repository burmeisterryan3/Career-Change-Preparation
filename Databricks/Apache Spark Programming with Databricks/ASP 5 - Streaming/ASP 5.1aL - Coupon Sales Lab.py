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
# # Coupon Sales Lab
# Process and append streaming data on transactions using coupons.
# 1. Read data stream
# 2. Filter for transactions with coupons codes
# 3. Write streaming query results to Delta
# 4. Monitor streaming query
# 5. Stop streaming query
#
# ##### Classes
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/api/pyspark.sql.streaming.DataStreamReader.html" target="_blank">DataStreamReader</a>
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/api/pyspark.sql.streaming.DataStreamWriter.html" target="_blank">DataStreamWriter</a>
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.ss/api/pyspark.sql.streaming.StreamingQuery.html" target="_blank">StreamingQuery</a>

# %run ../Includes/Classroom-Setup-5.1a

#
#
# ### 1. Read data stream
# - Set to process 1 file per trigger
# - Read from Delta files in the source directory specified by **`DA.paths.sales`**
#
# Assign the resulting DataFrame to **`df`**.

# TODO
df = (spark.readStream.option("maxFilesPerTrigger", 1).format("delta").load(DA.paths.sales))

#
#
#
# **1.1: CHECK YOUR WORK**

DA.tests.validate_1_1(df)

#
#
# ### 2. Filter for transactions with coupon codes
# - Explode the **`items`** field in **`df`** with the results replacing the existing **`items`** field
# - Filter for records where **`items.coupon`** is not null
#
# Assign the resulting DataFrame to **`coupon_sales_df`**.

# +
from pyspark.sql.functions import explode, col

coupon_sales_df = (df.withColumn("items", explode(col("items")))
                   .filter(col("items.coupon").isNotNull())
)
# -

#
#
#
# **2.1: CHECK YOUR WORK**

DA.tests.validate_2_1(coupon_sales_df.schema)

#
#
# ### 3. Write streaming query results to Delta
# - Configure the streaming query to write Delta format files in "append" mode
# - Set the query name to "coupon_sales"
# - Set a trigger interval of 1 second
# - Set the checkpoint location to **`coupons_checkpoint_path`**
# - Set the output path to **`coupons_output_path`**
#
# Start the streaming query and assign the resulting handle to **`coupon_sales_query`**.

# +
# TODO
coupons_checkpoint_path = f"{DA.paths.checkpoints}/coupon-sales"
coupons_output_path = f"{DA.paths.working_dir}/coupon-sales/output"

coupon_sales_query = (coupon_sales_df.writeStream
                                     .outputMode("append")
                                     .format("delta")
                                     .queryName("coupon_sales")
                                     .trigger(processingTime="1 second")
                                     .option("checkpointLocation", coupons_checkpoint_path)
                                     .start(coupons_output_path)
)

DA.block_until_stream_is_ready(coupon_sales_query)
# -

#
#
#
# **3.1: CHECK YOUR WORK**

DA.tests.validate_3_1(coupon_sales_query)

#
#
# ### 4. Monitor streaming query
# - Get the ID of streaming query and store it in **`queryID`**
# - Get the status of streaming query and store it in **`queryStatus`**

# TODO
query_id = coupon_sales_query.id

# TODO
query_status = coupon_sales_query.status

#
#
#
# **4.1: CHECK YOUR WORK**

DA.tests.validate_4_1(query_id, query_status)

#
#
# ### 5. Stop streaming query
# - Stop the streaming query

# TODO
coupon_sales_query.stop()
coupon_sales_query.awaitTermination()

#
#
#
# **5.1: CHECK YOUR WORK**

DA.tests.validate_5_1(coupon_sales_query)

#
#
# ### 6. Verify the records were written in Delta format

display(dbutils.fs.ls(coupons_output_path))

#
#
# ### Classroom Cleanup
# Run the cell below to clean up resources.

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
