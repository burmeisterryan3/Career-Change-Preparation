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
# # Building Multi-stage AI Systems in Databricks
#
# In this demo we will start building a multi-stage reasoning system using Databricks' features and LangChain. Before we build the chain, first, we will show various components that are commonly used in multi-stage chaining system. 
#
# In the main section of the demo, we will build a multi-stage system. First, we will build a chain that will answer user questions using DBRX model. The second chain will search for DAIS-2023 talks and will try to find the corresponding video on YouTube. The final, complete chain will recommend videos to the user.
#
# **Learning Objectives:**
#
# *By the end of this demo, you will be able to;*
#
# * Identify that LangChain can include stages/tasks that are not LLMs.
#
# * Create basic LLM chains to connect prompts and LLMs.
#
# * Use tools to complete various tasks in the complete system.
#
# * Construct sequential chains of multiple LLMChains to perform multi-stage reasoning analysis.

# %% [markdown]
# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **14.3.x-cpu-ml-scala2.12 14.3.x-scala2.12**
#

# %% [markdown]
#
# ## Classroom Setup
#
# Before starting the demo, run the provided classroom setup script. This script will define configuration variables necessary for the demo. Execute the following cell:

# %%
# %pip install -U --quiet databricks-sdk==0.29.0 langchain-core==0.2.24 databricks-vectorsearch==0.40 langchain-community==0.2.10 typing-extensions==4.12.2 youtube_search Wikipedia grandalf mlflow==2.14.3 pydantic==2.8.2

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
# ## Enable MLflow Auto-Log
#
# MLflow has support for auto-logging LangChain models. We will enable this below.

# %%
import mlflow
mlflow.langchain.autolog()

# %% [markdown]
# ## Using LLMs and Prompts without an External Library
#
# While there are many libraries out there for building chains and in this demo we will be using one as well, you don't need a third party library for a simple prompt. We can use `databricks-sdk` to directly query an **Foundational Model API endpoint**. 
#

# %%
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.serving import ChatMessage

w = WorkspaceClient()

genre = "romance"
actor = "Brad Pitt"

prompt = f"Tell me about a {genre} movie which {actor} is one of the actors."

messages = [
    { 
        "role": "user", 
        "content": prompt 
    }
]
messages = [ChatMessage.from_dict(message) for message in messages]
llm_response = w.serving_endpoints.query(
    name="databricks-dbrx-instruct",
    messages=messages,
    temperature=0.2,
    max_tokens=128
)

print(llm_response.as_dict()["choices"][0]["message"]["content"])

# %% [markdown]
#
# ## LangChain Basics
#
# As demonstrated in the previous section, it is not necessary to use a third-party chaining library to construct a multi-chain AI system. However, composition libraries like **LangChain** can simplify some of the steps by providing a generic interface for supported large language models (LLMs).
#
# Before we begin building a multi-stage chain, let's review the main LangChain components that we will use in this module.
#

# %% [markdown]
# ### Prompt
#
# Prompt is one of the basic blocks when interacting with GenAI models. They may include instructions, examples and specific context information related to the given task. Let's create a very basic prompt.
#

# %%
from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template("Tell me about a {genre} movie which {actor} is one of the actors.")
prompt_template.format(genre="romance", actor="Brad Pitt")

# %% [markdown]
# ### LLMs
#
# LLMs are the core component when building compound AI systems. They are the **brain** of the system for reasoning and generating the response.
#
# Let's see how to interact with **Databricks's DBRX** model.
#

# %%
from langchain_community.chat_models import ChatDatabricks

# You can play with max_tokens to define the length of the response
llm_dbrx = ChatDatabricks(endpoint="databricks-dbrx-instruct", max_tokens = 500)

for chunk in llm_dbrx.stream("Who is Brad Pitt?"):
    print(chunk.content, end="\n", flush=True)

# %% [markdown]
# ### Retriever
#
# Retrievers are used when external data is retrieved and passed to the model for generating response. There are various types of retrievers such as *document retrievers* and *vector store retrievers*.
#
# In the next section of the demo, we will use **Databricks Vector Search** as retriever to fetch documents by input query.
#
# For now, let's try a simple **Wikipedia retriever**.

# %%
from langchain_community.retrievers import WikipediaRetriever
retriever = WikipediaRetriever()
docs = retriever.invoke(input="Brad Pitt")
print(docs[0])

# %% [markdown]
# ### Tools
#
# Tools are functions that can be invoked in the chain. Tools has *input parameters* and a *function* to run.
#
# Here, we have a Youtube search tool. The tool's `description` defines why a tool can be used and the `args` defines what input arguments can be passed to the tool.

# %%
from langchain_community.tools import YouTubeSearchTool
tool = YouTubeSearchTool()
tool.run("Brad Pitt movie trailer")

# %%
print(tool.description)
print(tool.args)

# %% [markdown]
# ### Chaining
#
# One of the important features of these components is the ability to **chain** them together. Let's connect the LLM with the prompt.

# %%
from langchain_core.output_parsers import StrOutputParser

chain = prompt_template | llm_dbrx | StrOutputParser()
print(chain.invoke({"genre":"romance", "actor":"Brad Pitt"}))

# %% [markdown]
# ## Build a Multi-stage Chain

# %% [markdown]
# ### Create a Vector Store
#
# **🚨IMPORTANT: Vector Search endpoints must be created before running the rest of the demo. Endpoint names should be in this format; `vs_endpoint_x`. The endpoint will be assigned by username.**

# %%
# Assign VS search endpoint by username
vs_endpoint_prefix = "vs_endpoint_"
vs_endpoint_fallback = "vs_endpoint_fallback"
vs_endpoint_name = vs_endpoint_prefix+str(get_fixed_integer(DA.unique_name("_")))
print(f"Vector Endpoint name: {vs_endpoint_name}. In case of any issues, replace variable `vs_endpoint_name` with `vs_endpoint_fallback` in demos and labs.")

# Source table and VS index table names
vs_index_table_fullname = f"{DA.catalog_name}.{DA.schema_name}.dais_embeddings"
source_table_fullname = f"{DA.catalog_name}.{DA.schema_name}.dais_text"

# %% [markdown]
# The dataset that we will be using in this module is already created in the classroom setup script. Let's have a quick look at the dataset.
#
# Then, we will create a vector store index and store embeddings there.

# %%
display(spark.sql(f"SELECT * FROM {source_table_fullname}"))

# %%
# Store embeddings in vector store
create_vs_index(vs_endpoint_name, vs_index_table_fullname, source_table_fullname, "Title")

# %% [markdown]
# ### Define Common Objects

# %%
from langchain_community.chat_models import ChatDatabricks
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from IPython.display import display, HTML

llm_dbrx = ChatDatabricks(endpoint="databricks-meta-llama-3-70b-instruct", max_tokens = 1000)

# %% [markdown]
# ### Build First Chain
#
# The **first chain** will be used for listing videos relevant to the user's question. In order to get videos, first, we need to search for the DAIS-2023 talks that are already stored in a Vector Search index. After retrieving the relevant titles, we will use YouTube search tool to get the videos for the talks. In the final stage, these videos are passed to the chain to generate a response for the user.
#
# This chain consist of a `prompt template`, `retriever`, `llm model` and `output parser`.

# %%
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import DatabricksVectorSearch

# Prompt to format the video titles for YouTube search
prompt_template_1 = PromptTemplate.from_template(
    """
    Construct a search query for YouTube based on the titles below. Make sure to add DAIS 2023 as part of the query. Remove all quotes from the query and return only the query.

    <video_titles>
    {context}
    </video_titles>

    Answer:
    """
)

# Create a vector store client and retreive documents
def get_retriever(persist_dir=None):
    vsc = VectorSearchClient(disable_notice=True)
    vs_index = vsc.get_index(vs_endpoint_name, vs_index_table_fullname)
    vectorstore = DatabricksVectorSearch(vs_index, text_column="Title")
    return vectorstore.as_retriever(search_kwargs={"k": 2})


# First chain
chain_video = (
    {"context": get_retriever(), "input": RunnablePassthrough()}
    | prompt_template_1
    | llm_dbrx
    | StrOutputParser()
)

# Test the chain
chain_video.invoke("How machine learning models are stored in Unity Catalog?")

# %% [markdown]
# ### Build Second Chain
#
# This chain will take the video titles based query from. the previous chain and search YouTube. The chain response will be Youtube video links.

# %%
from langchain_community.tools import YouTubeSearchTool
from langchain_core.runnables import RunnableLambda

# Generate image using first chain
def get_videos(input):
    tool_yt = YouTubeSearchTool()
    video_urls = tool_yt.run(input)
    return video_urls

chain_youtube = RunnableLambda(get_videos) | StrOutputParser()

# Get the image URL
response = chain_youtube.invoke("DAIS 2023 Streamlining API Deployment for ML Models Across Multiple Brands Ahold Delhaize's Experience on Serverless OR Building a Real-Time Model Monitoring Pipeline on Databricks")

print(response)

# %% [markdown]
# ### Build Third Chain
#
# The **third chain** will be a simple question-answer prompt using **DBRX**. The chain will use the video links as well for recommendation. This chain consist of a `prompt template`, `llm model` and `output parser`.

# %%
prompt_template_3 = PromptTemplate.from_template(
    """You are a Databricks expert. You will get questions about Databricks. Try to give simple answers and be professional. Don't include code in your response.

    Question: {input}

    Answer:

    Also, encourage the user to watch the videos provided below. Show video links as a list. Strip the YouTube link at "&pp=" and keep the first part of the URL. There is no title for the links so only show the URL. Only use the videos provided below.

    Video Links: {videos}

    Format response in HTML format.
    """
)

chain_expert = (prompt_template_3 | llm_dbrx | StrOutputParser())
chain_expert.invoke({
    "input": "How machine learning models are stored in Unity Catalog?",
    "videos": ""
    })

# %% [markdown]
# ### Chaining Chains ⛓️
#
# So far we create chains for each stage. To build a multi-stage system, we need to link these chains together and build a multi-chain system.

# %%
multi_chain = (
  {
    "input": RunnablePassthrough(),
    "videos": (chain_video | chain_youtube | StrOutputParser())
  }
  |chain_expert
  |llm_dbrx 
  |StrOutputParser()
)

query = "How machine learning models are stored in Unity Catalog?"
response = multi_chain.invoke(query)
display(HTML(response))

# %% [markdown]
# View the flow of the final chain.

# %%
multi_chain.get_graph().print_ascii()

# %% [markdown]
# ## Save the Chain to Model Registery in UC
#
# Now that our chain is ready and evaluated, we can register it within our Unity Catalog schema. 
#
# After registering the chain, you can view the chain and models in the **Catalog Explorer**.

# %%
from mlflow.models import infer_signature
import mlflow


# Set model registery to UC
mlflow.set_registry_uri("databricks-uc")
model_name = f"{DA.catalog_name}.{DA.schema_name}.multi_stage_demo"

with mlflow.start_run(run_name="multi_stage_demo") as run:
    signature = infer_signature(query, response)
    model_info = mlflow.langchain.log_model(
        multi_chain,
        loader_fn=get_retriever, 
        artifact_path="chain",
        registered_model_name=model_name,
        input_example=query,
        signature=signature
    )

# %% [markdown]
# ## Load the chain from Model Registery in UC
#
# Now that our chain is registeried in UC, we can load it and invoke it.

# %%
model_uri = f"models:/{model_name}/{model_info.registered_model_version}"
model = mlflow.langchain.load_model(model_uri)

model.invoke("How machine learning models are stored in Unity Catalog?")

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
# In this demo, we explored building a multi-stage reasoning system with Databricks' tools and LangChain. We began by introducing common system components and then focused on creating chains for specific tasks like answering user queries and finding DAIS-2023 talks. By the end, participants learned to use LangChain beyond just LLMs and construct sequential chains for multi-stage analyses.

# %% [markdown]
#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
