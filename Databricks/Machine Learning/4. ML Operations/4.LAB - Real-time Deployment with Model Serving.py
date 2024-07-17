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
# # LAB - Real-time Deployment with Model Serving
#
# In this lab, you will deploy ML models with Databricks Model Serving **with and without a feature table**. This lab includes **two** sections.
#
# In the first section, you will deploy a model for real-time inference with Model Serving's **UI**. This section will demonstrate the most basic and simple way of deploying models with Model Serving. 
#
# For the second section, you will deploy a model with with an **online feature table using the API**. 
#
# For both sections, data preparation, model fitting and model registration are already done for you! You just need to focus on the deployment part.
#
# **Lab Outline:**
#
# * Simple real-time deployment
#   
#   - **Task 1:** Serve the model using the UI
#   
#   - **Task 2:** Query the endpoint
#
# * Real-time deployment with Online Features
#
#   - **Task 3**: Create an online feature table
#
#   - **Task 4:** Deploy a model with the online feature table
#
#   - **Task 5:** Query the endpoint 
#
#

# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **13.3.x-cpu-ml-scala2.12**

#
# ## Classroom Setup
#
# Before starting the demo, run the provided classroom setup scripts. 
#
# **📌 Note:** In this lab you will using the Databricks SDK to create Model Serving endpoint. Therefore, you will need to run the next code block to **install `databricks-sdk`**. 
#
# Before starting the demo, run the provided classroom setup script. This script will define configuration variables necessary for the demo. Execute the following cell:

# +
# %pip install databricks-sdk --upgrade

dbutils.library.restartPython()
# -

#

# %run ../Includes/Classroom-Setup-01

# **Other Conventions:**
#
# Throughout this demo, we'll refer to the object `DA`. This object, provided by Databricks Academy, contains variables such as your username, catalog name, schema name, working directory, and dataset locations. Run the code block below to view these details:

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")
print(f"Dataset Location:  {DA.paths.datasets}")

# ## Data and Model Preparation
#
# Before you start the deployment process, you will need to fit and register a model. In this section, you will load dataset, fit a model and register it with UC.
#
# **Note:** All necessary code is provided, which means you don't need to complete anything in this section.

# ### Load Dataset

# +
from pyspark.sql.functions import col, monotonically_increasing_id

# dataset path
dataset_path = f"{DA.paths.datasets}/cdc-diabetes/diabetes_binary_5050split_BRFSS2015.csv"

df = spark.read.csv(dataset_path, inferSchema=True, header=True, multiLine=True, escape='"')\
    .na.drop(how='any')

df = df.withColumn("uniqueID", monotonically_increasing_id())   # Add unique_id column

# Dataset specs
primary_key = "uniqueID"
response = "Diabetes_binary"

# Separate features and ground-truth
features_df = df.drop(response)
response_df = df.select(primary_key, response)

# Convert data to pandas dataframes
X_train_pdf = features_df.drop(primary_key).toPandas()
Y_train_pdf = response_df.drop(primary_key).toPandas()
# -

# ### Setup Model Registery with UC
#
# Before we start model deployment, we need to fit and register a model. In this demo, **we will log models to Unity Catalog**, which means first we need to setup the **MLflow Model Registry URI**.

# +
import mlflow

# Point to UC model registry
mlflow.set_registry_uri("databricks-uc")
client = mlflow.MlflowClient()
# -

# ### Helper Class for Model Creation

# +
import time
import warnings
from mlflow.types.utils import _infer_schema
from mlflow.models import infer_signature
from sklearn.tree import DecisionTreeClassifier
from databricks.feature_engineering import FeatureEngineeringClient

model_name = f"{DA.catalog_name}.{DA.schema_name}.ml_diabetes_model" # Use 3-level namespace

def get_latest_model_version(model_name):
    """Helper function to get latest model version"""
    model_version_infos = client.search_model_versions("name = '%s'" % model_name)
    return max([model_version_info.version for model_version_info in model_version_infos])

def fit_and_register_model(X, Y, model_name_=model_name, random_state_=42, model_alias=None, log_with_fs=False, training_set_spec_=None):
    """Helper function to train and register a decision tree model"""

    clf = DecisionTreeClassifier(random_state=random_state_)
    with mlflow.start_run(run_name="LAB4-Real-Time-Deployment") as mlflow_run:

        # Enable automatic logging of input samples, metrics, parameters, and models
        mlflow.sklearn.autolog(
            log_input_examples=True,
            log_models=False,
            log_post_training_metrics=True,
            silent=True)
        
        clf.fit(X, Y)
        signature = infer_signature(X, Y)

        # Log model and push to registry
        if log_with_fs:
            # Infer output schema
            # NOTE: cannot find _infer_schema or output_schema in documentation... not in the documentation... changed to signature by inferring with mlflow documentation save_model
            # try:
            #     output_schema = _infer_schema(Y) # see not in log_model below... not sure if this needed... can't find it in the mlflow documentation
            # except Exception as e:
            #     warnings.warn(f"Could not infer model output schema: {e}")
            #     output_schema = None
            
            # Log using feature engineering client and push to registry
            fe = FeatureEngineeringClient()
            fe.log_model(
                model = clf,
                artifact_path = "decision_tree",
                flavor = mlflow.sklearn,
                training_set = training_set_spec_,
                signature=signature,
                #output_schema = output_schema, not in the documentation... changed to signature by inferring with mlflow documentation save_model
                registered_model_name = model_name_
            )
        
        else:
            example = X[:3]
            mlflow.sklearn.log_model(
                clf,
                artifact_path = "decision_tree",
                signature = signature,
                input_example = example,
                registered_model_name = model_name_
            )

        # Set model alias
        if model_alias:
            time.sleep(10) # Wait 10secs for model version to be created
            client.set_registered_model_alias(model_name_, model_alias, get_latest_model_version(model_name_))

    return clf


# -

# ### Fit and Register the Model
#
# Before we start model deployment process, we will **fit and register a model**. The model's alias will be set to `Production` and it will be served with Databricks Model Serving in the next step.

model = fit_and_register_model(X_train_pdf, Y_train_pdf, model_name, 42, "Production")

# ## Simple Real-time Model Deployment
#
# Now that the model is registered and ready for deployment, the next step is to create a serving endpoint with Model Serving and serve the model.

# ### Task 1: Serve the Model Using the UI
#
# Serve the **"Production"** model that we registered in the previous section using the following endpoint configuration.
#
# **Configuration:**
#
# * Name: `la4-1-diabetes-model`
#
# * Compute Size: `small` (CPU)
#
# * Autoscaling: `Scale to zero`
#
# * Tags: Define tags that might be meaningful for this deployment
#
#
# **💡 Note:** Endpoint creation will take sometime. Therefore, you can work on the next section  while the endpoint is created for you.

# ### Task 2: Query the Endpoint 
#
# Test the model deployment using the **Query endpoint** feature in browsers. Use the provided **Example request** payload to use the model for inference.

# ## Real-time Model Deployment with Online Store
#
# In this section you will deploy a model with a feature table using Databricks' Online Tables. Also, instead of using the UI for creating and configuring the serving endpoint, this time you will need to use the API. 
#
# Note that feature table creation code is already provided for you. You just need to focus on creating Online Tables and deploying the model along with the online feature table.

# ### Create Feature Table
#
# Let's create a feature table to store the features that will be use for training the model.

# +
from databricks.feature_engineering import FeatureLookup, FeatureEngineeringClient

feature_table_name = f"{DA.catalog_name}.{DA.schema_name}.diabetes_features"
fe = FeatureEngineeringClient()

# Create feature table
fe.create_table(
    name=feature_table_name,
    df=features_df,
    primary_keys=[primary_key],
    description="Diabetes features table"
)

# Create training set based on feature lookup
fl_handle = FeatureLookup(
    table_name=feature_table_name,
    lookup_key=[primary_key]
)

training_set_spec = fe.create_training_set(
    df=response_df,
    label=response,
    feature_lookups=[fl_handle],
    exclude_columns=[primary_key]
)

# Load training dataframe based on defined feature-lookup specification
training_df = training_set_spec.load_df()

# Convert data to pandas dataframes
X_train_pdf2 = training_df.drop(response).toPandas()
Y_train_pdf2 = training_df.select(response).toPandas()
# -

# ### Fit a Model with Feature Table

model_name_2 = f"{DA.catalog_name}.{DA.schema_name}.ml_diabetes_model_fe"
model_fe = fit_and_register_model(X_train_pdf2, Y_train_pdf2, model_name_2, 20, log_with_fs=True, training_set_spec_=training_set_spec)

# ### Task 3: Create a Databricks Online Table
#
# As we created the model and registered it with feature store, we will need to integrate the feature table for inference. For real-time inference, Model Serving will need to access features in real-time. 
#
# **Create an online feature table using following configurations:**
#
# * Table name: `diabetes_online_feature_table`
#
# * Sync mode: `Snapshot` - NOTE: Can't find this in the documentation fora feature table.

# +
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.catalog import OnlineTableSpec

online_table_spec = OnlineTableSpec().from_dict({
    "source_table_full_name": feature_table_name,
    "primary_key_columns": [primary_key],
    "perform_full_copy": True,
    "run_triggered": True,
})

# Create online table
w = WorkspaceClient()
online_table = w.online_tables.create(
    name=f"{DA.catalog_name}.{DA.schema_name}.diabetes_online_feature_table",
    spec=online_table_spec
)
# -

# ### Task 4: Deploy the Model with Online Store
#
# Create an endpoint with following configuration;
#
# * Autoscaling: `Scale-to-zero`
#
# * Compute size: `Small`
#
# **💡 Note:** Endpoint creation will take sometime. Be patient while the endpoint is created.

# +
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import EndpointCoreConfigInput, EndpointTag

# Create/Update endpoint and deploy model+version
w = WorkspaceClient()

# Get model version that will be served
fs_model_version = get_latest_model_version(model_name_2)

# Endpoint configuration
fs_endpoint_config_dict = {
   "served_entities": [
       {
          "entity_name": model_name_2,
          "entity_version": fs_model_version,
          "scale_to_zero_enabled": True,
          "workload_size": "Small"
       }
   ]
}
fs_endpoint_config = EndpointCoreConfigInput.from_dict(fs_endpoint_config_dict)


fs_endpoint_name = f"ML_AS_03_Lab4_FS_{DA.unique_name('_')}"
try:
   w.serving_endpoints.create_and_wait(
     name=fs_endpoint_name,
     config=fs_endpoint_config,
     tags=[EndpointTag.from_dict({"key": "db_academy", "value": "lab4_serve_fs_model"})]
   )
  
   print(f"Creating endpoint {fs_endpoint_name} with models {model_name} versions {fs_model_version}")

except Exception as e:
   if "already exists" in e.args[0]:
     print(f"Endpoint with name {fs_endpoint_name} already exists")
   else:
     raise(e)
# -

# ### Task 5: Query the Endpoint
#
# After the endpoint is created, it is time to test it. Use the following hard-coded test-sample to query the endpoint using the API.

# Hard-coded test-sample. Feel free to change the ids
dataframe_records_lookups_only = [
    {"uniqueID": "123"},
    {"uniqueID": "45678"}
]

fs_endpoint_name

# Query the serving endpoint with test-sample
query_response = w.serving_endpoints.query(name=fs_endpoint_name, dataframe_records=dataframe_records_lookups_only)
print(f"FS Inference results: {query_response.predictions}")

#
# ## Clean up Classroom
#
# Run the following cell to remove lessons-specific assets created during this lesson.

DA.cleanup()

#
# ## Conclusion
#
# Great job for completing this lab! In this lab, you completed two main tasks: deploying a model with Model Serving using both with and without feature store tables. In the first section of the lab, the main task was to deploy a model simply using the UI. The second section focused on registering a model with a feature table, creating an online feature table from an existing table, and serving a model with an online feature store. Additionally, for each of these methods, there was an endpoint query task to test the endpoint.

#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
