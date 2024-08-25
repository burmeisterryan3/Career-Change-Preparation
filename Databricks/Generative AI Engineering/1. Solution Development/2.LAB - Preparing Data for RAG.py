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
# # Lab: Preparing Data for Retrieval-Augmented Generation (RAG)
#
# The objective of this lab is to demonstrate the process of ingesting and processing documents for a Retrieval-Augmented Generation (RAG) application. This involves extracting text from PDF documents, computing embeddings using a foundation model, and storing the embeddings in a Delta table.
#
#
# **Lab Outline:**
#
# In this lab, you will need to complete the following tasks:
#
# * **Task 1 :** Read the PDF files and load them into a DataFrame.
#
# * **Task 2 :** Extract the text content from the PDFs and split it into manageable chunks.
#
# * **Task 3 :** Compute embeddings for each text chunk using a foundation model endpoint.
#
# * **Task 4 :** Create a Delta table to store the computed embeddings.
#
# **📝 Your task:** Complete the **`<FILL_IN>`** sections in the code blocks and follow the other steps as instructed.

# %% [markdown]
# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **14.3.x-cpu-ml-scala2.12 14.3.x-scala2.12**

# %% [markdown]
#
# ## Classroom Setup
#
# Before starting the lab, run the provided classroom setup script. This script will define configuration variables necessary for the demo. Execute the following cell:

# %%
# %pip install --quiet PyMuPDF mlflow==2.14.3 transformers==4.44.0 "unstructured[pdf,docx]==0.14.10" llama-index==0.10.62 pydantic==2.8.2 accelerate
dbutils.library.restartPython()

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
# ## Task 1: Read the PDF files and load them into a DataFrame.
#
# To start, you need to load the PDF files into a DataFrame.
#
# **Steps:**
#
# 1. Use Spark to load the binary PDFs into a DataFrame.
#
# 2. Ensure that each PDF file is represented as a separate record in the DataFrame.

# %%
# run this cell to import the required libraries
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import Document
from llama_index.core.utils import set_global_tokenizer
from transformers import AutoTokenizer
from typing import Iterator
from pyspark.sql.functions import col, udf, length, pandas_udf, explode
import os
import pandas as pd 
from unstructured.partition.auto import partition
import io

# %%
# use Spark to load the PDF files into a DataFrame
# reduce the arrow batch size as our PDF can be big in memory
spark.conf.set("spark.sql.execution.arrow.maxRecordsPerBatch", 10)
articles_path = f"{DA.paths.datasets}/arxiv-articles/"
table_name = f"{DA.catalog_name}.{DA.schema_name}.pdf_raw_text"

# read pdf files
df = spark.read.format("binaryFile").option("recursiveFileLookup", "true").load(articles_path)

# save list of the files to table
df.write.mode("overwrite").saveAsTable(table_name)

display(df)


# %% [markdown]
# ## Task 2: Extract the text content from the PDFs and split it into manageable chunks
#
# Next, extract the text content from the PDFs and split it into manageable chunks.
#
# **Steps:**
#
# 1. Define a function to split the text content into chunks.
#
#     * Split the text content into manageable chunks.
#
#     * Ensure each chunk contains a reasonable amount of text for processing.
#
# 2. Apply the function to the DataFrame to create a new DataFrame with the text chunks.
#

# %%
### From the helper functions

# import fitz  # PyMuPDF

# # Function to extract text from PDF using PyMuPDF
# def extract_doc_text(pdf_content):
#     doc = fitz.open(stream=pdf_content, filetype="pdf")
#     text = ""
#     for page in doc:
#         text += page.get_text()
#     return text

# %%
# define a function to split the text content into chunks
@pandas_udf("array<string>")
def read_as_chunk(batch_iter: Iterator[pd.Series]) -> Iterator[pd.Series]:
    # set llama2 as tokenizer
    set_global_tokenizer(AutoTokenizer.from_pretrained("hf-internal-testing/llama-tokenizer"))
    # sentence splitter from llama_index to split on sentences
    splitter = SentenceSplitter(chunk_size=500, chunk_overlap=50)
    def extract_and_split(b):
      txt = extract_doc_text(b)
      nodes = splitter.get_nodes_from_documents([Document(text=txt)])
      return [n.text for n in nodes]


    for x in batch_iter:
        yield x.apply(extract_and_split)
#
df_chunks = (df
               .withColumn("content", explode(read_as_chunk("content")))
               .selectExpr('path as pdf_name', 'content')
               )
display(df_chunks)


# %% [markdown]
# ## Task 3: Compute embeddings for each text chunk using a foundation model endpoint
# Now, compute embeddings for each text chunk using a foundation model endpoint.
#
# **Steps:**
#
# 1. Define a function to compute embeddings for text chunks.
#     + Use a foundation model endpoint to compute embeddings for each text chunk.
#     + Ensure that the embeddings are computed efficiently, considering the limitations of the model.  
#
# 2. Apply the function to the DataFrame containing the text chunks to compute embeddings for each chunk.
#

# %%
# define a function to compute embeddings for text chunks
@pandas_udf("array<float>")
def get_embedding(contents: pd.Series) -> pd.Series:
    import mlflow.deployments

    # define deployment client
    deploy_client = mlflow.deployments.get_deploy_client("databricks")
    
    def get_embeddings(batch):
        # calculate embeddings using the deployment client's predict function 
        response = deploy_client.predict(endpoint="databricks-gte-large-en", inputs={"input": batch})
        return [e['embedding'] for e in response.data]

    # splitting the contents into batches of 150 items each, since the embedding model takes at most 150 inputs per request.
    max_batch_size = 150
    batches = [contents.iloc[i:i + max_batch_size] for i in range(0, len(contents), max_batch_size)]

    # process each batch and collect the results
    all_embeddings = []
    for batch in batches:
        all_embeddings.extend(get_embeddings(batch.tolist()))

    return pd.Series(all_embeddings)
    
df_chunk_emd = (df_chunks
                .withColumn("embedding", get_embedding("content"))
                .selectExpr("pdf_name", "content", "embedding")
               )
display(df_chunk_emd)

# %% [markdown]
# ## Task 4: Create a Delta table to store the computed embeddings
#
# Finally, create a Delta table to store the computed embeddings.
#
# Steps:
#
#   1. Define the schema for the Delta table.
#
#   2. Save the DataFrame containing the computed embeddings as a Delta table.
#
#
# **Note:** Ensure that the Delta table is properly structured to facilitate efficient querying and retrieval of the embeddings.
#
# **📌 Instructions:** 
#
# - Please execute the following SQL code block to create the Delta table. This table will store the computed embeddings along with other relevant information. 
#
# **Important:** Storing the computed embeddings in a structured format like a Delta table ensures efficient querying and retrieval of the embeddings when needed for various downstream tasks such as retrieval-augmented generation. Additionally, setting the `delta.enableChangeDataFeed` property to true enables Change Data Feed (CDC), which is required for VectorSearch to efficiently process changes in the Delta table.

# %%
# %sql
CREATE TABLE IF NOT EXISTS pdf_text_embeddings_lab (
  id BIGINT GENERATED BY DEFAULT AS IDENTITY,
  pdf_name STRING,
  content STRING,
  embedding ARRAY <FLOAT>
  -- NOTE: the table has to be CDC because VectorSearch is using DLT that is requiring CDC state
  ) TBLPROPERTIES (delta.enableChangeDataFeed = true);

# %%
# define the schema for the Delta table
embedding_table_name = f"{DA.catalog_name}.{DA.schema_name}.pdf_text_embeddings_lab"
# save the DataFrame as a Delta table
df_chunk_emd.write.mode("append").saveAsTable(embedding_table_name)

# %% [markdown]
#
# ## Clean up Classroom
#
# **🚨 Warning:** Please refrain from deleting the catalog and tables created in this lab, as they are required for upcoming labs. To clean up the classroom assets, execute the classroom clean-up script provided in the final lab.

# %% [markdown]
#
# ## Conclusion
#
# In this lab, you learned how to prepare data for Retrieval-Augmented Generation (RAG) applications. By extracting text from PDF documents, computing embeddings, and storing them in a Delta table, you can enhance the capabilities of language models to generate more accurate and relevant responses.

# %% [markdown]
#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
