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
# # Assembling and Evaluating a RAG Application
#
# In the previous demo, we created a Vector Search Index. To build a complete RAG application, it is time to connect all the components that you have learned so far and evaluate the performance of the RAG.
#
# After evaluating the performance of the RAG pipeline, we will create and deploy a new Model Serving Endpoint to perform RAG.
#
# **Learning Objectives:**
#
# *By the end of this demo, you will be able to:*
#
# - Describe embeddings, vector databases, and search/retrieval as key components of implementing performant RAG applications.
# - Assemble a RAG pipeline by combining various components.
# - Build a RAG evaluation pipeline with MLflow evaluation functions.
# - Register a RAG pipeline to the Model Registry.
#

# %% [markdown]
# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **14.3.x-cpu-ml-scala2.12 14.3.x-scala2.12**
#
#
#
# **🚨 Important: This demonstration relies on the resources established in the previous one. Please ensure you have completed the prior demonstration before starting this one.**

# %% [markdown]
#
# ## Classroom Setup
#
# Install required libraries.

# %%
# %pip install -U --quiet mlflow==2.14.3 databricks-vectorsearch==0.40 transformers==4.43.3 "unstructured[pdf,docx]==0.14.10" langchain==0.2.11 langchain-community==0.2.10 pydantic==2.8.2 flashrank==0.2.8 pyspark==3.1.2 PyMuPDF accelerate
dbutils.library.restartPython()

# %% [markdown]
# Before starting the demo, run the provided classroom setup script. This script will define configuration variables necessary for the demo. Execute the following cell:

# %%
# %run ../Includes/Classroom-Setup-03

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
# As seen in the diagram below, in this demo we will focus on the inference section (highlighted in green). The main focus of the previous demos was  Step 1 - Data preparation and vector storage. Now, it is time put all components together to create a RAG application. 
#
# The flow will be the following:
#
# - A user asks a question
# - The question is sent to our serverless Chatbot RAG endpoint
# - The endpoint compute the embeddings and searches for docs similar to the question, leveraging the Vector Search Index
# - The endpoint creates a prompt enriched with the doc
# - The prompt is sent to the Foundation Model Serving Endpoint
# - We display the output to our users!
#
#
# <img src="https://files.training.databricks.com/images/genai/genai-as-01-llm-rag-self-managed-flow-2.png" width="100%">
#
#
#

# %% [markdown]
# ## Setup the RAG Components
#
# In this section, we will first define the components that we created before. Next, we will set up the retriever component for the application. Then, we will combine all the components together. In the final step, we will register the developed application as a model in the Model Registry with Unity Catalog.

# %% [markdown]
# ### Setup the Retriever
#
# We will setup the Vector Search endpoint that we created in the previous demos as retriever. The retriever will return 2 relevant documents based on the query.
#

# %%
# components we created before
# assign vs search endpoint by username
vs_endpoint_prefix = "vs_endpoint_"
vs_endpoint_fallback = "vs_endpoint_fallback"

vs_endpoint_name = vs_endpoint_prefix + str(get_fixed_integer(DA.unique_name("_")))
print(f"Vector Endpoint name: {vs_endpoint_name}. In case of any issues, replace variable `vs_endpoint_name` with `vs_endpoint_fallback` in demos and labs.")

vs_index_fullname = f"{DA.catalog_name}.{DA.schema_name}.pdf_text_self_managed_vs_index"

# %%
from databricks.vector_search.client import VectorSearchClient
from langchain.embeddings import DatabricksEmbeddings
from langchain_core.runnables import RunnableLambda
from langchain.docstore.document import Document
from flashrank import Ranker, RerankRequest

def get_retriever(cache_dir="/tmp"):

    def retrieve(query, k: int=10):
        if isinstance(query, dict):
            query = next(iter(query.values()))

        # get the vector search index
        vsc = VectorSearchClient(disable_notice=True)
        vs_index = vsc.get_index(endpoint_name=vs_endpoint_name, index_name=vs_index_fullname)
        
        # get the query vector
        embeddings = DatabricksEmbeddings(endpoint="databricks-bge-large-en")
        query_vector = embeddings.embed_query(query)
        
        # get similar k documents
        return query, vs_index.similarity_search(
            query_vector=query_vector,
            columns=["pdf_name", "content"],
            num_results=k)

    def rerank(query, retrieved, cache_dir, k: int=2):
        # format result to align with reranker lib format 
        passages = []
        for doc in retrieved.get("result", {}).get("data_array", []):
            new_doc = {"file": doc[0], "text": doc[1]}
            passages.append(new_doc)       
        # Load the flashrank ranker
        ranker = Ranker(model_name="rank-T5-flan", cache_dir=cache_dir)

        # rerank the retrieved documents
        rerankrequest = RerankRequest(query=query, passages=passages)
        results = ranker.rerank(rerankrequest)[:k]

        # format the results of rerank to be ready for prompt
        return [Document(page_content=r.get("text"), metadata={"source": r.get("file")}) for r in results]

    # the retriever is a runnable sequence of retrieving and reranking.
    return RunnableLambda(retrieve) | RunnableLambda(lambda x: rerank(x[0], x[1], cache_dir))

# test our retriever
question = {"input": "How does Generative AI impact humans?"}
vectorstore = get_retriever(cache_dir = f"{DA.paths.working_dir.replace('dbfs:/', '/dbfs')}/opt")
similar_documents = vectorstore.invoke(question)
print(f"Relevant documents: {similar_documents}")

# %% [markdown]
# ### Setup the Foundation Model
#
# Building Databricks Chat Model to query llama-2-70b-chat foundation model
#
# Our chatbot will be using llama2 foundation model to provide answer. 
#
# While the model is available using the built-in [Foundation endpoint](/ml/endpoints) (using the `/serving-endpoints/databricks-llama-2-70b-chat/invocations` API), we can use Databricks Langchain Chat Model wrapper to easily build our chain.  
#
# Note: multipe type of endpoint or langchain models can be used:
#
# - Databricks Foundation models (what we'll use)
# - Your fined-tune model
# - An external model provider (such as Azure OpenAI)

# %%
from langchain_community.chat_models import ChatDatabricks

# test Databricks Foundation LLM model
chat_model = ChatDatabricks(endpoint="databricks-llama-2-70b-chat", max_tokens = 300)
print(f"Test chat model: {chat_model.invoke('What is Generative AI?')}")

# %% [markdown]
# ## Assembling the Complete RAG Solution
#
# Let's now merge the retriever and the model in a single Langchain chain.
#
# We will use a custom langchain template for our assistant to give proper answer.
#
# Make sure you take some time to try different templates and adjust your assistant tone and personality for your requirement.
#
# <img src="https://files.training.databricks.com/images/genai/genai-as-01-llm-rag-self-managed-model-2.png" width="100%" />

# %% [markdown]
# Some important notes about the LangChain formatting:
#
# * Context documents retreived from the vector store are added by sperated newline.

# %%
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import PromptTemplate


TEMPLATE = """You are an assistant for GENAI teaching class. You are answering questions related to Generative AI and how it impacts humans life. If the question is not related to one of these topics, kindly decline to answer. If you don't know the answer, just say that you don't know, don't try to make up an answer. Keep the answer as concise as possible.
Use the following pieces of context to answer the question at the end:

<context>
{context}
</context>

Question: {input}

Answer:
"""
prompt = PromptTemplate(template=TEMPLATE, input_variables=["context", "input"])

# unwrap the longchain document from the context to be a dict so we can register the signature in mlflow
def unwrap_document(answer):
  return answer | {"context": [{"metadata": r.metadata, "page_content": r.page_content} for r in answer["context"]]}

question_answer_chain = create_stuff_documents_chain(chat_model, prompt)
chain = create_retrieval_chain(get_retriever(), question_answer_chain)|RunnableLambda(unwrap_document)

# %%
question = {"input": "How does Generative AI impact humans?"}
answer = chain.invoke(question)
print(answer)

# %% [markdown]
# ## Evaluating the RAG Pipeline
#
# To evaluate the RAG pipeline, we will use MLflow's LLM evaluation functions. MLflow provides a suite of automated tools that streamline the evaluation process, saving time and enhancing accuracy.
#
# To evaluate the RAG pipeline, we need an evaluation dataset. Typically, this set would include **questions**, **ground truth**, **context**, and **answers** generated by the RAG. Ideally, the **ground truth** is handcrafted by human experts. In this demo, we synthetically generated the dataset, which means the quality of the ground truth might not be the best.
#
# Below is the evaluation dataset that we will be using.
#
# **📌 Note:** MLflow's advanced evaluation features are covered in the **"Generative AI Evaluation and Governance"** course.
#

# %% [markdown]
# ### Prepare the Evaluation Dataset

# %%
eval_set = """question,ground_truth,evolution_type,episode_done
"What are the limitations of symbolic planning in task and motion planning, and how can leveraging large language models help overcome these limitations?","Symbolic planning in task and motion planning can be limited by the need for explicit primitives and constraints. Leveraging large language models can help overcome these limitations by enabling the robot to use language models for planning and execution, and by providing a way to extract and leverage knowledge from large language models to solve temporally extended tasks.",simple,TRUE
"What are some techniques used to fine-tune transformer models for personalized code generation, and how effective are they in improving prediction accuracy and preventing runtime errors? ","The techniques used to fine-tune transformer models for personalized code generation include ﬁne-tuning transformer models, adopting a novel approach called Target Similarity Tuning (TST) to retrieve a small set of examples from a training bank, and utilizing these examples to train a pretrained language model. The effectiveness of these techniques is shown in the improvement in prediction accuracy and the prevention of runtime errors.",simple,TRUE
How does the PPO-ptx model mitigate performance regressions in the few-shot setting?,"The PPO-ptx model mitigates performance regressions in the few-shot setting by incorporating pre-training and fine-tuning on the downstream task. This approach allows the model to learn generalizable features and adapt to new tasks more effectively, leading to improved few-shot performance.",simple,TRUE
How can complex questions be decomposed using successive prompting?,"Successive prompting is a method for decomposing complex questions into simpler sub-questions, allowing language models to answer them more accurately. This approach was proposed by Dheeru Dua, Shivanshu Gupta, Sameer Singh, and Matt Gardner in their paper 'Successive Prompting for Decomposing Complex Questions', presented at EMNLP 2022.",simple,TRUE
"Which entity type in Named Entity Recognition is likely to be involved in information extraction, question answering, semantic parsing, and machine translation?",Organization,reasoning,TRUE
What is the purpose of ROUGE (Recall-Oriented Understudy for Gisting Evaluation) in automatic evaluation methods?,"ROUGE (Recall-Oriented Understudy for Gisting Evaluation) is used in automatic evaluation methods to evaluate the quality of machine translation. It calculates N-gram co-occurrence statistics, which are used to assess the similarity between the candidate text and the reference text. ROUGE is based on recall, whereas BLEU is based on accuracy.",simple,TRUE
"What are the challenges associated with Foundation SSL in CV, and how do they relate to the lack of theoretical foundation, semantic understanding, and explicable exploration?","The challenges associated with Foundation SSL in CV include the lack of a profound theory to support all kinds of tentative experiments, and further exploration has no handbook. The pretrained LM may not learn the meaning of the language, relying on corpus learning instead. The models cannot reach a better level of stability and match different downstream tasks, and the primary method is to increase data, improve computation power, and design training procedures to achieve better results. The lack of theoretical foundation, semantic understanding, and explicable exploration are the main challenges in Foundation SSL in CV.",simple,TRUE
How does ChatGPT handle factual input compared to GPT-3.5?,"ChatGPT handles factual input better than GPT-3.5, with a 21.9% increase in accuracy when the premise entails the hypothesis. This is possibly related to the preference for human feedback in ChatGPT's RLHF design during model training.",simple,TRUE
What are some of the challenges in understanding natural language commands for robotic navigation and mobile manipulation?,"Some challenges in understanding natural language commands for robotic navigation and mobile manipulation include integrating natural language understanding with reinforcement learning, understanding natural language directions for robotic navigation, and mapping instructions and visual observations to actions with reinforcement learning.",simple,TRUE
"How does chain of thought prompting elicit reasoning in large language models, and what are the potential applications of this technique in neural text generation and human-AI interaction?","The context discusses the use of chain of thought prompting to elicit reasoning in large language models, which can be applied in neural text generation and human-AI interaction. Specifically, researchers have used this technique to train language models to generate coherent and contextually relevant text, and to create transparent and controllable human-AI interaction systems. The potential applications of this technique include improving the performance of language models in generating contextually appropriate responses, enhancing the interpretability and controllability of AI systems, and facilitating more effective human-AI collaboration.",simple,TRUE
"Using the given context, how can the robot be instructed to move objects around on a tabletop to complete rearrangement tasks?","The robot can be instructed to move objects around on a tabletop to complete rearrangement tasks by using natural language instructions that specify the objects to be moved and their desired locations. The instructions can be parsed using functions such as parse_obj_name and parse_position to extract the necessary information, and then passed to a motion primitive that can pick up and place objects in the specified locations. The get_obj_names and get_obj_pos APIs can be used to access information about the available objects and their locations in the scene.",reasoning,TRUE
"How can searching over an organization's existing knowledge, data, or documents using LLM-powered applications reduce the time it takes to complete worker activities?","Searching over an organization's existing knowledge, data, or documents using LLM-powered applications can reduce the time it takes to complete worker activities by retrieving information quickly and efficiently. This can be done by using the LLM's capabilities to search through large amounts of data and retrieve relevant information in a short amount of time.",simple,TRUE
"""

import pandas as pd
from io import StringIO

obj = StringIO(eval_set)
eval_df = pd.read_csv(obj)

# %%
display(eval_df)

# %% [markdown]
# Next, we will fill the dataset using the RAG pipeline we created to **answer** each question in the dataset. Also, we will store the **context** used for while answering the question. Context data will be used to evaluate context related metrics such as **context relevancy**

# %%
from datasets import Dataset


test_questions = eval_df["question"].values.tolist()
test_groundtruths = eval_df["ground_truth"].values.tolist()

answers = []
contexts = []

# answer each question in the dataset
for question in test_questions:
    # save the answer generated
    chain_response = chain.invoke({"input" : question})
    answers.append(chain_response["answer"])
    
    # save the contexts used
    vs_response = vectorstore.invoke(question)
    contexts.append(list(map(lambda doc: doc.page_content, vs_response)))

# construct the final dataset
response_dataset = Dataset.from_dict({
    "inputs" : test_questions,
    "answer" : answers,
    "context" : contexts,
    "ground_truth" : test_groundtruths
})

# %%
display(response_dataset.to_pandas())

# %% [markdown]
# ### Calcuate Evaluation Metrics
#
# Let's use MLflow's LLM evaluation functionality to compute some of the RAG evaluation metrics.
#
# As we will use a second model to judge the performance of the answer, we will need to define **a model to evaluate**. In this demo, we will use `DBRX` for evaluation. 
#
# The metrics to compute; `answer_similarity` and `relevance`. 
#
# For more information about various evaluation metrics, check [MLflow LLM evaluation documentation](https://mlflow.org/docs/latest/llms/llm-evaluate/index.html).
#

# %%
import mlflow
from mlflow.deployments import set_deployments_target

set_deployments_target("databricks")

dbrx_answer_similarity = mlflow.metrics.genai.answer_similarity(
    model="endpoints:/databricks-dbrx-instruct"
)

dbrx_relevance = mlflow.metrics.genai.relevance(
    model="endpoints:/databricks-dbrx-instruct"   
)

results = mlflow.evaluate(
        data=response_dataset.to_pandas(),
        targets="ground_truth",
        predictions="answer",
        extra_metrics=[dbrx_answer_similarity, dbrx_relevance],
        evaluators="default",
    )

# %%
display(results.tables["eval_results_table"])

# %% [markdown]
# ## Save the Model to Model Registery in UC
#
# Now that our model is ready and evaluated, we can register it within our Unity Catalog schema. 
#
# After registering the model, you can view the model and models in the **Catalog Explorer**.

# %%
from mlflow.models import infer_signature
import mlflow
import langchain


# set model registery to UC
mlflow.set_registry_uri("databricks-uc")
model_name = f"{DA.catalog_name}.{DA.schema_name}.rag_app_demo4"

with mlflow.start_run(run_name="rag_app_demo4") as run:
    signature = infer_signature(question, answer)
    model_info = mlflow.langchain.log_model(
        chain,
        loader_fn=get_retriever, 
        artifact_path="chain",
        registered_model_name=model_name,
        pip_requirements=[
            "mlflow==" + mlflow.__version__,
            "langchain==" + langchain.__version__,
            "databricks-vectorsearch",
        ],
        input_example=question,
        signature=signature
    )

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
# In this demo, we illustrated the process of constructing a comprehensive RAG application utilizing a variety of Databricks products. Initially, we established the RAG components that were previously created in the earlier demos, namely the Vector Search endpoint and Vector Search index. Subsequently, we constructed the retriever component and set up the foundational model for use. Following this, we put together the entire RAG application and evaluated the performance of the pipeline using MLflow's LLM evaluation functions. As a final step, we registered the newly created RAG application as a model within the Model Registry with Unity Catalog.

# %% [markdown]
# ## Hepful Resources
#
# * **The Databricks Generative AI Cookbook ([https://ai-cookbook.io/](https://ai-cookbook.io/))**: Learning materials and production-ready code to take you from initial POC to high-quality production-ready application using Mosaic AI Agent Evaluation and Mosaic AI Agent Framework on the Databricks platform.
#

# %% [markdown]
#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
