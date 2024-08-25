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
#
# # Deploying an LLM Chain to Databricks Model Serving
#
# **In this demo, we will focus on deploying and querying GenAI models in realtime.**
#
# Deployment is a key part of operationalizing our LLM-based applications. We will explore deployment options within Databricks and demonstrate how to achieve each one.
#
# **Learning Objectives:**
#
# *By the end of this demo, you will be able to:*
#
# * Determine the right deployment strategy for your use case.
# * Deploy a custom RAG chain to a Databricks Model Serving endpoint.

# %% [markdown]
# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **14.3.x-cpu-ml-scala2.12**
#

# %% [markdown]
# Before starting the demo, **open & run the provided [00-Build-Model]($../00-Build-Model)** script at begining of class.
#
# **Note:** This script sets up a RAG applications, including a Databricks Vector Search and Vector Search Index, and it can take ~1 hour to complete at the moment. If the Vector Search and accompanying index are already created in your workspace, they will be used.

# %% [markdown]
#
# ## Classroom Setup
#
# Install required libraries.

# %%
# %pip install -U --quiet databricks-sdk==0.28.0 mlflow==2.12.1

dbutils.library.restartPython()

# %% [markdown]
# Before starting the demo, run the provided classroom setup script.

# %%
# %run ../Includes/Classroom-Setup-02

# %% [markdown]
# **Other Conventions:**
#
# Throughout this demo, we'll refer to the object `DA`. This object, provided by Databricks Academy, contains variables such as your username, catalog name, schema name, working directory, and dataset locations. Run the code block below to view these details:

# %%
print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")
print(f"Dataset Location:  {DA.paths.datasets}")

# %% [markdown]
# ## Demo Overview
#
# In this demo, we will walk through basic real-time deployment capabilities in Databricks. Model Serving allows us to deploy models and query it using various methods. 
#
# In this demo, we'll discuss this in the following steps:
#
# 1. Prepare a model to be deployed.
#
# 1. Deploy the registered model to a Databricks Model Serving endpoint.
#
# 1. Query the endpoint using various methods such as `python sdk` and `mlflow deployments`.

# %% [markdown]
# ## Model Preparation
#
# When we do this, we need to first to create our model.
#
# We have created a RAG model as a part of the set up of this lesson and have logged it in Unity Catalog for governance purposes and ease of deployment to Model Serving.
#
# It's here: **`genai_shared_catalog.default.rag_app`**.

# %%
import mlflow
from mlflow import MlflowClient

schema_name = f'ws_{spark.conf.get("spark.databricks.clusterUsageTags.clusterOwnerOrgId")}'

model_name = f"genai_shared_catalog.{schema_name}.rag_app"

# Point to UC registry
mlflow.set_registry_uri("databricks-uc")

def get_latest_model_version(model_name_in:str = None):
    """
    Get latest version of registered model
    """
    client = MlflowClient()
    model_version_infos = client.search_model_versions("name = '%s'" % model_name_in)
    if model_version_infos:
      return max([model_version_info.version for model_version_info in model_version_infos])
    else:
      return None


# %%
latest_model_version = get_latest_model_version(model_name)

if latest_model_version:
  print(f"Model created and logged to: {model_name}/{latest_model_version}")
else:
  raise(BaseException("Error: Model not created, verify if 00-Build-Model script ran successfully!"))

# %% [markdown]
# ## Deploy a Custom Model to Model Serving
#
# Deploying custom models once they're in Unity Catalog is similar to the workflow we demonstrated for external models once they're in Unity Catalog.

# %% [markdown]
# ### Pre-Requisite: Set up Secrets
#
# To secure access to the serving endpoint, we need set up a couple of secrets for the host (workspace URL) and a personal access token.
#
# Secrets can be set up using the Databricks CLI with the following commands:
#
# <br>
#
# ```
# databricks secrets create-scope <scope-name>
# databricks secrets put-secret --json '{
#   "scope": "<scope-name>",
#   "key": "<key-name>",    
#   "string_value": "<value>"
# }' 
# ```
#
# So in our case, we've run:
#
# <br>
#
# ```
# databricks secrets create-scope <scope-name>
# databricks secrets put-secret --json '{
#   "scope": "genai_training",
#   "key": "depl_demo_host",    
#   "string_value": "<host-name>"
# }'
# databricks secrets put-secret --json '{
#   "scope": "genai_training",
#   "key": "depl_demo_token",    
#   "string_value": "<token_value>"
# }' 
# ```
#
# Once this is set up, we will load the values into variables for the notebook using the Secrets utility in Databricks.

# %% [markdown]
# ### Deploy model using `databricks-sdk` API
#
# In the notebook we will use the API to create the endpoint and serving the model.
#
# **Note :** You could also simply use the UI for this task.
#
# **⏰ Expected deployment time: ~10 mins**

# %%
from databricks.sdk.service.serving import EndpointCoreConfigInput

# Configure the endpoint
endpoint_config_dict = {
    "served_models": [
        {
            "model_name": model_name,
            "model_version": latest_model_version,
            "scale_to_zero_enabled": True,
            "workload_size": "Small",
            "environment_vars": {
                # "DATABRICKS_TOKEN": "{{secrets/genai_training/depl_demo_token}}",
                # "DATABRICKS_HOST": "{{secrets/genai_training/depl_demo_host}}", 
                "DATABRICKS_TOKEN": "{{{{secrets/{0}/depl_demo_token}}}}".format(DA.scope_name),
                "DATABRICKS_HOST": "{{{{secrets/{0}/depl_demo_host}}}}".format(DA.scope_name),
                #"DATABRICKS_TOKEN": token,
                #"DATABRICKS_HOST": host,  
            },
        },
    ],
    "auto_capture_config":{
        "catalog_name": DA.catalog_name,
        "schema_name": DA.schema_name,
        "table_name_prefix": "rag_app_realtime"
    }
}

endpoint_config = EndpointCoreConfigInput.from_dict(endpoint_config_dict)

# %% [markdown]
# **Important:** Please note the syntax setup for the authentication above. Rather than passing the secret variables directly, we follow syntax requirements **&lcub;&lcub;secrets/&lt;scope&gt;/&lt;key-name&gt;&rcub;&rcub;** so that the endpoint will look up the secrets in real-time rather than automatically configure and expose static values.

# %%
from databricks.sdk import WorkspaceClient


# Initiate the workspace client
w = WorkspaceClient()
serving_endpoint_name = f"{DA.unique_name('_')}_endpoint"

# Get endpoint if it exists
existing_endpoint = next(
    (e for e in w.serving_endpoints.list() if e.name == serving_endpoint_name), None
)

db_host = dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().get("browserHostName").value()
serving_endpoint_url = f"{db_host}/ml/endpoints/{serving_endpoint_name}"

# If endpoint doesn't exist, create it
if existing_endpoint == None:
    print(f"Creating the endpoint {serving_endpoint_url}, this will take a few minutes to package and deploy the endpoint...")
    w.serving_endpoints.create_and_wait(name=serving_endpoint_name, config=endpoint_config)

# If endpoint does exist, update it to serve the new version
else:
    print(f"Updating the endpoint {serving_endpoint_url} to version {latest_model_version}, this will take a few minutes to package and deploy the endpoint...")
    w.serving_endpoints.update_config_and_wait(served_models=endpoint_config.served_models, name=serving_endpoint_name)

displayHTML(f'Your Model Endpoint Serving is now available. Open the <a href="/ml/endpoints/{serving_endpoint_name}">Model Serving Endpoint page</a> for more details.')

# %% [markdown]
# The model could have also been deployed programmatically using mlflow's [deploy_client](add ref)
#
# ```
#
# from mlflow.deployments import get_deploy_client
#
#
# deploy_client = get_deploy_client("databricks")
# endpoint = deploy_client.create_endpoint(
#     name=serving_endpoint_name,
#     config=endpoint_config
# )
# ```

# %% [markdown]
# ### (Method 2) - Create Inference Table via Model Serving UI
#
#
# If an endpoint is already up and running, we can tell if an inference table is not already set up by navigating to the Model Serving endpoint page and view the inference table field.
#
# To set up this inference table manually, we'll follow the below steps:
#
# 1. Go to [Serving](/ml/endpoints).
#
# 1. Find the endpoint you created and click the **Edit endpoint** button on the endpoint page. 
#
# 1. Expand the **Inference tables** section.
#
# 1. Check the **Enable inference tables** box.
#
# 1. Enter the catalog, schema and table information for the inference table.
#
# <br>
#
# <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/genai/genai-as-04-realtime-inference.png"  width="=100%">
#
# **Note:** To set up an inference table, you must configure your endpoint using a Databricks Secret.
#

# %% [markdown]
# ## Perform Inference on the Model
#
# Next, we will want to perform inference using the model – that is, provide input and return output.
#
# We'll start with a simple example of a single input:

# %%
question = "What is PPO?"

# %% [markdown]
# ### Inference width SDK

# %%
answer = w.serving_endpoints.query(serving_endpoint_name, inputs=[{"query": question}])
print(answer.predictions)

# %% [markdown]
# ### Inference with MLflow Deployments

# %%
from mlflow.deployments import get_deploy_client

deploy_client = get_deploy_client("databricks")
response = deploy_client.predict(
  endpoint=serving_endpoint_name,
  inputs={"inputs" : [{"query": question}]}
)
print(response.predictions)

# %% [markdown]
# ## View the Inference Table
#
# Once the table is created and the endpoint is hit couple times, we can view the table in the Catalog Explorer to inspect the saved query data.
#
# To view the inference table:
#
# 1. Go to **[Catalog](explore/data)**.
#
# 1. Select the catalog and schema you entered while configuring the inference table in previous step.
#
# 1. Select the inference table and view the sample data. 
#
# **🚨 Note:** It might take couple minutes to see the monitoring data.
#
# <br/>
#
# <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/genai/genai-as-04-realtime-inference-table.png" width="100%">
#
# <br/>
#
# **💡 Note:** We can also view the data directly by querying the table. This can be useful if we're wanting to work the data into our application in some way (e.g. using human feedback to inform testing strategy, etc.).
#
# **Question:** What data do you see in the inference table?

# %% [markdown]
#
# ## Clean up Classroom
#
# Run the following cell to remove lessons-specific assets created during this lesson.

# %%
DA.cleanup()

# %% [markdown]
#
# ## Conclusion
#
# In this demo, we demonstrated how to deploy an RAG pipeline in real-time using Databricks Model Serving. The model was created and registered in the Model Registry, making it ready for use. First, we deployed the model to a Model Serving endpoint using the SDK. Then, we configured the endpoint and enabled the inference table. Finally, we showed how to query the endpoint in real-time using the SDK and MLflow deployments.

# %%

# %% [markdown]
#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
