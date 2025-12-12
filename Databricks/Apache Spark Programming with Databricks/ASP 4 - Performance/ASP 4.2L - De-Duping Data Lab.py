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
# # De-Duping Data Lab
#
# In this exercise, we're doing ETL on a file we've received from a customer. That file contains data about people, including:
#
# * first, middle and last names
# * gender
# * birth date
# * Social Security number
# * salary
#
# But, as is unfortunately common in data we get from this customer, the file contains some duplicate records. Worse:
#
# * In some of the records, the names are mixed case (e.g., "Carol"), while in others, they are uppercase (e.g., "CAROL").
# * The Social Security numbers aren't consistent either. Some of them are hyphenated (e.g., "992-83-4829"), while others are missing hyphens ("992834829").
#
# If all of the name fields match -- if you disregard character case -- then the birth dates and salaries are guaranteed to match as well,
# and the Social Security Numbers *would* match if they were somehow put in the same format.
#
# Your job is to remove the duplicate records. The specific requirements of your job are:
#
# * Remove duplicates. It doesn't matter which record you keep; it only matters that you keep one of them.
# * Preserve the data format of the columns. For example, if you write the first name column in all lowercase, you haven't met this requirement.
#
# <img src="https://files.training.databricks.com/images/icon_hint_32.png" alt="Hint"> The initial dataset contains 103,000 records.
# The de-duplicated result has 100,000 records.
#
# Next, write the results in **Delta** format as a **single data file** to the directory given by the variable **delta_dest_dir**.
#
# <img src="https://files.training.databricks.com/images/icon_hint_32.png" alt="Hint"> Remember the relationship between the number of partitions in a DataFrame and the number of files written.
#
# ##### Methods
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/io.html" target="_blank">DataFrameReader</a>
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html" target="_blank">DataFrame</a>
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html" target="_blank">Built-In Functions</a>
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/io.html" target="_blank">DataFrameWriter</a>

# %run ../Includes/Classroom-Setup

#
#
# It's helpful to look at the file first, so you can check the format with **`dbutils.fs.head()`**.

dbutils.fs.head(f"{DA.paths.datasets}/people/people-with-dups.txt")

# +
source_file = f"{DA.paths.datasets}/people/people-with-dups.txt"
delta_dest_dir = f"{DA.paths.working_dir}/people"

# In case it already exists
dbutils.fs.rm(delta_dest_dir, True)

# +
df = spark.read.csv(source_file, header=True, inferSchema=True, sep=":")

display(df)

# +
from pyspark.sql.functions import lower

df = (df.withColumn("firstName_lower", lower("firstName"))
        .withColumn("middleName_lower", lower("middleName"))
        .withColumn("lastName_lower", lower("lastName"))
)

df = df.dropDuplicates(["firstName_lower", "middleName_lower", "lastName_lower"])
df = df.drop("firstName_lower", "middleName_lower", "lastName_lower")

display(df)

# +
from pyspark.sql.functions import col, regexp_replace, when

df = df.withColumn("ssn", when(col("ssn").rlike(r'^\d{9}$'),
                               regexp_replace(col("ssn"), 
                                              r'(\d{3})(\d{2})(\d{4})',
                                              r'$1-$2-$3')
                               ).otherwise(col("ssn"))
)

display(df)
# -

# The coalesce(1) method is used to reduce the DataFrame to a single partition, ensuring that only one file is created.
df.coalesce(1).write.format("delta").mode("overwrite").save(delta_dest_dir)

#
#
#
# **CHECK YOUR WORK**

# +
verify_files = dbutils.fs.ls(delta_dest_dir)
verify_delta_format = False
verify_num_data_files = 0
for f in verify_files:
    if f.name == "_delta_log/":
        verify_delta_format = True
    elif f.name.endswith(".parquet"):
        verify_num_data_files += 1

assert verify_delta_format, "Data not written in Delta format"
assert verify_num_data_files == 1, "Expected 1 data file written"

verify_record_count = spark.read.format("delta").load(delta_dest_dir).count()
assert verify_record_count == 100000, "Expected 100000 records in final result"

del verify_files, verify_delta_format, verify_num_data_files, verify_record_count
print("All test pass")
# -

#
#
# ## Clean up classroom
# Run the cell below to clean up resources.

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
