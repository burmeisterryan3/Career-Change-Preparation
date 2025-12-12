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
# # Benchmark Evaluation
#
#
# In this demo, **we will focus on evaluating large language models using a benchmark dataset specific to the task at hand.**
#
# **Learning Objectives:**
#
# *By the end of this demo, you will be able to;*
#
# * Obtain reference/benchmark data set for task-specific LLM evaluation
# * Evaluate an LLM's performance on a specific task using task-specific metrics
# * Compare relative performance of two LLMs using a benchmark set

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
# Install required libraries.

# %%
# %pip install mlflow==2.12.1 databricks-sdk==0.28.0 evaluate==0.4.1 rouge_score
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
# In this demonstration, we will be evaluating the performance of an AI system designed to summarize text.
#
# The text documents that we will be summarizing are a collection of fictional product reviews for grocery products.
#
# The AI system works as follows:
#
# 1. Accepts a text document as input
# 2. Constructs an LLM prompt using few-shot learning to summarize the text
# 3. Submits the prompt to an LLM for summarization
# 4. Returns summarized text
#
# See below for an example of the system.

# %% [markdown]
# ## Step 1: Setup Models to Use
#
# Next, we will setup the model that will be used for evaluation.
#
# We will use **Databricks DBRX** and **Llma2-70b-chat** for evaluation.

# %%
from databricks.sdk.service.serving import ChatMessage
from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

# first model for summarization
def query_summary_system(input: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are an assistant that summarizes text. Given a text input, you need to provide a one-sentence summary. You specialize in summiarizing reviews of grocery products. Please keep the reviews in first-person perspective if they're originally written in first person. Do not change the sentiment. Do not create a run-on sentence – be concise."
        },
        { 
            "role": "user", 
            "content": input 
        }
    ]
    messages = [ChatMessage.from_dict(message) for message in messages]
    chat_response = w.serving_endpoints.query(
        name="databricks-llama-2-70b-chat",
        messages=messages,
        temperature=0.1,
        max_tokens=128
    )

    return chat_response.as_dict()["choices"][0]["message"]["content"]

# second model for summarization
def challenger_query_summary_system(input: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are an assistant that summarizes text. Given a text input, you need to provide a one-sentence summary. You specialize in summiarizing reviews of grocery products. Please keep the reviews in first-person perspective if they're originally written in first person. Do not change the sentiment. Do not create a run-on sentence – be concise."
        },
        { 
            "role": "user", 
            "content": input 
        }
    ]
    messages = [ChatMessage.from_dict(message) for message in messages]
    chat_response = w.serving_endpoints.query(
        name="databricks-dbrx-instruct",
        messages=messages,
        temperature=0.1,
        max_tokens=128
    )

    return chat_response.as_dict()["choices"][0]["message"]["content"]


# %% [markdown]
# Let's test the models!

# %%
query_summary_system(
    "This is the best frozen pizza I've ever had! Sure, it's not the healthiest, but it tasted just like it was delivery from our favorite pizzeria down the street. The cheese browned nicely and fresh tomatoes are a nice touch, too! I would buy it again despite it's high price. If I could change one thing, I'd made it a little healthier – could we get a gluten-free crust option? My son would love that."
)

# %%
challenger_query_summary_system(
    "This is the best frozen pizza I've ever had! Sure, it's not the healthiest, but it tasted just like it was delivery from our favorite pizzeria down the street. The cheese browned nicely and fresh tomatoes are a nice touch, too! I would buy it again despite it's high price. If I could change one thing, I'd made it a little healthier – could we get a gluten-free crust option? My son would love that."
)

# %% [markdown]
# To complete this workflow, we'll focus on the following steps:
#
# 1. Obtain a benchmark set for evaluating summarization
# 2. Compute summarization-specific evaluation metrics using the benchmark set
# 3. Compare performance with another LLM using the benchmark set and evaluation metrics

# %% [markdown]
# ## Step 2: Benchmark and Reference Sets
#
# As a reminder, our task-specific evaluation metrics (including ROUGE for summarization) require a benchmark set to compute scores.
#
# There are two types of reference/benchmark sets that we can use:
#
# 1. Large, generic benchmark sets commonly used across use cases
# 2. Domain-specific benchmark sets specific to your use case
#
# For this demo, we'll focus on the former.
#
# ### Generic Benchmark Set
#
# First, we'll import a generic benchmark set used for evaluating text summarization.
#
# We'll use the data set used in [Benchmarking Large Language Models for News Summarization](https://arxiv.org/abs/2301.13848) to evaluate how well our LLM solution summarizes general text.
#
# This data set:
#
# * is relatively large in scale at 599 records
# * is related to news articles
# * contains original text and *author-written* summaries of the original text
#
# **Question:** What is the advantage of using ground-truth summaries that are written by the original author?

# %%
import pandas as pd

# Read and display the dataset
eval_data = pd.read_csv(f"{DA.paths.datasets.replace('dbfs:/', '/dbfs/')}/news-summarization.csv")
display(eval_data)


# %% [markdown]
# ## Step 4: Compute the ROUGE Evaluation Metric
#
# Next, we will want to compute our ROUGE-N metric to understand how well our system summarizes grocery generic text using the benchmark dataset.
#
# We can compute the ROUGE metric (among others) using MLflow's new LLM evaluation capabilities. MLflow LLM evaluation includes default collections of metrics for pre-selected tasks, e.g, “question-answering” or "text-summarization" (our case). Depending on the LLM use case that you are evaluating, these pre-defined collections can greatly simplify the process of running evaluations.
#
# The `mlflow.evaluate` function accepts the following parameters for this use case:
#
# * An LLM model
# * Reference data for evaluation (our benchmark set)
# * Column with ground truth data
# * The model/task type (e.g. `"text-summarization"`)
#
# **Note:** The `text-summarization` type will automatically compute ROUGE-related metrics. For some metrics, additional library intalls will be needed – you can see the requirements in the printed output.

# %%
# A custom function to iterate through our eval DF
def query_iteration(inputs):
    answers = []

    for index, row in inputs.iterrows():
        completion = query_summary_system(row["inputs"])
        answers.append(completion)

    return answers

# Test query_iteration function – it needs to return a list of output strings
query_iteration(eval_data.head())

# %%
import mlflow

# MLflow's `evaluate` with a custom function
results = mlflow.evaluate(
    query_iteration,                      # iterative function from above
    eval_data.head(50),                   # limiting for speed
    targets="writer_summary",             # column with expected or "good" output
    model_type="text-summarization"       # type of model or task
)

# %% [markdown]
# We can view the results for individual records by subsetting the handy `.tables` object.
#
# Notice all of the different versions of the ROUGE metric. These are calculated using the HuggingFace `evaluator` library, and the metrics are detailed [here](https://huggingface.co/spaces/evaluate-metric/rouge).
#
# In summary, the descriptions of each metric are below:
#
# * "rouge1": unigram (1-gram) based scoring
# * "rouge2": bigram (2-gram) based scoring
# * "rougeL": Longest common subsequence based scoring.
# * "rougeLSum": splits text using "\n"

# %%
display(results.tables["eval_results_table"].head(10))

# %% [markdown]
# And we can view summarized (mean, variance, etc.) model-level (rather than record-level) results with the following:

# %%
results.metrics

# %% [markdown]
# We are also able to review the results in the MLflow Experiment Tracking UI.

# %% [markdown]
# ### What does good look like?
#
# The ROUGE metrics range between 0 and 1 – where 0 indicates extremely dissimilar text and 1 indicates extremely similar text. However, our interpretation of what is "good" is usually going to be use-case specific. We don't always want a ROUGE score close to 1 because it's likely not reducing the text size too much.
#
# To explore what "good" looks like, let's review a couple of our examples.

# %%
import pandas as pd
display(
    pd.DataFrame(
        results.tables["eval_results_table"]
    ).loc[0:1, ["inputs", "outputs", "rouge1/v1/score"]]
)


# %% [markdown]
# **Discussion Questions:**
# 1. How do you interpret the ROUGE-1 score?
# 2. Do the scores reflect the summarization that you think is best?

# %% [markdown]
# ## Step 5: Comparing LLM Performance
#
# In practice, we will frequently be comparing LLMs (or larger AI systems) against one another when determining which is the best for our use case. As a result of this, it's important to become familiar with comparing these solutions.
#
# In the below cell, we demonstrate computing the same metrics using the same reference dataset – but this time, we're summarizing using a system that utilizes a different LLM.
#
# **Note:** This time, we're going to read our reference dataset from Delta.

# %%
# A compare custom function to iterate through our eval DF
def challenger_query_iteration(inputs):
    answers = []

    for index, row in inputs.iterrows():
        completion = challenger_query_summary_system(row["inputs"])
        answers.append(completion)

    return answers

# Compute challenger results
challenger_results = mlflow.evaluate(
    challenger_query_iteration,           # iterative function from above
    eval_data.head(50),
    targets="writer_summary",             # column with expected or "good" output
    model_type="text-summarization"       # type of model or task
)

# %% [markdown]
# Let's take a look at our model-level results.

# %%
challenger_results.metrics

# %% [markdown]
# And let's compare in the MLflow UI, looking at the experiment's **Chart** tab.
#
# **Note:** We can filter specifically to ROUGE metrics.

# %% [markdown]
# ### What about other tasks/metrics?
#
# The `mlflow` library contains [a number of LLM task evaluation tools](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.evaluate) that we can use in our workflows.

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
# You should now be able to:
#
# * Obtain reference/benchmark data set for task-specific LLM evaluation
# * Evaluate an LLM's performance on a specific task using task-specific metrics
# * Compare relative performance of two LLMs using a benchmark set

# %% [markdown]
#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
