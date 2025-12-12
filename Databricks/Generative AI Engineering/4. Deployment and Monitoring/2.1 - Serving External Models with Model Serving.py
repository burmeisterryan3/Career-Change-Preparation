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
# # Serving External Models with Model Serving
#
# **In this demo, we will focus on deploying GenAI applications.**
#
# Deployment is a key part of operationalizing our LLM-based applications. We will explore deployment options within Databricks and demonstrate how to achieve each one.
#
# **Learning Objectives:**
#
# *By the end of this demo, you will be able to:*
#
# * Determine the right deployment strategy for your use case.
# * Deploy an external model to a Databricks Model Serving endpoint.
# * Deploy a custom application to a Databricks Model Serving endpoint.

# %% [markdown]
# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **14.3.x-cpu-ml-scala2.12**
#

# %% [markdown]
# ## Classroom Setup
#
# Install required libraries.

# %%
# %pip install -U --quiet databricks-sdk mlflow

dbutils.library.restartPython()

# %% [markdown]
# ## Demo Overview
#
# In this demo, we will walk through basic deployment capabilities in Databricks. We'll discuss this in the following steps:
#
# 1. Access to custom model in Databricks Marketplace.
#
# 1. Deploy an external model to a Databricks Model Serving endpoint
#
# 1. Deploy a custom application to a Databricks Model Serving endpoint

# %% [markdown]
# ## Deploy an External Model with Databricks Model Serving
#
# While we have described and used tools like the AI Playground and Foundation Model APIs for querying common LLMs, there is sometimes a need to deploy more specific models as part of our applications.
#
# To achieve this, we can use **Databricks Model Serving**. Databricks Model Serving is a production-ready, serverless solution that simplifies real-time (and other types of) ML model deployment.
#
# Next, we will demonstrate the basics of Model Serving.
#
# **🚨 Important: Deploying custom models requires Model Serving with provisioned throughput and consumes significant compute resources. Therefore, this demo is intended to be presented by the instructor only. If you are running this course in your own environment and have the necessary permissions to deploy models, feel free to follow these instructions.**
#

# %% [markdown]
# ### Getting an External Model
#
# The simplest way to deploy a model in Model Serving is by getting an existing external model from the **Databricks Marketplace**.
#
# Let's explore the Marketplace for the Databricks-provided **CodeLlama Models**:
#
# 1. Head to the **[Databricks Marketplace](/marketplace)**.
#
# 1. Filter to "Models" **products provided by "Databricks"**.
#
# 1. Click on the **"CodeLlama Models"** tile.
#
# <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/genai/genai-as-04-marketplace-llama-code.png" width="100%"/>
#
#
# These models are designed to help with generating code – there are a series of fine-tuned versions.
#
# We are interested in deploying one of these models using Databricks Model Serving, so we'll need to follow the below steps:
#
# 1. Click on the **Get instant access** button on the models page
#
# 1. Specify our parameters, including that we want to use the model in Databricks and our `catalog name`.
#
# 1. Acknowledge the terms and conditions
#
# 1. Click **Get instant access**
#
# This will clone the models to the specified catalog. We can see them in the Catalog Explorer. Note that the catalog is created under **shared catalogs**.
#
# <br>
#
# <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/genai/genai-as-04-catalog-llama-code-.png" width="100%">
#
# **Note:** An important point here is that these models are now stored in Unity Catalog. This means that they're secure and we can govern access to them using the familiar, general Unity Catalog tooling.

# %% [markdown]
# ### Deploying a Model using Model Serving
#
# Once these models are in our catalog, we can deploy them directly to Databricks Model Serving by following the below steps:
#
# 1. Navigate to a specific model page in the Catalog.
#
# 1. Click the **Serve this Model** button.
#
# 1. Configure the served entity.
#     * Name: `CodeLlama_13b_Python_hf`.
#     * For served entities, select the model.
#
# 1. Click the **Confirm** button.
#
# 1. Configure the Model Serving endpoint.
#
# 1. Click the **Create** button.

# %% [markdown]
# ### Confirming the Deployed Model
#
# When the Model Serving endpoint is operational, we'll see a screen like this:
#
# <br>
#
# <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/genai/genai-as-04-serving-llama-endpoint.png" width="100%">
#
# **Note:** Notice the "Serving Deployment Status" field on the page. This will say "Not ready" until the model is deployed.
#
#

# %% [markdown]
# ## Query the Deployed Model
#
# More realistically, we can query the deployed model directly from our serving applications.

# %% [markdown]
# ### Query via the UI
#
# We can query the model directly in Databricks to confirm everything is working using the **Query endpoint** capability.
#
# Sample query:
# `{"prompt": "from spark.sql import functions as"}`

# %% [markdown]
# ### Query the Deployed Model in AI Playground
#
# To test the model with AI Playground, select the deployed model and use chatbox to send queries.

# %% [markdown]
# ### Query the Deployed Model with the SDK
#
# **💡 Tip:** Change the number of `max_tokens` to change the length of suggested code completion.

# %%
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

dataframe_records = [
    {"prompt": "from spark.sql import functions as", "max_tokens": 3}
]

w = WorkspaceClient()
response = w.serving_endpoints.query(
    name="CodeLlama_13b_Python_hf", #name of the model serving endpoint
    dataframe_records=dataframe_records,
)

print(response.as_dict()["predictions"][0]["candidates"][0]["text"])

# %% [markdown]
# This workflow is similar for external models like CodeLlama and **any other model that's in Unity Catalog**. In the next demo, we will deploy a custom model (RAG pipeline) using Model Serving.
#
# **Question:** What do you think of the results of the query? How could we improve the application to return better results?

# %% [markdown]
#
# ## Conclusion
#
# At this point, you should be able to:
#
# * Determine the right deployment strategy for your use case.
# * Deploy an external model to a Databricks Model Serving endpoint.
# * Deploy a custom application to a Databricks Model Serving endpoint.

# %% [markdown]
#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
