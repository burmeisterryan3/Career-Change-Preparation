# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.3
# ---

# # Data Exploration
# - This notebook performs exploratory data analysis on the dataset.
# - To expand on the analysis, attach this notebook to a cluster with runtime version **13.3.x-cpu-ml-scala2.12**,
# edit [the options of pandas-profiling](https://pandas-profiling.ydata.ai/docs/master/rtd/pages/advanced_usage.html), and rerun it.
# - Explore completed trials in the [MLflow experiment](#mlflow/experiments/1249599295316005).

# +
import mlflow
import os
import uuid
import shutil
import pandas as pd
import databricks.automl_runtime

# Download input data from mlflow into a pandas DataFrame
# Create temporary directory to download data
temp_dir = os.path.join(os.environ["SPARK_LOCAL_DIRS"], "tmp", str(uuid.uuid4())[:8])
os.makedirs(temp_dir)

# Download the artifact and read it
training_data_path = mlflow.artifacts.download_artifacts(run_id="ae107c444e80400b836a3f774360d077", artifact_path="data", dst_path=temp_dir)
df = pd.read_parquet(os.path.join(training_data_path, "training_data"))

# Delete the temporary data
shutil.rmtree(temp_dir)

target_col = "Churn"

# Drop columns created by AutoML before pandas-profiling
df = df.drop(['_automl_split_col_0000'], axis=1)
# -

# ## Semantic Type Detection Alerts
#
# For details about the definition of the semantic types and how to override the detection, see
# [Databricks documentation on semantic type detection](https://docs.databricks.com/applications/machine-learning/automl.html#semantic-type-detection).
#
# - Semantic type `categorical` detected for column `SeniorCitizen`. Training notebooks will encode features based on categorical transformations.

# ## Profiling Results

# + large_display_output=true
from ydata_profiling import ProfileReport
df_profile = ProfileReport(df,
                           correlations={
                               "auto": {"calculate": True},
                               "pearson": {"calculate": True},
                               "spearman": {"calculate": True},
                               "kendall": {"calculate": True},
                               "phi_k": {"calculate": True},
                               "cramers": {"calculate": True},
                           }, title="Profiling Report", progress_bar=False, infer_dtypes=False)
profile_html = df_profile.to_html()

displayHTML(profile_html)
