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
# # Real-time Deployment with Model Serving
#
# In this demo, we will focus on real-time deployment of machine learning models. ML models can be deployed using various technologies. Databricks' Model Serving is an easy to use serverless infrastructure for serving the models in real-time.
#
# First, we will fit a model **without using a feature store**. Then, we will serve the model via Model Serving. Model serving **supports both the API and the UI**. To demonstrate both methods, we will, first, serve the model using the UI and then server the model using **Databricks' Python SDK**.
#
# In the second section, we will fit a model **with feature store and we will use online features during the inference.** For online features, **Databricks' Online Tables** can be used.
#
# **Learning Objectives:**
#
# *By the end of this demo, you will be able to;*
#
# * Implement a real-time deployment REST API using Model Serving.
#
# * Serve multiple model versions to a Serverless Model Serving endpoint.
#
# * Set up an A/B testing endpoint by splitting the traffic.
#
#

# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **13.3.x-cpu-ml-scala2.12**
#
# * Online Tables must be enabled for the workspace.

#
# ## Classroom Setup
#
# Before starting the demo, run the provided classroom setup script. This script will define configuration variables necessary for the demo. Execute the following cell:

# +
# %pip install databricks-sdk --upgrade

dbutils.library.restartPython()
# -

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
# For this demonstration, we will use a fictional dataset from a Telecom Company, which includes customer information. This dataset encompasses **customer demographics**, including internet subscription details such as subscription plans, monthly charges and payment methods.
#
# After load the dataset, we will perform simple **data cleaning and feature selection**. 
#
# In the final step, we will split the dataset to **features** and **response** sets.

# +
from pyspark.sql.functions import col

# Dataset path
dataset_p_telco = f"{DA.paths.datasets}/telco/telco-customer-churn.csv"

# Dataset specs
primary_key = "customerID"
response = "Churn"
features = ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"] # Keeping numerical only for simplicity and demo purposes


# Read dataset (and drop nan)
# Convert all fields to double for spark compatibility
telco_df = spark.read.csv(dataset_p_telco, inferSchema=True, header=True, multiLine=True, escape='"')\
            .withColumn("TotalCharges", col("TotalCharges").cast('double'))\
            .withColumn("SeniorCitizen", col("SeniorCitizen").cast('double'))\
            .withColumn("Tenure", col("tenure").cast('double'))\
            .na.drop(how='any')

# Separate features and ground-truth
features_df = telco_df.select(primary_key, *features)
response_df = telco_df.select(primary_key, response)

# Covert data to pandas dataframes
X_train_pdf = features_df.drop(primary_key).toPandas()
Y_train_pdf = response_df.drop(primary_key).toPandas()
# -

#
# ## Fit and Register Models
#
# Before we start model deployment process, we will **fit and register two models**. These models are called **"Champion"** and **"Challenger"** and they will be served later on using Databricks Model Serving.

# ### Setup Model Registry with UC
#
# Before we start model deployment, we need to fit and register a model. In this demo, **we will log models to Unity Catalog**, which means first we need to setup the **MLflow Model Registry URI**.

# [mlflow.set_registry_uri](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.set_registry_uri)
#
# [MlflowClient](https://mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient)

# +
import mlflow

# Point to UC model registry
mlflow.set_registry_uri("databricks-uc")
client = mlflow.MlflowClient()
# -

# ### Fit and Register a Model with UC

# NOTE: I need to better understand the difference between `mlflow.sklearn.log_model` and `FeatureingEngineeringClient.log_model`. Note that when the query call is used for testing, the primary difference is that the Feature Table/Store created using `FeatureEngineeringClient` allows for efficient searching of the records with only the id and without having to provide the entire dataframe to the query as when we log with `mlflow.sklearn.log_model`. I imagine id-only querying allows for efficient savings when performing inference from a front-end API call.

# ### Mlflow
# [mlflow.start_run](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.start_run)
#
# [mlflow.search_model_versions](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.search_model_versions)
#
# [mlflow.sklearn.autolog](https://mlflow.org/docs/latest/python_api/mlflow.sklearn.html#mlflow.sklearn.autolog)
#
# [mlflow.MlflowClient.set_registered_model_alias](https://mlflow.org/docs/latest/python_api/mlflow.client.html#mlflow.client.MlflowClient.set_registered_model_alias)
#
# [mlflow.models.infer_signature](https://mlflow.org/docs/latest/python_api/mlflow.models.html#mlflow.models.infer_signature)
#
# # %md
# [mlflow.sklearn.save_model](https://mlflow.org/docs/latest/python_api/mlflow.sklearn.html#mlflow.sklearn.save_model)
#
# ### Databricks
# [FeatureEngineeringClient](https://api-docs.databricks.com/python/feature-engineering/latest/feature_engineering.client.html) - Can search for `FeatureEngineeringClient.log_model` from this link as well.
#

# +
import time
import warnings
from mlflow.types.utils import _infer_schema
from mlflow.models import infer_signature
from sklearn.tree import DecisionTreeClassifier
from databricks.feature_engineering import FeatureEngineeringClient

model_name = f"{DA.catalog_name}.{DA.schema_name}.ml_model" # Use 3-level namespace

def get_latest_model_version(model_name):
    """Helper function to get latest model version"""
    model_version_infos = client.search_model_versions("name = '%s'" % model_name)
    return max([model_version_info.version for model_version_info in model_version_infos])

def fit_and_register_model(X, Y, model_name_=model_name, random_state_=42, model_alias=None, log_with_fs=False, training_set_spec_=None):
    """Helper function to train and register a decision tree model"""

    clf = DecisionTreeClassifier(random_state=random_state_)
    with mlflow.start_run(run_name="Demo4_1-Real-Time-Deployment") as mlflow_run:

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
                model=clf,
                artifact_path="decision_tree",
                flavor=mlflow.sklearn,
                training_set=training_set_spec_,
                signature = signature,
                #output_schema = output_schema, not in the documentation... changed to signature by inferring with mlflow documentation save_model
                registered_model_name=model_name_
            )
        
        else:
            mlflow.sklearn.log_model(
                clf,
                artifact_path="decision_tree",
                signature=signature,
                registered_model_name=model_name_
            )

        # Set model alias
        if model_alias:
            time.sleep(20) # Wait 20secs for model version to be created
            client.set_registered_model_alias(model_name_, model_alias, get_latest_model_version(model_name_))

    return clf


# -

model_champion   = fit_and_register_model(X_train_pdf, Y_train_pdf, model_name, 42, "Champion")

model_challenger = fit_and_register_model(X_train_pdf, Y_train_pdf, model_name, 10, "Challenger")

#
# ## Real-time A/B Testing Deployment with Model Serving
#
# Let's serve the two models we logged in the previous step using Model Serving. Model Serving supports endpoint management via the UI and the API. 
#
# Below you will find instructions for using the UI and it is simpler method compared to the API. **In this demo, we will use the API to configure and create the endpoint**.
#
# **Both the UI and the API support querying created endpoints in real-time**. We will use the API to query the endpoint using a test-set.

# ### Option 1: Serve model(s) using UI
#
# After registering the (new version(s) of the) model to the model registry. To provision a serving endpoint via UI, follow the steps below.
#
# 1. In the left sidebar, click **Serving**.
#
# 2. To create a new serving endpoint, click **Create serving endpoint**.   
#   
#     a. In the **Name** field, type a name for the endpoint.  
#   
#     b. Click in the **Entity** field. A dialog appears. Select **Unity catalog model**, and then select the catalog, schema, and model from the drop-down menus.  
#   
#     c. In the **Version** drop-down menu, select the version of the model to use.  
#   
#     d. Click **Confirm**.  
#   
#     e. In the **Compute Scale-out** drop-down, select Small, Medium, or Large. If you want to use GPU serving, select a GPU type from the **Compute type** drop-down menu.
#   
#     f. *[OPTIONAL]* to deploy another model (e.g. for A/B testing) click on **+Add Served Entity** and fill the above mentioned details.
#   
#     g. Click **Create**. The endpoint page opens and the endpoint creation process starts.   
#   
# See the Databricks documentation for details ([AWS](https://docs.databricks.com/machine-learning/model-serving/create-manage-serving-endpoints.html#ui-workflow)|[Azure](https://learn.microsoft.com/azure/databricks/machine-learning/model-serving/create-manage-serving-endpoints#--ui-workflow)).

# ### Option 2: Serve Model(s) Using the *Databricks Python SDK*
#

# #### Get Models to Serve
#
# We will serve two models, therefore, we will get model version of the two models (**Champion** and **Challenger**) that we registered in the previous step.

model_version_champion = client.get_model_version_by_alias(name=model_name, alias="Champion").version # Get champion version
model_version_challenger = client.get_model_version_by_alias(name=model_name, alias="Challenger").version # Get challenger version

# #### Configure and Create Serving Endpoint

# [CreateServingEndpoint](https://databricks-sdk-py.readthedocs.io/en/latest/dbdataclasses/serving.html#databricks.sdk.service.serving.CreateServingEndpoint)
#
# [EndpointCoreConfigInput](https://databricks-sdk-py.readthedocs.io/en/latest/dbdataclasses/serving.html#databricks.sdk.service.serving.EndpointCoreConfigInput)
#
# [ServedEntityInput](https://databricks-sdk-py.readthedocs.io/en/latest/dbdataclasses/serving.html#databricks.sdk.service.serving.ServedEntityInput) - NOTE: `served_models` used below is deprecated... should use `served_entities` - See deployment with online features below for alternative

# +
from databricks.sdk.service.serving import EndpointCoreConfigInput


# Parse model name from UC namespace
served_model_name =  model_name.split('.')[-1] # ml_model in this case

endpoint_config_dict = {
    "served_models": [
        {
            "model_name": model_name,
            "model_version": model_version_champion,
            "scale_to_zero_enabled": True,
            "workload_size": "Small"
        },
        {
            "model_name": model_name,
            "model_version": model_version_challenger,
            "scale_to_zero_enabled": True,
            "workload_size": "Small"
        },
    ],
    "traffic_config": {
        "routes": [
            {"served_model_name": f"{served_model_name}-{model_version_champion}", "traffic_percentage": 50},
            {"served_model_name": f"{served_model_name}-{model_version_challenger}", "traffic_percentage": 50},
        ]
    },
    "auto_capture_config":{
        "catalog_name": DA.catalog_name,
        "schema_name": DA.schema_name,
        "table_name_prefix": "db_academy"
    }
}


endpoint_config = EndpointCoreConfigInput.from_dict(endpoint_config_dict)

# +
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import EndpointTag


# Create/Update endpoint and deploy model+version
w = WorkspaceClient()
# -

# [EndpointTag](https://databricks-sdk-py.readthedocs.io/en/latest/dbdataclasses/serving.html#databricks.sdk.service.serving.EndpointTag)
#
# [ServingEndpointsAPI](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/serving/serving_endpoints.html#databricks.sdk.service.serving.ServingEndpointsAPI)
#
# [ServingEndpointsAPI.create_and_wait](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/serving/serving_endpoints.html#databricks.sdk.service.serving.ServingEndpointsAPI.create_and_wait)

# +
# Use a helper funciton to produce a unique endpoint name... required to ensure we do not have any conflicts
endpoint_name = f"ML_AS_03_Demo4_{DA.unique_name('_')}"

try:
  w.serving_endpoints.create_and_wait(
    name=endpoint_name,
    config=endpoint_config,
    tags=[EndpointTag.from_dict({"key": "db_academy", "value": "serve_model_example"})]
  )
  
  print(f"Creating endpoint {endpoint_name} with models {model_name} versions {model_version_champion} & {model_version_challenger}")

except Exception as e:
  if "already exists" in e.args[0]:
    print(f"Endpoint with name {endpoint_name} already exists")

  else:
    raise(e)
# -

# #### Verify Endpoint Creation
#
# Let's verify that the endpoint is created and ready to be used for inference.

# [EndpointState](https://databricks-sdk-py.readthedocs.io/en/latest/dbdataclasses/serving.html#databricks.sdk.service.serving.EndpointState)
#
# [ServingEndpointDetailed](https://databricks-sdk-py.readthedocs.io/en/latest/dbdataclasses/serving.html#databricks.sdk.service.serving.ServingEndpointDetailed)
#
# [ServingEndpointsAPI.wait_get_serving_endpoint_not_updating](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/serving/serving_endpoints.html#databricks.sdk.service.serving.ServingEndpointsAPI.wait_get_serving_endpoint_not_updating)

# +
endpoint = w.serving_endpoints.wait_get_serving_endpoint_not_updating(endpoint_name)

assert endpoint.state.config_update.value == "NOT_UPDATING" and endpoint.state.ready.value == "READY" , "Endpoint not ready or failed"
# -

# #### Query the Endpoint
#
# Here we will use a very simple `test-sample` to use for inference. In a real-life scenario, you would typically load this set from a table or a streaming pipeline.

# Hard-code test-sample
dataframe_records = [
    {"SeniorCitizen": 0, "tenure":12, "MonthlyCharges":65, "TotalCharges":800},
    {"SeniorCitizen": 1, "tenure":24, "MonthlyCharges":40, "TotalCharges":500}
]

# [ServingEndpointsAPI.query](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/serving/serving_endpoints.html#databricks.sdk.service.serving.ServingEndpointsAPI.query)
#
# [QueryEndpointResposne](https://databricks-sdk-py.readthedocs.io/en/latest/dbdataclasses/serving.html#databricks.sdk.service.serving.QueryEndpointResponse)

print("Inference results:")
query_response = w.serving_endpoints.query(name=endpoint_name, dataframe_records=dataframe_records)
print(query_response.predictions)

#
# ## Real-time Deployment with Online Features
#
# In the previous section we deployed a model without using feature tables. In this section **we will register and deploy a model for real-time inference with feature tables.** First, we will **deploy a model with online store integration** and then we will demonstrate **inference with online store integration**.

# ### Fit and Log the Model with Feature Table

# +
from databricks.feature_engineering import FeatureLookup, FeatureEngineeringClient


feature_table_name = f"{DA.catalog_name}.{DA.schema_name}.features"
fe = FeatureEngineeringClient()

# Create feature table
fe.create_table(
    name=feature_table_name,
    df=features_df,
    primary_keys=[primary_key], 
    description="Example feature table"
)

# Create training set based on feature lookup
fl_handle = FeatureLookup(
    table_name=feature_table_name,
    lookup_key=[primary_key] # used to join with the dataframe passed to create_training_set
)

# Performs a join on the feature table and the dataframe passed to create_training_set
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

model_fe = fit_and_register_model(X_train_pdf2, Y_train_pdf2, model_name, 20, log_with_fs=True, training_set_spec_=training_set_spec)

# ### Set Up Databricks Online Tables
#
# In this section, we will create an online table to serve feature table for real-time inference. Databricks Online Tables can be created and managed via the UI and the SDK. While we provided instructions for both of these methods, you can pick one option for creating the table.

#
#
# #### OPTION 1: Create Online Table via the UI
#
# You create an online table from the Catalog Explorer. The steps are described below. For more details, see the Databricks documentation ([AWS](https://docs.databricks.com/en/machine-learning/feature-store/online-tables.html#create)|[Azure](https://learn.microsoft.com/azure/databricks/machine-learning/feature-store/online-tables#create)). For information about required permissions, see Permissions ([AWS](https://docs.databricks.com/en/machine-learning/feature-store/online-tables.html#user-permissions)|[Azure](https://learn.microsoft.com/azure/databricks/machine-learning/feature-store/online-tables#user-permissions)).
#
#
# In **Catalog Explorer**, navigate to the source table that you want to sync to an online table. 
#
# From the kebab menu, select **Create online table**.
#
# * Use the selectors in the dialog to configure the online table.
#   
#   * `Name`: Name to use for the online table in Unity Catalog.
#   
#   * `Primary Key`: Column(s) in the source table to use as primary key(s) in the online table.
#   
#   * Timeseries Key: (Optional). Column in the source table to use as timeseries key. When specified, the online table includes only the row with the latest timeseries key value for each primary key.
#   
#   * `Sync mode`:  Select **`Snapshot`** for Sync mode. Please refer to the documentation for more details about available options.
#   
#   * When you are done, click Confirm. The online table page appears.
#
# The new online table is created under the catalog, schema, and name specified in the creation dialog. In Catalog Explorer, the online table is indicated by online table icon.

# #### OPTION 2: Use the Databricks SDK 
#
# The first option for creating an online table the UI. The other alternative is the Databricks' [python-sdk](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/catalog/online_tables.html). Let's  first define the table specifications, then create the table.
#
# **🚨 Note:** The workspace must be enabled for using the SDK for creating and managing online tables. You can run following code blocks in your workspace is enabled for this feature.

#
# **Step1: Define table configuration:**
#
# [OnlineTableSpec](https://databricks-sdk-py.readthedocs.io/en/latest/dbdataclasses/catalog.html#databricks.sdk.service.catalog.OnlineTableSpec)

# +
from databricks.sdk.service.catalog import OnlineTableSpec

online_table_spec = OnlineTableSpec().from_dict({
    "source_table_full_name": feature_table_name,
    "primary_key_columns": [primary_key],
    "perform_full_copy": True,
    "run_triggered": True,
})
# -

# **Step2: Create the table**
#
# [Workspace APIs - Unity Catalog](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/catalog/index.html)
#
# [OnlineTablesAPI.create](https://databricks-sdk-py.readthedocs.io/en/latest/workspace/catalog/online_tables.html#databricks.sdk.service.catalog.OnlineTablesAPI.create)

# +
from databricks.sdk.service.catalog import OnlineTablesAPI

# Create online table
w = WorkspaceClient()
online_table = w.online_tables.create(
    name=f"{DA.catalog_name}.{DA.schema_name}.online_features",
    spec=online_table_spec
)
# -

# ### Deploy the Model with Online Features
#
# Now that we have a model registered with feature table and we created an online feature table, we can deploy the model with Model Serving and use the online table during inference.
#
# **💡 Note:** The Model Serving **endpoint configuration and creation process is the same for serving models with or without feature tables**. The registered model metadata handles feature lookup during inference.

# +
fs_model_version = get_latest_model_version(model_name)

fs_endpoint_config_dict = {
    "served_entities": [
        {
            "entity_name": model_name,
            "entity_version": fs_model_version,
            "scale_to_zero_enabled": True,
            "workload_size": "Small"
        }
    ]
}

fs_endpoint_config = EndpointCoreConfigInput.from_dict(fs_endpoint_config_dict)

fs_endpoint_name = f"ML_AS_03_Demo4_FS_{DA.unique_name('_')}"

try:
  w.serving_endpoints.create_and_wait(
    name=fs_endpoint_name,
    config=fs_endpoint_config,
    tags=[EndpointTag.from_dict({"key": "db_academy", "value": "serve_fs_model_example"})]
  )
  
  print(f"Creating endpoint {fs_endpoint_name} with models {model_name} versions {fs_model_version}")

except Exception as e:
  if "already exists" in e.args[0]:
    print(f"Endpoint with name {fs_endpoint_name} already exists")

  else:
    raise(e)
# -

# Hard-code test-sample
dataframe_records_lookups_only = [
    {"customerID": "0002-ORFBO"},
    {"customerID": "0003-MKNFE"}
]

print("FS Inference results:")
query_response = w.serving_endpoints.query(name=fs_endpoint_name, dataframe_records=dataframe_records_lookups_only)
print(query_response.predictions)

#
# ## Clean up Classroom
#
# Run the following cell to remove lessons-specific assets created during this lesson.

DA.cleanup()

#
# ## Conclusion
#
# In this demo, we covered how to serve ML models in real-time using Databricks Model Serving. In the first part, we demonstrated how to serve models without feature store integration. Furthermore, we showed how to deploy two models on the same endpoint to conduct an A/B testing scenario. In the second section of the demo, we deployed a model with feature store integration using Databricks Online Tables. Additionally, we demonstrated how to use the endpoint for inference with Online Tables integration.

#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
