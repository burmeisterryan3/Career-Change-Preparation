# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.3
# ---

# %% [markdown]
#
# <div style="text-align: center; line-height: 0; padding-top: 9px;">
#   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# </div>
#

# %% [markdown]
# # LAB - Online Monitoring
#
# In this lab, you will create an online monitor for a sample inference table using Databricks Lakehouse Monitoring. A sample inference table, extracted from a deployed Model Serving Endpoint, has been imported for you to use for monitoring.
#
# **Lab Outline:**
#
# *In this lab, you will need to complete the following tasks:*
#
# * **Task 1:** Define Evaluation Metrics
# * **Task 2:** Unpack the Request Payload
# * **Task 3:** Compute Metrics
# * **Task 4:** Save the Processed Inference Table
# * **Task 5:** Create a Monitor on the Inference Table
# * **Task 6:** Review the Monitor Details
# * **Task 7:** View the Monitor Dashboard

# %% [markdown]
# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **14.3.x-cpu-ml-scala2.12**

# %% [markdown]
# ## Classroom Setup
#
# Install required libraries and load classroom configuration.

# %%
# %pip install -U --quiet databricks-sdk mlflow==2.12.1 textstat tiktoken evaluate

dbutils.library.restartPython()

# %%
# %run ../Includes/Classroom-Setup-03

# %% [markdown]
# ## Inference Table
#
# You are going to use the same inference table that we used for the demo. The inference table is pre-loaded and ready to be used.

# %%
inference_table_name = f"{DA.catalog_name}.{DA.schema_name}.rag_app_realtime_payload"
display(spark.sql(f"SELECT * FROM {inference_table_name}"))

# %% [markdown]
# ## Task 1: Define Evaluation Metrics
# In this task, you will define evaluation metrics such as toxicity, perplexity, and readability, which will be used to analyze the inference table data.
#
# -  Define the evaluation metrics functions using `pandas_udf`.

# %%
# Import necessary libraries
import tiktoken, textstat, evaluate
import pandas as pd
from pyspark.sql.functions import pandas_udf

# Define a pandas UDF to compute the number of tokens in the text
@pandas_udf("int")
def compute_num_tokens(texts: pd.Series) -> pd.Series:
  encoding = tiktoken.get_encoding("cl100k_base")
  return pd.Series(<FILL_IN>)

# Define a pandas UDF to compute the toxicity of the text
@pandas_udf("double")
def compute_toxicity(texts: pd.Series) -> pd.Series:
  # Omit entries with null input from evaluation
  toxicity = <FILL_IN>
  return pd.Series(toxicity.compute(<FILL_IN>)["toxicity"]).where(<FILL_IN>)

# Define a pandas UDF to compute the perplexity of the text
@pandas_udf("double")
def compute_perplexity(texts: pd.Series) -> pd.Series:
  # Omit entries with null input from evaluation
  perplexity = <FILL_IN>
  return pd.Series(perplexity.compute(<FILL_IN>)["perplexities"]).where(<FILL_IN>)


# %% [markdown]
# ## Task 2: Unpack the Request Payload
# In this task, you will unpack the request payload from the inference table and prepare it for processing.
#
# **Steps:**
#
# - Unpack the requests as a stream.
# - Drop unnecessary columns for monitoring jobs.

# %%
import os

# Reset checkpoint [for demo purposes ONLY]
checkpoint_location = os.path.join(DA.paths.working_dir, "checkpoint")
dbutils.fs.rm(checkpoint_location, True)

# Define the JSON path and type for the input requests
INPUT_REQUEST_JSON_PATH = <FILL_IN>
INPUT_JSON_PATH_TYPE = <FILL_IN>
KEEP_LAST_QUESTION_ONLY = False

# Define the JSON path and type for the output responses
OUTPUT_REQUEST_JSON_PATH = <FILL_IN>
OUPUT_JSON_PATH_TYPE = <FILL_IN>

# Unpack the requests as a stream
requests_raw_df = spark.readStream.table(inference_table_name)
requests_processed_df = unpack_requests(
    <FILL_IN>,
    <FILL_IN>,
    <FILL_IN>,
    <FILL_IN>,
    <FILL_IN>,
    <FILL_IN>
)

# Drop un-necessary columns for monitoring jobs
requests_processed_df = <FILL_IN>

# %% [markdown]
# ## Task 3: Compute Metrics
#
# In this task, you will compute the defined evaluation metrics for the unpacked request payloads.
#
# - Compute the toxicity, perplexity, and token count for the input and output columns.

# %%
# Define the columns to measure
column_to_measure = <FILL_IN>

# Iterate over each column to measure
for column_name in column_to_measure:
    Compute the metrics and add them as new columns to the DataFrame
    requests_df_with_metrics = <FILL_IN>

# %% [markdown]
# ## Task 4: Save the Processed Inference Table
#
# In this task, you will save the processed inference table with the computed metrics to a Delta table.
#
# **Steps:**
#
# - Create the processed inference table if it doesn't exist.
# - Append the new unpacked payloads and metrics to the processed table.

# %%
from delta.tables import DeltaTable
# Define the name of the processed table
processed_table_name = f"{DA.catalog_name}.{DA.schema_name}.rag_app_processed_inferences_lab"

# Create the table if it does not exist
(DeltaTable.createOrReplace(spark)
        .tableName(<FILL_IN>) 
        .addColumns(<FILL_IN>.schema) 
        .property("delta.enableChangeDataFeed", "true") 
        .property("delta.columnMapping.mode", "name") 
        .execute()) # Execute the table creation

# Write the requests_df_with_metrics DataFrame to the processed table as a stream
(requests_df_with_metrics.writeStream
                      .trigger(availableNow=True) 
                      .format("delta") 
                      .outputMode("append") 
                      .option("checkpointLocation", <FILL_IN>)
                      .toTable(<FILL_IN>).awaitTermination())

# %% [markdown]
# ## Task 5: Create a Monitor on the Inference Table
#
# In this task, you will create a monitor on the processed inference table using Databricks Lakehouse Monitoring.
#
# - Create a monitor using the `databricks-sdk`.

# %%
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import MonitorTimeSeries
# Initialize the workspace client
w = WorkspaceClient()

try:
  # Create a monitor using the workspace client's quality_monitors service
  lhm_monitor = w.quality_monitors.create(
    table_name=<FILL_IN>,
    time_series = MonitorTimeSeries(
      timestamp_col = "timestamp",
      granularities = ["5 minutes"],
    ),
    assets_dir = <FILL_IN>,
    slicing_exprs = <FILL_IN>,
    output_schema_name=f"{DA.catalog_name}.{DA.schema_name}"
  )

Handle any exceptions that occur during monitor creation
except Exception as lhm_exception:
  <FIll_IN>

# %%
from databricks.sdk.service.catalog import MonitorInfoStatus

# Get the monitor information for the processed table
monitor_info = <FILL_IN>
print(monitor_info.status)

# Check if the monitor status is pending
if monitor_info.status == MonitorInfoStatus.<FILL_IN>:
    print("Wait until monitor creation is completed...")

# %% [markdown]
# ## Task 6: Review the Monitor Details
#
# In this task, you will review the details of the monitor created in the previous step. This will involve checking the **Quality** tab for the monitor details and reviewing the metrics tables generated by the monitor.
#
# **Steps:**
#
#
# Complete following steps:
#
#
# 1. **Review Monitor Details in Quality Tab**
#    - Go to the **[Catalog](explore/data)** and find the table you monitored.
#    - Click on the **Quality** tab to view the monitor details.
#
# 2. **Review Metrics Tables**
#    - Examine the metrics tables (`*_processed_profile_metrics` and `*_processed_drift_metrics`).
#
#
# **🚨Note:** Ensure that the refresh process is completed and the metrics tables are ready before reviewing the details.
#

# %% [markdown]
# ## Task 7: View the Monitor Dashboard
#
# In this task, you will view the Databricks SQL dashboard generated by Lakehouse Monitoring to review the data and metrics of your monitoring solution.
#
# **Steps:**
#
# Complete following steps:
#
# 1. **View the SQL Dashboard**
#    - Click on **View Dashboard** to open the SQL dashboard from the **Quality** tab.
#
# 2. **Inspect Overall Summary Statistics**
#    - Examine the overall summary statistics presented in the dashboard.
#
# 3. **Review the Created Metrics**
#    - Review the metrics that were created in the first step of this lab to understand the data quality and model performance over time.
#
#
# **🚨Note:** Make sure there is an accessible DBSQL cluster up and running to ensure dashboard creation.

# %% [markdown]
# ##Cleanup Classroom
# Run the following cell to remove lesson-specific assets created during this lesson.

# %%
DA.cleanup()

# %% [markdown]
# ## Conclusion
#
# In this lab, you created an online monitor using Databricks Lakehouse Monitoring. First, you defined evaluation metrics and computed these metrics for the inference table. Then, you created a monitor on the inference table. Lastly, you reviewed the monitor details and the auto-created Databricks SQL dashboard. After successfully completing this lab, you should be able to create online monitoring for an inference table that captures the inference requests of deployed AI models.

# %% [markdown]
#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
