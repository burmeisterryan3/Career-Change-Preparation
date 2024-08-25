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
# # LAB - Create a "Managed" Vector Search Index
#
# The objective of this lab is to demonstrate the process of creating a **managed** Vector Search index for retrieval-augmented generation (RAG) applications. This involves configuring Databricks Vector Search to ingest data from a Delta table containing text embeddings and metadata.
#
#
#
# **Lab Outline:**
#
# In this lab, you will need to complete the following tasks;
#
# * **Task 1 :** Create a Vector Search endpoint to serve the index.
#
# * **Task 2 :** Connect Delta table with Vector Search endpoint
#
# * **Task 3 :** Test the Vector Search index
#
# * **Task 4 :** Re-rank search results
#
# **📝 Your task:** Complete the **`<FILL_IN>`** sections in the code blocks and follow the other steps as instructed.

# %% [markdown]
# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **14.3.x-cpu-ml-scala2.12 14.3.x-scala2.12**
#
# **🚨 Important: This lab relies on the resources created in the previous Lab. Please ensure you have completed the prior lab before starting this lab.**

# %% [markdown]
#
# ## Classroom Setup
#
# Before starting the demo, run the provided classroom setup script. This script will define configuration variables necessary for the demo. Execute the following cell:

# %%
# %pip install -U --quiet mlflow==2.14.3 databricks-vectorsearch==0.40 transformers==4.43.3 "unstructured[pdf,docx]==0.14.10" langchain==0.2.11 langchain-community==0.2.10 pydantic==2.8.2 flashrank==0.2.8 pyspark==3.1.2 PyMuPDF accelerate
dbutils.library.restartPython()

# %%
# %run ../Includes/Classroom-Setup-Lab

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
# ## Task 1: Create a Vector Search Endpoint
#
# To start, you need to create a Vector Search endpoint to serve the index.
#
# **🚨IMPORTANT: Vector Search endpoints must be created before running the rest of the demo. Endpoint names should be in this format; `vs_endpoint_x`. The endpoint will be assigned by username.**
#
# **💡 Instructions:**
#
# 1. Define the endpoint that you will use if you don't have endpoint creation permissions. 
# 1. [Optional]: Create a new enpoint. Check if the vector serch endpoint exists, if not, create it.
# 1. Wait for the endpoint to be ready.
#

# %% [markdown]
# ### Step-by-Step Instructions:
#
# 1. **Define Endpoint Name**: Set the variable `VECTOR_SEARCH_ENDPOINT_NAME` to the name of the endpoint you will use. If you don't have endpoint creation permissions, use the name of the existing endpoint.
#
# Additionally, you can check the endpoint status in the Databricks workspace [Vector Search Endpoints in Compute section](#/setting/clusters/vector-search).

# %%
# assign vs search endpoint by username
vs_endpoint_prefix = "vs_endpoint_"
vs_endpoint_fallback = "vs_endpoint_fallback"
vs_endpoint_name = vs_endpoint_prefix + str(get_fixed_integer(DA.unique_name("_")))
print(f"Vector Endpoint name: {vs_endpoint_name}. In case of any issues, replace variable `vs_endpoint_name` with `vs_endpoint_fallback` in demos and labs.")

# %%
import databricks.sdk.service.catalog as c
from databricks.vector_search.client import VectorSearchClient
from databricks.sdk import WorkspaceClient

vsc = VectorSearchClient()

# %% [markdown]
# **(Optional): Create New Endpoint**:
#     - If you have endpoint creation permissions:
#         - Uncomment the provided code block to create the endpoint.
#         - Run the code block to create the endpoint if it doesn't exist.
#     - If you don't have permissions:
#         - Skip this step.

# %%
# verify if the vector search endpoint already exists, if not, create it
# try:
#     # check if the vector search endpoint exists
#     vsc.get_endpoint(name=vs_endpoint_name)
#     print("Endpoint found: " + vs_endpoint_name)
# except Exception as e:
#     print("\nEndpoint not found: " + vs_endpoint_name)
#     # create a new vector search endpoint
#     if "NOT_FOUND" in str(e):
#         print("\nCreating Endpoint...")
#         vsc.create_endpoint(name=vs_endpoint_name, endpoint_type="STANDARD")
#     print("Endpoint Created: " + vs_endpoint_name)

# %% [markdown]
# 2. **Wait for Endpoint to be Ready**:
#     - After defining the endpoint name:
#         - Check the status of the endpoint using the provided function `wait_for_vs_endpoint_to_be_ready`.
#         >**Note:** 
#         > - If you encounter an error indicating that the endpoint is not found, proceed with the following steps:
#         >     - Replace the endpoint name in the code with the appropriate name.
#         >     - Uncomment and run the code block provided to create the endpoint (if you have permissions).

# %%
# def wait_for_vs_endpoint_to_be_ready(vsc, vs_endpoint_name):
#   for i in range(180):
#     endpoint = vsc.get_endpoint(vs_endpoint_name)
#     status = endpoint.get("endpoint_status", endpoint.get("status"))["state"].upper()
#     if "ONLINE" in status:
#       return endpoint
#     elif "PROVISIONING" in status or i <6:
#       if i % 20 == 0: 
#         print(f"Waiting for endpoint to be ready, this can take a few min... {endpoint}")
#       time.sleep(10)
#     else:
#       raise Exception(f'''Error with the endpoint {vs_endpoint_name}. - this shouldn't happen: {endpoint}.\n Please delete it and re-run the previous cell: vsc.delete_endpoint("{vs_endpoint_name}")''')
#   raise Exception(f"Timeout, your endpoint isn't ready yet: {vsc.get_endpoint(vs_endpoint_name)}")

# %%
# check the status of the endpoint.
wait_for_vs_endpoint_to_be_ready(vsc, vs_endpoint_name)
print(f"Endpoint named {vs_endpoint_name} is ready.")

# %% [markdown]
# ## Task 2: Create a Managed Vector Search Index
#
# Now, connect the Delta table containing text and metadata with the Vector Search endpoint. In this lab, you will create a **managed** index, which means you don't need to create the embeddings manually. For API details, check the [documentation page](https://docs.databricks.com/en/generative-ai/create-query-vector-search.html#create-index-using-the-python-sdk).
#
#
# **📌 Note 1: You will use the embeddings table that you created in the previous lab. If you haven't completed that lab, stop here and complete it first.**
#
# **📌 Note 2:** Although the source table already has the embedding column precomputed, we are not going to use it here to test the managed vector search capability to populate embeddings on the fly during data ingestion and query.
#
# **💡 Instructions:**
#
# 1. Define the source Delta table containing the text to be indexed.
#
# 1. Create a Vector Search index. Use these parameters; source column as `content` and `databricks-gte-large-en` as embedding model. Also, the sync process should be  `manually triggered`.
#
# 1. Create or synchronize the Vector Search index based on the source Delta table.
#

# %%
# def index_exists(vsc, endpoint_name, index_full_name):
#   try:
#       dict_vsindex = vsc.get_index(endpoint_name, index_full_name).describe()
#       return dict_vsindex.get('status').get('ready', False)
#   except Exception as e:
#       if 'RESOURCE_DOES_NOT_EXIST' not in str(e):
#           print(f'Unexpected error describing the index. This could be a permission issue.')
#           raise e
#   return False

# %%
# def wait_for_index_to_be_ready(vsc, vs_endpoint_name, index_name):
#   for i in range(180):
#     idx = vsc.get_index(vs_endpoint_name, index_name).describe()
#     index_status = idx.get('status', idx.get('index_status', {}))
#     status = index_status.get('detailed_state', index_status.get('status', 'UNKNOWN')).upper()
#     url = index_status.get('index_url', index_status.get('url', 'UNKNOWN'))
#     if "ONLINE" in status:
#       return
#     if "UNKNOWN" in status:
#       print(f"Can't get the status - will assume index is ready {idx} - url: {url}")
#       return
#     elif "PROVISIONING" in status:
#       if i % 40 == 0: print(f"Waiting for index to be ready, this can take a few min... {index_status} - pipeline url:{url}")
#       time.sleep(10)
#     else:
#         raise Exception(f'''Error with the index - this shouldn't happen. DLT pipeline might have been killed.\n Please delete it and re-run the previous cell: vsc.delete_index("{index_name}, {vs_endpoint_name}") \nIndex details: {idx}''')
#   raise Exception(f"Timeout, your index isn't ready yet: {vsc.get_index(index_name, vs_endpoint_name)}")

# %%
# the Delta table containing the text embeddings and metadata.
source_table_fullname = f"{DA.catalog_name}.{DA.schema_name}.pdf_text_embeddings_lab"
#
# the Delta table to store the Vector Search index.
vs_index_fullname = f"{DA.catalog_name}.{DA.schema_name}.pdf_text_self_managed_vs_index"
#
# create or sync the index
if not index_exists(vsc, vs_endpoint_name, vs_index_fullname):
  print(f"Creating index {vs_index_fullname} on endpoint {vs_endpoint_name}...")
#
  vsc.create_delta_sync_index(
    endpoint_name=vs_endpoint_name,
    index_name=vs_index_fullname,
    source_table_name=source_table_fullname,
    pipeline_type="TRIGGERED",
    primary_key="id",
    embedding_dimension=1024, # Embedding size must match your model's embedding dimension
    embedding_vector_column="embedding",
  )
else:
  # trigger a sync to update our vs content with the new data saved in the table
  vsc.get_index(vs_endpoint_name, vs_index_fullname).sync()

# let's wait for the index to be ready and all our embeddings to be created and indexed
wait_for_index_to_be_ready(vsc, vs_endpoint_name, vs_index_fullname)

# %% [markdown]
# ## Task 3: Search Documents Similar to the Query
#
# Test the Vector Search index by searching for similar content based on a sample query.
#
# **💡 Instructions:**
#
# 1. Get the index instance that we created.
#
# 1. Send a sample query to the language model endpoint using **query text**. 🚨 Note: As you created a managed index, you will use plain text for similarity search using `query_text` parameter.
#
# 1. Use the embeddings to search for similar content in the Vector Search index.

# %%
import mlflow.deployments

deploy_client = mlflow.deployments.get_deploy_client("databricks")
question = "What are the security and privacy concerns when training generative models?"
response = deploy_client.predict(endpoint="databricks-gte-large-en", inputs={"input": [question]})
embedding = response.data[0]["embedding"]

# %%
# get VS index.
index = vsc.get_index(vs_endpoint_name, vs_index_fullname)
#
#
# search for similar documents.
results = index.similarity_search(query_vector=embedding, columns=['pdf_name', 'content'], num_results=5)
#
# show the results.
docs = results.get('result', {}).get('data_array', [])
#
pprint(docs)

# %% [markdown]
# ## Task 4: Re-rank Search Results
#
# You have retreived some documents that are similar to the query text. However, the question of which documents are the most relevant is not done by the vector search results. Use `flashrank` library to re-rank the results and show the most relevant top 3 documents. 
#
# **💡 Instructions:**
#
# 1. Define `flashrank` with **`rank-T5-flan`** model.
#
# 1. Re-rank the search results.
#
# 1. Show the most relevant **top 3** documents.
#

# %%
from flashrank import Ranker, RerankRequest
#
# define the ranker.
cache_dir=f"{DA.paths.working_dir.replace('dbfs:/', '/dbfs/')}/opt/rank-T5-flan"
ranker = Ranker(model_name="rank-T5-flan", cache_dir=cache_dir)
#
# format the result to align with reranker library format 
passages = []
for doc in docs:
   new_doc = {"file": doc[0], "text": doc[1]}
   passages.append(new_doc)
#
# rerank the passages.
rerankrequest = RerankRequest(passages=passages, query=question)
ranked_passages = ranker.rerank(rerankrequest)

# show the top 3 results.
print(*ranked_passages[:3], sep="\n\n")

# %% [markdown]
#
# ## Clean up Classroom
#
# **🚨 Warning:** Please don't delete the catalog and tables created in this lab as next labs depend on these resources. To clean-up the classroom assets, run the classroom clean-up script in the last lab.

# %% [markdown]
#
# ## Conclusion
#
# In this lab, you learned how to set up a Vector Search index using Databricks Vector Search for retrieval-augmented generation (RAG) applications. By following the tasks, you successfully created a Vector Search endpoint, connected a Delta table containing text embeddings, and tested the search functionality. Furthermore, using a re-ranking library, you re-ordered the search results from the most relevant to least relevant documents. This lab provided hands-on experience in configuring and utilizing Vector Search, empowering you to enhance content retrieval and recommendation systems in your projects.

# %% [markdown]
#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
