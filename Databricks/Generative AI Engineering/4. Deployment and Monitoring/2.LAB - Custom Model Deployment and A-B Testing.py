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
# # LAB: Custom Model Deployment and A/B Testing
#
# In this lab, you will learn how to deploy and serve a custom model using Databricks Model Serving. You will understand the steps involved in preparing, deploying, and querying a model endpoint in Databricks. This lab will focus on the practical aspects of deploying custom models and querying them for real-time inference.
#
#
# **Lab Outline:**
#
# *In this lab, you will need to complete the following tasks:*
#
# 1. **Task 1:** Get Model Version
# 1. **Task 2:** Deploy Model with SDK
# 1. **Task 3:** Configure A/B Testing Using the UI
# 1. **Task 4:** Query the Endpoint
# 1. **Task 5:** Inspect Inference Table

# %% [markdown]
#
# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **14.3.x-cpu-ml-scala2.12**

# %% [markdown]
#
# ## Classroom Setup
#
# Install required libraries.

# %%
# %pip install -U --quiet mlflow databricks-sdk

dbutils.library.restartPython()

# %% [markdown]
# Before starting the Lab, run the provided classroom setup script. This script will define configuration variables necessary for the lab. Execute the following cell:

# %%
# %run ../Includes/Classroom-Setup-02

# %% [markdown]
# **Other Conventions:**
#
# Throughout this lab, we'll refer to the object `DA`. This object, provided by Databricks Academy, contains variables such as your username, catalog name, schema name, working directory, and dataset locations. Run the code block below to view these details:

# %%
print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")
print(f"Dataset Location:  {DA.paths.datasets}")

# %% [markdown]
# ##Model Details
# The model is created with the **00-Model-Build** notebook. It's registered in Unity Catalog for governance purposes and ease of deployment to Model Serving.
#
# Model location: `genai_shared_catalog.ws_<xxxx>.rag_app`

# %%
model_name = f"genai_shared_catalog.{DA.schema_name_shared}.rag_app"
print(f"Model name: {model_name}")

# %% [markdown]
#
# ## Task 1: Get Model Version
#
# In this task, you will retrieve model details and version from the model registry. This will help you identify the latest version of your model for deployment.

# %%
import mlflow
from mlflow import MlflowClient

# Set the registry URI to Unity Catalog
mlflow.set_registry_uri("databricks-uc")

# Initialize the MLflow client
client = MlflowClient()

# Get the latest version number of the specified model
model_version_infos = client.<FILL_IN>
latest_model_version = <FILL_IN>

# Print the latest model version
<FILL_IN>

# %%
import mlflow
from mlflow import MlflowClient

# Set the registry URI to Unity Catalog
mlflow.set_registry_uri("databricks-uc")

# Initialize the MLflow client
client = MlflowClient()

# Get the latest version number of the specified model
model_version_infos = client.search_model_versions("name = '%s'" % model_name)
latest_model_version = max([model_version_info.version for model_version_info in model_version_infos])

# Print the latest model version
print(f"Latest model version: {latest_model_version}")

# %% [markdown]
# ## Task 2: Deploy Model with SDK
#
# In this task, you will deploy the model using the SDK and enable the inference table. This involves defining environment variables, configuring the endpoint, and setting up the inference table.
#
#

# %% [markdown]
# ###2.1: Set Up Secrets
#
#
# To secure access to the serving endpoint, set up secrets for the host (workspace URL) and a personal access token. This can be done using the Databricks CLI:
#
#
# ```
# databricks secrets create-scope <scope-name>
# databricks secrets put-secret --json '{
#   "scope": "<scope-name>",
#   "key": "<key-name>",
#   "string_value": "<value>"
# }'
# ```

# %% [markdown]
# **Important:** Please note the syntax setup for the authentication above. Rather than passing the secret variables directly, we follow syntax requirements **&lcub;&lcub;secrets/&lt;scope&gt;/&lt;key-name&gt;&rcub;&rcub;** so that the endpoint will look up the secrets in real-time rather than automatically configure and expose static values.
#
# **To print the secret values:**

# %%
# Print the value of scope, key for token and key for host
print("Scope: ", DA.scope_name)
print("Key for Token: depl_demo_token")
print("Key for Host: depl_demo_host")

# %% [markdown]
# ###2.2: Configure and Deploy Endpoint
#
# Configure the endpoint and deploy the model using the SDK, ensuring proper setup of environment variables.

# %%
from databricks.sdk.service.serving import EndpointCoreConfigInput
from databricks.sdk import WorkspaceClient

# Define endpoint configuration
endpoint_config_dict = {
    "served_models": [
        {
            "model_name": <FILL_IN>,
            "model_version": <FILL_IN>,
            "scale_to_zero_enabled": True,
            "workload_size": "Small",
            "environment_vars": {
               "DATABRICKS_TOKEN": "{{{{secrets/{0}/depl_demo_token}}}}".format(DA.scope_name),
               "DATABRICKS_HOST": "{{{{secrets/{0}/depl_demo_host}}}}".format(DA.scope_name),
            },
        },
    ]
}

endpoint_config = EndpointCoreConfigInput.from_dict(endpoint_config_dict)

# Initiate the workspace client
w = WorkspaceClient()
serving_endpoint_name = f"{DA.unique_name('_')}_endpoint"

# Get endpoint if it exists
existing_endpoint = next(
    (e for e in w.serving_endpoints.list() if e.name == serving_endpoint_name), None
)

# Get the Databricks host
db_host = dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().get("browserHostName").value()
serving_endpoint_url = f"{db_host}/ml/endpoints/{serving_endpoint_name}"

# If endpoint doesn't exist, create it
if existing_endpoint is None:
    print(f"Creating the endpoint {serving_endpoint_url}, this will take a few minutes to package and deploy the endpoint...")
    w.serving_endpoints.<FILL_IN>
# If endpoint does exist, update it to serve the new version
else:
    print(f"Updating the endpoint {serving_endpoint_url} to version {latest_model_version}, this will take a few minutes to package and deploy the endpoint...")
    w.serving_endpoints.<FILL_IN>

# Display the endpoint URL
displayHTML(f'Your Model Endpoint Serving is now available. Open the <a href="/ml/endpoints/{serving_endpoint_name}">Model Serving Endpoint page</a> for more details.')

# %%
from databricks.sdk.service.serving import EndpointCoreConfigInput
from databricks.sdk import WorkspaceClient

# Define endpoint configuration
endpoint_config_dict = {
    "served_models": [
        {
            "model_name": model_name,
            "model_version": latest_model_version,
            "scale_to_zero_enabled": True,
            "workload_size": "Small",
            "environment_vars": {
                "DATABRICKS_TOKEN": "{{{{secrets/{0}/depl_demo_token}}}}".format(DA.scope_name),
                "DATABRICKS_HOST": "{{{{secrets/{0}/depl_demo_host}}}}".format(DA.scope_name),
            },
        },
    ]
}

endpoint_config = EndpointCoreConfigInput.from_dict(endpoint_config_dict)

# Initiate the workspace client
w = WorkspaceClient()
serving_endpoint_name = f"{DA.unique_name('_')}_endpoint"

# Get endpoint if it exists
existing_endpoint = next(
    (e for e in w.serving_endpoints.list() if e.name == serving_endpoint_name), None
)

# Get the Databricks host
db_host = dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().get("browserHostName").value()
serving_endpoint_url = f"{db_host}/ml/endpoints/{serving_endpoint_name}"

# If endpoint doesn't exist, create it
if existing_endpoint is None:
    print(f"Creating the endpoint {serving_endpoint_url}, this will take a few minutes to package and deploy the endpoint...")
    w.serving_endpoints.create_and_wait(name=serving_endpoint_name, config=endpoint_config)
# If endpoint does exist, update it to serve the new version
else:
    print(f"Updating the endpoint {serving_endpoint_url} to version {latest_model_version}, this will take a few minutes to package and deploy the endpoint...")
    w.serving_endpoints.update_config_and_wait(served_models=endpoint_config.served_models, name=serving_endpoint_name)

# Display the endpoint URL
displayHTML(f'Your Model Endpoint Serving is now available. Open the <a href="/ml/endpoints/{serving_endpoint_name}">Model Serving Endpoint')

# %% [markdown]
# ### 2.3: Create Inference Table via Model Serving UI
#
# Set up an inference table through the Model Serving UI:
#
# 1. Click the link printed above in the output of **step 2.2**.
# 2. Click the **Edit endpoint** button.
# 3. Expand the **Inference tables** section.
# 4. Check the **Enable inference tables** box.
# 5. Enter the catalog, schema, and table information for the inference table:
#    - **Catalog Name:** `<Your Catalog Name>`
#    - **Schema Name:** `<Your Schema Name>`
#    - **Table Name Prefix:** `<Your Table Name>` (e.g.: `rag_app_realtime`)

# %% [markdown]
# ## Task 3: Configure A/B Testing Using the UI
#
# In this task, you will configure traffic splitting between the same version of the model for A/B testing using the Databricks UI. This will ensure that both configurations are available for inference, and you can direct a percentage of traffic to each configuration for A/B testing or gradual rollouts.
#
#
# 🚨 **Note:** Normally, you would register an improved version of the model. However, due to time constraints, you will deploy the same model that we served.
#
# **Steps:**
#
# 1. **Go to [Serving](/ml/endpoints)**
#
# 2. Locate the endpoint you created earlier.
# 3. Click on the **Edit endpoint** button next to the endpoint name.
#
# 4. **Add a New Served Entity**
#     - In the **Served entities** section, click on **+ Add served entity**.
#     - Select the entity name that matches your model name: **`genai_shared_catalog.ws_<xxx>.rag_app`**. Model name is printed in the begining of this notebook.
#     - Choose **Version 1** for the new served entity.
#
# 5. **Configure Traffic Splitting**
#     - In the **Traffic Splitting** section, divide the traffic between the two configurations.
#     - Set the traffic percentage to 60% for the new configuration and 40% for the old configuration.
#
# 6. **Set Compute Scale-out**
#     - For **Compute scale-out**, select **Small**.
#
# 7. **Advanced Configuration**
#     - Fill in the environment variables as follows - **These values are printed at the beginning of the lab**:
#       - **DATABRICKS_HOST** : **&lcub;&lcub;secrets/`scope`/`token_key` &rcub;&rcub;**
#       - **DATABRICKS_TOKEN** : **&lcub;&lcub;secrets/`scope`/`host_key` &rcub;&rcub;**
#
# 8. **Check Inference Table Details**
#     - Ensure that the inference table settings are correct.
#     - The table should capture inference results for analysis.
#
# 9. **Update and Wait**
#     - Click on the **Update** button to save your changes.
#     - Wait for the serving endpoint to update. This may take a few minutes.
#
# By following these steps, you will successfully configure A/B testing for your model using the same version, allowing you to evaluate different configurations and monitor their performance.

# %% [markdown]
# ## Task 4: Query the Endpoint 
#
# In this task, you will query the model using MLflow deployments.

# %%
from mlflow.deployments import get_deploy_client
# Initialize the deployment client
deploy_client = get_deploy_client("databricks")
# Define the question to be sent to the model for inference
question = "What is PPO?"
# Send the query to the specified serving endpoint and receive the response
response = deploy_client.<FILL_IN>

# Print the model's prediction from the response received
print(<FILL_IN>)

# %%
from mlflow.deployments import get_deploy_client
# Initialize the deployment client
deploy_client = get_deploy_client("databricks")
# Define the question to be sent to the model for inference
question = "What is PPO?"
# Send the query to the specified serving endpoint and receive the response
response = deploy_client.predict(
    endpoint=serving_endpoint_name,
    inputs={"inputs": [{"query": question}]}
)

# Print the model's prediction from the response received
print(response.predictions)

# %% [markdown]
# ## Task 5: Inspect Inference Table
#
# In this task, you will view and inspect the inference table created during the deployment process. The inference table stores data about the inferences made by your model, which can be useful for monitoring and analyzing model performance.
#
# **Steps:**
#
# 1. **Go to [Catalog](explore/data).**
#
# 2. **Select the Catalog and Schema:**
#    - In the Catalog Explorer, find and select the catalog that you entered while configuring the inference table.
#    - Within the selected catalog, navigate to the schema that contains your inference table.
#
# 3. **View the Inference Table:**
#    - Locate the inference table within the selected schema. The table name is prefixed as specified during the deployment configuration.
#    - Click on the inference table to open and view the sample data stored in it.
#
# By following these steps, you will be able to access and inspect the inference data stored in the table, allowing you to analyze how your model is performing and what kind of predictions it is making.
#

# %% [markdown]
# ##Cleanup Classroom
# Run the following cell to remove lesson-specific assets created during this lesson.

# %%
DA.cleanup()

# %% [markdown]
# ## Conclusion
#
# In this lab, you successfully deployed a custom model using Databricks Model Serving. You learned how to retrieve model versions, deploy models using the SDK, create and deploy a second version using the UI, query the model endpoint, and inspect inference results stored in the table.

# %% [markdown]
#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
