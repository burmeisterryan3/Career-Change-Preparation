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
# # LAB - Load and Explore Data
#
#
# Welcome to the "Load and Explore Data" lab! In this session, you will learn essential skills in data loading and exploration using PySpark in a Databricks environment. Gain hands-on experience reading data from Delta tables, managing data permissions, computing summary statistics, and using data profiling tools to unveil insights in your Telco dataset. Let's dive into the world of data exploration!
#
#
# **Lab Outline:**
#
#
# In this Lab, you will learn how to:
# 1. Read data from delta table
# 1. Manage data permissions
# 1. Show summary statistics
# 1. Use data profiler to explore data frame
#     - Check outliers
#     - Check data distributions
# 1. Read previous versions of the delta table
#

#
# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **13.3.x-cpu-ml-scala2.12**

#
# ## Lab Setup
#
# Before starting the Lab, follow these initial steps:
#
# 1. Run the provided classroom setup script. This script will establish necessary configuration variables tailored to each user. Execute the following code cell:

# %run ../Includes/Classroom-Setup-01

#
# **Other Conventions:**
#
# Throughout this lab, we'll make use of the object `DA`, which provides critical variables. Execute the code block below to see various variables that will be used in this notebook:

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")
print(f"Dataset Location:  {DA.paths.datasets}")

# ##Task 1: Read Data from Delta Table
#
#
# + Use Spark to read data from the Delta table into a DataFrame.
#
#

# +
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType

dataset_path = f"{DA.paths.datasets}/telco/telco-customer-churn-missing.csv"

schema = StructType([
    StructField("customerID", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("SeniorCitizen", DoubleType(), True),
    StructField("Partner", StringType(), True),
    StructField("Dependents", StringType(), True),
    StructField("tenure", DoubleType(), True),
    StructField("PhoneService", StringType(), True),
    StructField("MultipleLines", StringType(), True),
    StructField("InternetService", StringType(), True),
    StructField("OnlineSecurity", StringType(), True),
    StructField("OnlineBackup", StringType(), True),
    StructField("DeviceProtection", StringType(), True),
    StructField("TechSupport", StringType(), True),
    StructField("StreamingTV", StringType(), True),
    StructField("StreamingMovies", StringType(), True),
    StructField("Contract", StringType(), True),
    StructField("PaperlessBilling", StringType(), True),
    StructField("PaymentMethod", StringType(), True),
    StructField("MonthlyCharges", DoubleType(), True),
    StructField("TotalCharges", DoubleType(), True),  # TotalCharges should be DoubleType but may contain empty strings.
    StructField("Churn", StringType(), True)
])

telco_df = spark.read.csv(dataset_path,
                          header=True,
                          schema=schema,
                          multiLine=True,
                          escape='"'
                         )

table_name = "telco_missing"
table_name_bronze = f"{table_name}_bronze"

telco_df.write.mode("overwrite").option("overwriteSchema", "True").saveAsTable(table_name_bronze)
display(telco_df)
# -

# ##Task 2: Manage Data Permissions
#
# Establish controlled access to the Telco Delta table by granting specific permissions for essential actions.
#
# + Grant permissions for specific actions (e.g., read, write) on the Delta table.

# %sql
GRANT SELECT ON default.telco_missing_bronze TO `labuser6987190@vocareum.com`;

# ##Task 3: Show Summary Statistics
#
#
# Compute and present key statistical metrics to gain a comprehensive understanding of the Telco dataset.
#
#
# + Utilize PySpark to compute and display summary statistics for the Telco dataset.
#
# + Include key metrics such as mean, standard deviation, min, max, etc.

display(telco_df.summary())

# ##Task 4: Use Data Profiler to Explore DataFrame
# Use the Data Profiler and Visualization Editor tools.
#
# + Use the Data Profiler to explore the structure, data types, and basic statistics of the DataFrame.
#     - **Task 4.1.1:** Identify columns with missing values and analyze the percentage of missing data for each column.
#     - **Task 4.1.2:** Review the data types of each column to ensure they match expectations. Identify any columns that might need type conversion.
# + Use Visualization Editor to Check Outliers and Data Distributions:
#     - **Task 4.2.1:** Create a bar chart to visualize the distribution of churned and non-churned customers.
#     - **Task 4.2.2:** Generate a pie chart to visualize the distribution of different contract types.
#     - **Task 4.2.3:** Create a scatter plot to explore the relationship between monthly charges and total charges.
#     - **Task 4.2.4:** Visualize the count of customers for each payment method using a bar chart.
#     - **Task 4.2.5:** Compare monthly charges for different contract types using a box plot.
#             

# +
# Display the data and Explore the Data Profiler and Visualization Editor
dbutils.data.summarize(telco_df)

# Select "+" and "Data Profile" for same result as above
# display(telco_df)
# -

# Display the data and Explore the Data Profiler and Visualization Editor
display(telco_df)

# ##Task 5: Drop the Column
# Remove a specific column, enhancing data cleanliness and focus.
#
#
# + Identify the column that needs to be dropped. For example, let's say we want to drop the 'SeniorCitizen' column.
#
#
# + Use the appropriate command or method to drop the identified column from the Telco dataset.
#
#
# + Verify that the column has been successfully dropped by displaying the updated dataset.

# +
telco_dropped_df = telco_df.drop("SeniorCitizen")

telco_dropped_df.write.mode("overwrite").saveAsTable(table_name_bronze)
# -

# ##Task 6: Time-Travel to First 
#
#
# Revert the Telco dataset back to its initial state, exploring the characteristics of the first version.
#
#
# + Utilize time-travel capabilities to revert the dataset to its initial version.
#
#
# + Display and analyze the first version of the Telco dataset to understand its original structure and content.
#

# %sql
DESCRIBE HISTORY telco_missing_bronze

timestamp_v0 = spark.sql("DESCRIBE HISTORY telco_missing_bronze").orderBy("version").first()["timestamp"]
(spark
        .read
        #.option("versionAsOf", 0)
        .option("timestampAsOf", timestamp_v0)
        .table(table_name_bronze)
        .printSchema()
)

#
# ##Task 7: Read previous versions of the delta table
# Demonstrate the ability to read data from a specific version of the Delta table.
#
# + Replace the timestamp in the code with the actual version or timestamp of interest.

# %sql
SELECT *
FROM telco_missing_bronze
VERSION AS OF 0;

#
# ## Clean up Classroom
#
# Run the following cell to remove lessons-specific assets created during this lesson.

DA.cleanup()

# ##Conclusion
# In this lab, you demonstrated how to explore and manipulate the dataset using Databricks, focusing on data exploration, management, and time-travel capabilities. 

# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
