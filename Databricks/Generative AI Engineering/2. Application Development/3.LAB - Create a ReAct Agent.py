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
# # LAB - Create a ReAct Agent
#
# In this lab we will create a virtual stock advisor agent using that uses the **ReAct** prompting. This agent will reason and act based on the prompts and tools provided. 
#
# Of course, the agent is build for demonstration purposes and it the answers shouldn't be used as investment advise! 
#
#
# **Lab Outline:**
#
# In this lab, you will need to complete the following tasks;
#
# * **Task 1 :** Define the agent brain
#
# * **Task 2 :** Define the agent tools
#
# * **Task 3 :** Define an agent logic
#
# * **Task 4 :** Create the agent 
#
# * **Task 5 :** Run the agent
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
# Before starting the lab, run the provided classroom setup scripts. These scripts will install the required libraries and configure variables which are needed for the lab.

# %%
# %pip install --upgrade --quiet langchain==0.2.11 langchain_community==0.2.10 yfinance==0.2.41 wikipedia==1.4.0 youtube-search mlflow==2.14.3

dbutils.library.restartPython()

# %%
# %run ../Includes/Classroom-Setup-LAB

# %%
import mlflow
mlflow.langchain.autolog()

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
# ## Task 1: Define the Brain of the Agent
#
# Let's start by defining the agent brain using one of the available LLMs on Databricks.
#
# * For this lab, use **databricks-dbrx-instruct** 
#
# * Define the maximum number of tokens

# %%
from langchain.agents import AgentType, initialize_agent
from langchain_community.chat_models import ChatDatabricks

# define the brain
llm_dbrx = <FILL_IN>

# %%
# let's test the brain
llm_dbrx.invoke("Hi! How are you?")

# %% [markdown]
# ## Task 2 : Define Tools that the Agent Will Use
#
# For an agent the toolset is a crucial component to complete the task define. The agent will reason for the next action to take and an appropriate tool will be used to complete the action.
#
# For our stock advisor agent, we will use following tools;
#
# * **Wikipedia tool**: For searching company details. [[LangChain Doc](https://python.langchain.com/docs/integrations/tools/wikipedia/)]
#
# * **YahooFinance News tool**: This will be used for aggregating latest news about a stock. [[LangChain Doc](https://python.langchain.com/docs/integrations/tools/yahoo_finance_news/)]
#
# * **YouTube search tool**: This will be used to search for review videos about the latest financial reports. [[LangChain Doc](https://python.langchain.com/docs/integrations/tools/youtube/)]

# %% [markdown]
# ### Wikipedia Tool

# %%
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

api_wrapper = <FILL_IN>
tool_wiki = <FILL_IN>

# %% [markdown]
# ### YahooFinance News Tool

# %%
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool

tool_finance = <FILL_IN>

# %% [markdown]
# ### YouTube Search Tool

# %%
from langchain_community.tools import YouTubeSearchTool

tool_youtube = <FILL_IN>

# %% [markdown]
# ### Define Toolset
#
# Next, add all tools together to be used in the next step.

# %%
tools = <FILL_IN>

# %% [markdown]
# ## Tasks 3: Define Agent Logic
#
# Agent needs a planning logic while doing reasoning and defining actions. Here you will use a common LangChain prompt template.

# %%
template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

# %%
from langchain.prompts import PromptTemplate

prompt = <FILL_IN>

# %% [markdown]
# ## Task 4: Create the Agent
#
# The final step is to create the agent using the LLM, planning prompt and toolset.

# %%
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent

agent = <FILL_IN>
agent_exec  = <FILL_IN>

# %% [markdown]
# ## Task 5: Run the Agent
#
# Let's test the agent!
#
# **Use this prompt:**
# <blockquote>
# What do you think about investing in Apple stock? Provide an overview of the latest news about the company. Next, search a video on YouTube which reviews Apple's latest financials. 
#
# Format the final answer as HTML.
# </blockquote>
#

# %%
response = <FILL_IN>
displayHTML(response["output"])

# %% [markdown]
# It seems like the agent uses company name only when searching for videos. **Let's play with the prompt to get better results.**
#
# In real-world, the agent would be used in a conversational way and we would just chat with the agent to tweak the search query or to adjust the response in a desired format. 
#
# **Use this prompt:**
# <blockquote>
# What do you think about investing in Apple stock? Provide an overview of the latest news about the company. Next, search a video on YouTube which reviews Apple's latest financials.
#
# When searching on YouTube use such as "Apple  stock finance investment earnings valuation".
#
# Write a nice summary of the results.
#
# Format the final answer as HTML.
# </blockquote>

# %%
response = <FILL_IN>
displayHTML(response["output"])

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
# In this lab, you successfully created a virtual stock advisor agent using the ReAct prompting framework. By defining the agent's brain, tools, logic, and execution flow, you demonstrated how the agent can interact with various data sources to provide investment insights.

# %% [markdown]
#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
