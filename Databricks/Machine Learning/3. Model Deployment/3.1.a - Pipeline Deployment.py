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
#   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# </div>
#

#
# # Pipeline Deployment
#
# In this demo, we will show how to use a model as part of a data pipeline for inference. In the first section of the demo, we will prepare data and perform some basic feature engineering. Then, we will fit and register the model to model registry. Please note that these two steps are already covered in other courses and they are not the main focus of this demo. In the last section, which is the main focus of this demo, we will create a Delta Live Tables (DLT) pipeline and use the registered model as part of the pipeline. 
#
# **Learning Objectives:**
#
# *By the end of this demo, you will be able to;*
#
# * Describe steps for deploying a model within a pipeline.
#
# * Develop a simple Delta Live Tables pipeline that performs batch inference in its final step.
#

# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **13.3.x-cpu-ml-scala2.12**

#
# ## Classroom Setup
#
# Before starting the demo, run the provided classroom setup script. This script will define configuration variables necessary for the demo. Execute the following cell:

# %run ../Includes/Classroom-Setup-01

# **Other Conventions:**
#
# Throughout this demo, we'll refer to the object `DA`. This object, provided by Databricks Academy, contains variables such as your username, catalog name, schema name, working directory, and dataset locations. Run the code block below to view these details:

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")
print(f"User DB Location:  {DA.paths.datasets}")

# ## Data Preparation
#
# For this demonstration, we will utilize a fictional dataset from a Telecom Company, which includes customer information. This dataset encompasses **customer demographics**, including gender, as well as internet subscription details such as subscription plans and payment methods.
#
# After load the dataset, we will perform simple **data cleaning and feature selection**. 
#
# In the final step, we will split the dataset to **features** and **response** sets.

# +
from pyspark.sql.functions import col

#dataset path 
dataset_p_telco = f"{DA.paths.datasets}/telco/telco-customer-churn.csv"

# Dataset specs
primary_key = "customerID"
response = "Churn"
features = ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"] # Keeping numerical only for simplicity and demo purposes

# Read dataset (and drop nan)
telco_df = spark.read.csv(dataset_p_telco, inferSchema=True, header=True, multiLine=True, escape='"')\
            .withColumn("TotalCharges", col("TotalCharges").cast('double'))\
            .na.drop(how='any')

# Separate features and ground-truth
features_df = telco_df.select(primary_key, *features)
response_df = telco_df.select(primary_key, response)

# Train a sklearn Decision Tree Classification model
# Convert data to pandas dataframes
X_train_pdf = features_df.drop(primary_key).toPandas()
Y_train_pdf = response_df.drop(primary_key).toPandas()

for col in X_train_pdf.select_dtypes("int32"):
    X_train_pdf[col] = X_train_pdf[col].astype("double")
# -

print(X_train_pdf.info())

# ## Model Preparation
#
# **Note:** This section is not the main focus of this course. We are just repeating the model development and registration process here.

#
# ### Setup Model Registery with UC
#
# Before we start model deployment, we need to fit and register a model. In this demo, **we will log models to Unity Catalog**, which means first we need to setup the **MLflow Model Registry URI**.

# +
import mlflow

# Point to UC model registry
mlflow.set_registry_uri("databricks-uc")
client = mlflow.MlflowClient()


def get_latest_model_version(model_name):
    """Helper function to get latest model version"""
    model_version_infos = client.search_model_versions("name = '%s'" % model_name)
    return max([model_version_info.version for model_version_info in model_version_infos])


# -

# ### Fit and Register a Model with UC

# +
from sklearn.tree import DecisionTreeClassifier
from mlflow.models import infer_signature

# Use 3-level namespace for model name
model_name = f"{DA.catalog_name}.{DA.schema_name}.ml_model" 

# model to use for classification
clf = DecisionTreeClassifier(max_depth=4, random_state=10)

with mlflow.start_run(run_name="Model-Deployment demo") as mlflow_run:

    # Enable automatic logging of input samples, metrics, parameters, and models
    mlflow.sklearn.autolog(
        log_input_examples=True,
        log_models=False,
        log_post_training_metrics=True,
        silent=True)
    
    clf.fit(X_train_pdf, Y_train_pdf)

    # Log model and push to registry
    signature = infer_signature(X_train_pdf, Y_train_pdf)
    mlflow.sklearn.log_model(
        clf,
        artifact_path="decision_tree",
        signature=signature,
        registered_model_name=model_name
    )

    # Set model alias
    client.set_registered_model_alias(model_name, "DLT", get_latest_model_version(model_name))
# -

# ## Configure Pipeline to Run Batch Inference
#
# Now that our model is registered and ready, we can move on the most important part; using the model for inference inside a pipeline. 
#
# **Note: The DLT pipeline is already defined in `3.1.b` notebook.**
#
# **Note: If you want to learn more about DLT please check out `Data Engineering with Databricks (Data Pipeline with Delta Live Tables).**
#

# ### Config Variables
#
# While defining the DLT pipeline, you will need to use the following variables. Run the code block below first. Then, use the output in the next section while creating the pipeline.
#

print(f"mlpipeline.bronze_dataset_path: {dataset_p_telco}")
print(f"mlpipeline.model_name: {model_name}")

# ### Create the DLT Pipeline
#
# To create a pipeline, follow these steps:
#
# 1. Go to **Delta Live Tables** from the left menu.
# 1. Click **Create Pipeline**.
# 1. For `Pipeline name` enter **Demo3.1-Pipeline-[Yourname]**. Make sure the pipeline name is unique.
# 1. For `Pipeline mode` select **Triggered**.
# 1. For `Paths` navigate to and select the notebook **3.1.b - Inference Pipeline**, in the same folder as this notebook.
# 1. For `Destination`:
#     * Select **Unity Catalog**.
#     * For `Catalog` and `Target schema`, select the catalog and schema that is created for you in the beginning of this notebook.
# 1. For `Compute`:
#     * Choose **DBAcademy DLT-UC** for the `Cluster policy`.
#     * Choose **Fixed size** for `Cluster mode`.
#     * Specify **1** for `Workers`.
# 1. For **Advanced** section, add these two configurations using the values from previous cell's output. Add the keys and values directly (no quotes needed).
#     * `mlpipeline.bronze_dataset_path`
#     * `mlpipeline.model_name`

# ### Start the DLT Pipeline
#
# Initiate the first update to your pipeline by clicking **Start**.

#
# ## Clean up Classroom
#
# Run the following cell to remove lessons-specific assets created during this lesson.

DA.cleanup()

# ## Conclusion
#
# In this demonstration, we walked through the sequential process of training, registering, and deploying a model within a pipeline. Following the standard procedure of fitting and registering the model, we then established a Delta Live Tables pipeline. This pipeline not only ingests data from a source file but also implements necessary data transformations, culminating in the utilization of the registered model as the final step in the pipeline. While your specific project requirements may vary, this example illustrates how to set up and integrate a model for inference within the Delta Live Tables pipeline.

#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
