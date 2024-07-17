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
# # Datetime Functions
#
# ##### Objectives
# 1. Cast to timestamp
# 2. Format datetimes
# 3. Extract from timestamp
# 4. Convert to date
# 5. Manipulate datetimes
#
# ##### Methods
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/column.html" target="_blank">Column</a>: **`cast`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html#datetime-functions" target="_blank">Built-In Functions</a>: **`date_format`**, **`to_date`**, **`date_add`**, **`year`**, **`month`**, **`dayofweek`**, **`minute`**, **`second`**

# %run ../Includes/Classroom-Setup

#
#
#
# Let's use a subset of the BedBricks events dataset to practice working with date times.

# +
from pyspark.sql.functions import col

df = spark.read.format("delta").load(DA.paths.events).select("user_id", col("event_timestamp").alias("timestamp"))
display(df)
# -

#
#
# ### Built-In Functions: Date Time Functions
# Here are a few built-in functions to manipulate dates and times in Spark.
#
# | Method | Description |
# | --- | --- |
# | **`add_months`** | Returns the date that is numMonths after startDate |
# | **`current_timestamp`** | Returns the current timestamp at the start of query evaluation as a timestamp column |
# | **`date_format`** | Converts a date/timestamp/string to a value of string in the format specified by the date format given by the second argument. |
# | **`dayofweek`** | Extracts the day of the month as an integer from a given date/timestamp/string |
# | **`from_unixtime`** | Converts the number of seconds from unix epoch (1970-01-01 00:00:00 UTC) to a string representing the timestamp of that moment in the current system time zone in the yyyy-MM-dd HH:mm:ss format |
# | **`minute`** | Extracts the minutes as an integer from a given date/timestamp/string. |
# | **`unix_timestamp`** | Converts time string with given pattern to Unix timestamp (in seconds) |

#
#
# ### Cast to Timestamp

#
#
# #### **`cast()`**
# Casts column to a different data type, specified using string representation or DataType.

timestamp_df = df.withColumn("timestamp", (col("timestamp") / 1e6).cast("timestamp"))
display(timestamp_df)

# +
from pyspark.sql.types import TimestampType

timestamp_df = df.withColumn("timestamp", (col("timestamp") / 1e6).cast(TimestampType()))
display(timestamp_df)
# -

#
#
# ### Datetime Patterns for Formatting and Parsing
# There are several common scenarios for datetime usage in Spark:
#
# - CSV/JSON datasources use the pattern string for parsing and formatting datetime content.
# - Datetime functions related to convert StringType to/from DateType or TimestampType e.g. **`unix_timestamp`**, **`date_format`**, **`from_unixtime`**, **`to_date`**, **`to_timestamp`**, etc.
#
# Spark uses <a href="https://spark.apache.org/docs/latest/sql-ref-datetime-pattern.html" target="_blank">pattern letters for date and timestamp parsing and formatting</a>. A subset of these patterns are shown below.
#
# | Symbol | Meaning         | Presentation | Examples               |
# | ------ | --------------- | ------------ | ---------------------- |
# | G      | era             | text         | AD; Anno Domini        |
# | y      | year            | year         | 2020; 20               |
# | D      | day-of-year     | number(3)    | 189                    |
# | M/L    | month-of-year   | month        | 7; 07; Jul; July       |
# | d      | day-of-month    | number(3)    | 28                     |
# | Q/q    | quarter-of-year | number/text  | 3; 03; Q3; 3rd quarter |
# | E      | day-of-week     | text         | Tue; Tuesday           |
#
# <img src="https://files.training.databricks.com/images/icon_warn_32.png" alt="Warning"> Spark's handling of dates and timestamps changed in version 3.0, and the patterns used for parsing and formatting these values changed as well. For a discussion of these changes, please reference <a href="https://databricks.com/blog/2020/07/22/a-comprehensive-look-at-dates-and-timestamps-in-apache-spark-3-0.html" target="_blank">this Databricks blog post</a>.

#
#
# ### Format date

#
#
# #### **`date_format()`**
# Converts a date/timestamp/string to a string formatted with the given date time pattern.

# +
from pyspark.sql.functions import date_format

formatted_df = (timestamp_df
                .withColumn("date string", date_format("timestamp", "MMMM dd, yyyy"))
                .withColumn("time string", date_format(col("timestamp"), "HH:mm:ss.SSSSSS"))
               )
display(formatted_df)
# -

#
#
# ### Extract datetime attribute from timestamp

#
#
# #### **`year`**
# Extracts the year as an integer from a given date/timestamp/string.
#
# ##### Similar methods: **`month`**, **`dayofweek`**, **`minute`**, **`second`**, etc.

# +
from pyspark.sql.functions import year, month, dayofweek, minute, second

datetime_df = (timestamp_df
               .withColumn("year", year(col("timestamp")))
               .withColumn("month", month(col("timestamp")))
               .withColumn("dayofweek", dayofweek(col("timestamp")))
               .withColumn("minute", minute(col("timestamp")))
               .withColumn("second", second(col("timestamp")))
              )
display(datetime_df)
# -

#
#
# ### Convert to Date

#
#
# #### **`to_date`**
# Converts the column into DateType by casting rules to DateType.

# +
from pyspark.sql.functions import to_date

date_df = timestamp_df.withColumn("date", to_date(col("timestamp")))
display(date_df)
# -

#
#
# ### Manipulate Datetimes

#
#
# #### **`date_add`**
# Returns the date that is the given number of days after start

# +
from pyspark.sql.functions import date_add

plus_2_df = timestamp_df.withColumn("plus_two_days", date_add(col("timestamp"), 2))
display(plus_2_df)
# -

#
#
# ### Clean up classroom

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
