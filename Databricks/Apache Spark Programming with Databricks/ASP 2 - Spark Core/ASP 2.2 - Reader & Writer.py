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
# # Reader & Writer
# ##### Objectives
# 1. Read from CSV files
# 1. Read from JSON files
# 1. Write DataFrame to files
# 1. Write DataFrame to tables
# 1. Write DataFrame to a Delta table
#
# ##### Methods
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.html" target="_blank">DataFrameReader</a>: **`csv`**, **`json`**, **`option`**, **`schema`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameWriter.html" target="_blank">DataFrameWriter</a>: **`mode`**, **`option`**, **`parquet`**, **`format`**, **`saveAsTable`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.types.StructType.html?highlight=structtype#pyspark.sql.types.StructType" target="_blank">StructType</a>: **`toDDL`**
#
# ##### Spark Types
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/data_types.html" target="_blank">Types</a>: **`ArrayType`**, **`DoubleType`**, **`IntegerType`**, **`LongType`**, **`StringType`**, **`StructType`**, **`StructField`**

# %run ../Includes/Classroom-Setup

#
#
# ## DataFrameReader
# Interface used to load a DataFrame from external storage systems
#
# **`spark.read.parquet("path/to/files")`**
#
# DataFrameReader is accessible through the SparkSession attribute **`read`**. This class includes methods to load DataFrames from different external storage systems.

#
#
# ### Read from CSV files
# Read from CSV with the DataFrameReader's **`csv`** method and the following options:
#
# Tab separator, use first line as header, infer schema

# +
users_csv_path = f"{DA.paths.datasets}/ecommerce/users/users-500k.csv"

# NOTE: Read is not an action, but to trigger the schema inference an action is required... which is why Spark Jobs are created
users_df = (spark
           .read
           .option("sep", "\t")
           .option("header", True)
           .option("inferSchema", True)
           .csv(users_csv_path)
          )

users_df.printSchema()
# -

#
#
# Spark's Python API also allows you to specify the DataFrameReader options as parameters to the **`csv`** method

# +
users_df = (spark
           .read
           .csv(users_csv_path, sep="\t", header=True, inferSchema=True)
          )

users_df.printSchema()
# -

#
#
#
# Manually define the schema by creating a **`StructType`** with column names and data types

# +
from pyspark.sql.types import LongType, StringType, StructType, StructField

user_defined_schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("user_first_touch_timestamp", LongType(), True),
    StructField("email", StringType(), True)
])
# -

#
#
#
# Read from CSV using this user-defined schema instead of inferring the schema

# NOTE: By predefining the schema, no jobs are created as no action is taken on the data.
users_df = (spark
           .read
           .option("sep", "\t")
           .option("header", True)
           .schema(user_defined_schema)
           .csv(users_csv_path)
          )

#
#
#
# Alternatively, define the schema using <a href="https://en.wikipedia.org/wiki/Data_definition_language" target="_blank">data definition language (DDL)</a> syntax.

# +
ddl_schema = "user_id string, user_first_touch_timestamp long, email string"

users_df = (spark
           .read
           .option("sep", "\t")
           .option("header", True)
           .schema(ddl_schema)
           .csv(users_csv_path)
          )
# -

#
#
# ### Read from JSON files
#
# Read from JSON with DataFrameReader's **`json`** method and the infer schema option

# +
events_json_path = f"{DA.paths.datasets}/ecommerce/events/events-500k.json"

events_df = (spark
            .read
            .option("inferSchema", True)
            .json(events_json_path)
           )

events_df.printSchema()
# -

#
#
#
# Read data faster by creating a **`StructType`** with the schema names and data types

# +
from pyspark.sql.types import ArrayType, DoubleType, IntegerType, LongType, StringType, StructType, StructField

user_defined_schema = StructType([
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

events_df = (spark
            .read
            .schema(user_defined_schema)
            .json(events_json_path)
           )
# -

#
#
#
# You can use the **`StructType`** Scala method **`toDDL`** to have a DDL-formatted string created for you.
#
# This is convenient when you need to get the DDL-formated string for ingesting CSV and JSON but you don't want to hand craft it or the **`StructType`** variant of the schema.
#
# However, this functionality is not available in Python but the power of the notebooks allows us to use both languages.

# Step 1 - use this trick to transfer a value (the dataset path) between Python and Scala using the shared spark-config
spark.conf.set("whatever_your_scope.events", events_json_path)

#
#
# In a Python notebook like this one, create a Scala cell to injest the data and produce the DDL formatted schema

# +
# %scala
// Step 2 - pull the value from the config (or copy & paste it)
val eventsJsonPath = spark.conf.get("whatever_your_scope.events")

// Step 3 - Read in the JSON, but let it infer the schema
val eventsSchema = spark.read
                        .option("inferSchema", true)
                        .json(eventsJsonPath)
                        .schema.toDDL

// Step 4 - print the schema, select it, and copy it.
println("="*80)
println(eventsSchema)
println("="*80)

# +
# Step 5 - paste the schema from above and assign it to a variable as seen here
events_schema = "`device` STRING,`ecommerce` STRUCT<`purchase_revenue_in_usd`: DOUBLE, `total_item_quantity`: BIGINT, `unique_items`: BIGINT>,`event_name` STRING,`event_previous_timestamp` BIGINT,`event_timestamp` BIGINT,`geo` STRUCT<`city`: STRING, `state`: STRING>,`items` ARRAY<STRUCT<`coupon`: STRING, `item_id`: STRING, `item_name`: STRING, `item_revenue_in_usd`: DOUBLE, `price_in_usd`: DOUBLE, `quantity`: BIGINT>>,`traffic_source` STRING,`user_first_touch_timestamp` BIGINT,`user_id` STRING"

# Step 6 - Read in the JSON data using our new DDL formatted string
events_df = (spark.read
                 .schema(events_schema)
                 .json(events_json_path))

display(events_df)
# -

#
#
# This is a great "trick" for producing a schema for a net-new dataset and for accelerating development.
#
# When you are done (e.g. for Step #7), make sure to delete your temporary code.
#
# <img src="https://files.training.databricks.com/images/icon_warn_32.png"> WARNING: **Do not use this trick in production**</br>
# the inference of a schema can be REALLY slow as it<br/>
# forces a full read of the source dataset to infer the schema

#
#
# ## DataFrameWriter
# Interface used to write a DataFrame to external storage systems
#
# <strong><code>
# (df  
# &nbsp;  .write                         
# &nbsp;  .option("compression", "snappy")  
# &nbsp;  .mode("overwrite")      
# &nbsp;  .parquet(output_dir)       
# )
# </code></strong>
#
# DataFrameWriter is accessible through the SparkSession attribute **`write`**. This class includes methods to write DataFrames to different external storage systems.

#
#
# ### Write DataFrames to files
#
# Write **`users_df`** to parquet with DataFrameWriter's **`parquet`** method and the following configurations:
#
# Snappy compression, overwrite mode

# +
users_output_dir = f"{DA.paths.working_dir}/users.parquet"

(users_df
 .write
 .option("compression", "snappy") # default for Parquet
 .mode("overwrite")
 .parquet(users_output_dir)
)
# -

display(
    dbutils.fs.ls(users_output_dir)
)

#
#
# As with DataFrameReader, Spark's Python API also allows you to specify the DataFrameWriter options as parameters to the **`parquet`** method

(users_df
 .write
 .parquet(users_output_dir, compression="snappy", mode="overwrite")
)

#
#
# ### Write DataFrames to tables
#
# Write **`events_df`** to a table using the DataFrameWriter method **`saveAsTable`**
#
# <img src="https://files.training.databricks.com/images/icon_note_32.png" alt="Note"> This creates a global table, unlike the local view created by the DataFrame method **`createOrReplaceTempView`**

events_df.write.mode("overwrite").saveAsTable("events")

# %sql
SELECT *
FROM events
LIMIT 10;

#
#
#
# This table was saved in the database created for you in classroom setup.
#
# See database name printed below.

print(f"Database Name: {DA.schema_name}")

#
#
#
# ... or even the tables in that database:

# %sql
SHOW TABLES IN ${DA.schema_name}

#
#
# ## Delta Lake
#
# In almost all cases, the best practice is to use Delta Lake format, especially whenever the data will be referenced from a Databricks workspace. 
#
# <a href="https://delta.io/" target="_blank">Delta Lake</a> is an open source technology designed to work with Spark to bring reliability to data lakes.
#
# ![delta](https://files.training.databricks.com/images/aspwd/delta_storage_layer.png)
#
# #### Delta Lake's Key Features
# - ACID transactions
# - Scalable metadata handling
# - Unified streaming and batch processing
# - Time travel (data versioning)
# - Schema enforcement and evolution
# - Audit history
# - Parquet format
# - Compatible with Apache Spark API

#
#
# ### Write Results to a Delta Table
#
# Write **`events_df`** with the DataFrameWriter's **`save`** method and the following configurations: Delta format & overwrite mode.

# +
events_output_path = f"{DA.paths.working_dir}/delta/events"

(events_df
 .write
 .format("delta")
 .mode("overwrite")
 .save(events_output_path)
)
# -

#
#
# ### Clean up classroom

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
