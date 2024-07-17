# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.3
# ---

# %pip install mlflow==2.4.0 importlib-metadata==6.8.0 cloudpickle==2.0.0 zipp==3.16.2
# %pip install --ignore-installed Jinja2==3.1.2 markupsafe==2.1.1

# **🚨 Warning: Please don't run this notebook directly. This notebook must be used when creating the DLT pipeline. Follow the instructions listed in the "3.1.a - Pipeline Deployment" notebook.**
#
# **🚨 Warning:** For this notebook to successfully run, you must have;
# * Trained and logged a model to the registry (e.g. `ml_model`)
# * Set the `catalog` and `schema` to point to your own. 
# * Create pipeline parameters for input data path and model name (e.g. `mlpipeline.bronze_dataset_path`& `mlpipeline.model_name`)

#
# # Inference Pipeline
#
#  MLflow-trained models can be used in Delta Live Tables pipelines. MLflow models are treated as transformations in Databricks, meaning they act upon a Spark DataFrame input and return results as a Spark DataFrame. Because Delta Live Tables defines datasets against DataFrames, you can convert Apache Spark workloads that leverage MLflow to Delta Live Tables with just a few lines of code.
#
# If you already have a Python notebook calling an MLflow model, you can adapt the code to Delta Live Tables by using the `@dlt.table` decorator and ensuring functions are defined to return transformation results. For an introduction to Delta Live Tables syntax, see Tutorial: [Declare a data pipeline with Python in Delta Live Tables.](https://docs.databricks.com/en/delta-live-tables/tutorial-python.html)
#

#
# ## Pipeline configs

bronze_dataset_path = spark.conf.get("mlpipeline.bronze_dataset_path")
model_name = spark.conf.get("mlpipeline.model_name")

# ## Inference configs

# +
import mlflow


mlflow.set_registry_uri("databricks-uc")
model_uri=f"models:/{model_name}@DLT" 
loaded_model_udf = mlflow.pyfunc.spark_udf(spark, model_uri=model_uri, result_type="string")

primary_key = "customerID"
features = ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]
# -

# ## DLT Inference code

# +
import dlt
from pyspark.sql.functions import col, struct


@dlt.table(
  name="raw_inputs",
  comment="Raw inputs table",
  table_properties={
    "quality": "bronze"
  } 
)
def raw_inputs():
  return spark.read.csv(bronze_dataset_path, inferSchema=True, header=True, multiLine=True, escape='"')
  
@dlt.table(
  name="features_input",
  comment="Features table",
  table_properties={
    "quality": "silver"
  }
)
def features_input():
  return (
    dlt.read("raw_inputs")
    .select(primary_key, *features)
    .withColumn("SeniorCitizen",col("SeniorCitizen").cast('double'))
    .withColumn("tenure",col("tenure").cast('double'))
    .withColumn("TotalCharges",col("TotalCharges").cast('double'))
    .na.drop(how='any')
  )

@dlt.table(
  name="model_predictions",
  comment="Inference table",
  table_properties={
    "quality": "gold"
  }
)
def model_predictions():
  return (
    dlt.read("features_input")
    .withColumn("prediction", loaded_model_udf(struct(features)))
  )
