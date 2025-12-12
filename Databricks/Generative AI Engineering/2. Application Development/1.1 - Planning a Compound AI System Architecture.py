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
# # Planning a Compound AI System Architecture
#
# In this demo, we will plan a compound AI system architecture using pure python. The goal is to define the scope, functionalities and constraints of the system to be developed. 
#
# We will create the system architecture to outline the structure and relationship of each component of the system. At this stage, we need to address the technical challenges and constraints of language model and frameworks to be used. 
#
# **Learning Objectives:**
#
# *By the end of this demo, you will be able to*:
#
# * Apply a class architecture to the stages identified during Decomposition
#
# * Explain a convention that maps stage(s) to class methods
#
# * Plan what method attributes to use when writing a compound application
#
# * Identify various components in a compound app
#

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
# Before starting the demo, **run the following code cells**.

# %%
# %sh
apt-get install -y graphviz

# %%
# %pip install -U --quiet graphviz

dbutils.library.restartPython()

# %%
# %run ../Includes/Classroom-Setup-01

# %% [markdown]
# ## Overview of application
#
# In  notebook 1.1 - Multi-stage Deconstruct we created the sketch of our application below. Now it's time to fill in some of the details about each stage. Approach is more art than science, so this activity, we'll set convention for our planning that we want to define the following method attributes for each of our stages:
#  * **Intent**: Provided from our previous exercise. Keep this around, when you get into actual coding this will be the description part of your docstring, see [PEP-257
# ](https://peps.python.org/pep-0257/).
#  * **Name**: YES! Naming things is hard. You'll get a pass in the exercise because we provide the name for you keep the content organized, but consider how you would have named things. Would you have used the `run_` prefix? Also remember that [PEP-8](https://peps.python.org/pep-0008/#method-names-and-instance-variables) already provides some conventions, specifically:
#      * lowercase with words separated by underscores as necessary to improve readability
#      * Use one leading underscore only for non-public methods and instance variables (not applicable to our exercise here)
#      * Avoid name clashes with subclasses
#  * **Dependencies**: When planning you'll likely already have an idea of approach or libary that you'll need in each stage. Here, you will want to capture those dependencies. After looking at those dependencies you may notice that you'll need more     
#  * **Signature**: These are the argument names and types as well as the output type. However, when working with compound apps it's helpful to have stage methods that are directly tied to an llm type of chat or completion to take the form:
#      * **model_inputs**: These are inputs that will change with each request and are not a configuration setting in the application.
#      * **params**: These are additional arguments we want exposed in our methods, but will likely not be argumented by users once the model is in model serving.
#      * **output**: This is the output of a method and will commonly take the form of the request response of a served model if one is called within the method.
#
#
#  **NOTE**: At this point in planning, you don't necessarily need to get into the decisions about what arguments should be a compound app class entity and which should be maintained as class members.
#
#  **NOTE**: The separation of model_inputs and params is an important one. Compound applications accumulate a lot of parameters that will need to have defaults set during class instantion or load_context calls. By separating those areguments in the planning phase, it will be easier to identify the parameter space that is configurable in you compound application. While not exactly the same, it may be helpful to think of this collection of parameters as hyperparameters - these are configurations will spend time optimizing prior to best application selection, but not set during inference.
#

# %%
displayHTML(html_run_search_1.replace("[SEARCH_GRAPHIC]", get_stage_html('search')))

# %%
displayHTML(html_run_search_2.replace("[SUMMARY_GRAPHIC]", get_stage_html('summary')))

# %%
displayHTML(html_run_search_3.replace("[AUGMENT_GRAPHIC]", get_stage_html('augment')))

# %%
displayHTML(html_run_search_4.replace("[GET_CONTEXT_GRAPHIC]", get_stage_html('get_context')))

# %%
displayHTML(html_run_search_5.replace("[QA_GRAPHIC]", get_stage_html('qa')))

# %%
displayHTML(html_run_search_6.replace("[MAIN_GRAPHIC]", get_stage_html('main')))

# %%
displayHTML(html_run_search_7.replace("[MAIN_GRAPHIC]", get_stage_html('main')))

# %% [markdown]
#
# ## Full Multi-Endpoint Architecture
#
# We've gone through all the work of identifying the dependencies which include both a Data Serving Endpoing and a couple model serving endpoints. We should have a look at what our final architecture is. Even in this straight forward compound application, you can see that it has a lot of endpoint dependencies. It's worth having this perspective to see all the serving endpoints that must be maintained.

# %%
displayHTML(get_multistage_html())

# %% [markdown]
#
# ## Conclusion
#
# In this demo, we planned a sample compound AI system using pure code. This demo showed how different components can be defined independently and then are linked together to build the system.

# %% [markdown]
#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
