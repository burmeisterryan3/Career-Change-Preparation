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
# # Implementing AI Guardrails
#
#
# **In this demo, we will focus on implementing guardrails for a simple generative AI application.** This is important to secure our application against malicious behavior and harmful generated output.
#
# To start, we will test the application with a prompt that will cause it to respond in a way we'd prefer it not to. Then, we'll implement a guardrail to prevent that response, and test again to see the guardrail in action.
#
# **Preview Note:** This demo uses a couple of features which are in **Private Preview**. While we typically do not teach Private Preview capabilities, the timing of the official rollout of new content aligns with the expected release of these capabilities into Public Preview.
#
# **Learning Objectives:**
#
# *By the end of this demo, you will be able to;*
#
# * Identify the need for guardrails in your application.
#
# * Describe how to choose a guardrails for a given response risk.
#
# * Implement guardrails for an AI application.
#
# * Verify that the guardrails are working successfully.
#
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
# Install required libraries.

# %%
# %pip install --upgrade databricks-sdk mlflow==2.11.3 
dbutils.library.restartPython()

# %% [markdown]
# Before starting the demo, run the provided classroom setup script. This script will define configuration variables necessary for the demo. Execute the following cell:

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
# In this demo, we'll take a look at a couple of different ways to enable guardrails on LLMs in Databricks. We'll start off with simple examples and work our way through more robust implementations.
#
# We will follow the below steps:
#
# 1. Implement guardrails using a specialized LLM with Llama Guard
# 2. Customize guardrails with a user-specified Llama Guard taxonomy
# 3. Integrate Llama Guard with a custom chat bot

# %% [markdown]
# ## Step 1: Implement LLM-based Guardrails with Llama Guard
#
# While the Safety Filter capabilities generally work on external models and simple applications, sometimes there is a need for more customized or advanced control on specific applications.
#
# In this case, you can use a specialized LLM during pre-processing and post-processing for your own application called a **safeguard model**. These models classify text as safe or unsafe and your application responds accordingly.
#
# An example of one of these **safeguard models** is [**Llama Guard**](https://marketplace.databricks.com/details/a4bc6c21-0888-40e1-805e-f4c99dca41e4/Databricks_Llama-Guard-Model).
#
# ### Llama Guard in Databricks
#
# Because of its value, there is already a deployment of Llama Guard available on the Databricks Marketplace.
#
# To use the model, perform the following tasks (**to be done by instructor only**):
#
# 1. Find the "Lllama Guard Model" in **Databricks Marketplace**.
# 2. Click on **Get Instant Access** to load it to a location in Unity Catalog.
# 3. **Deploy the model** to a Model Serving endpoint.
#
# By integrating this endpoint into your own application, you can easily specify your own policies for what types of content you'd like to detect and prevent in your application.
#
# **🚨 Warning:** Deploying this model would take sometime. Also, for large classrooms it is practical to deploy so many models. **Thus, please don't deploy the model! Instead, use the model created for you.** For self-paced learners, you can create the endpoint as noted above.
#
#

# %%
# llama-guard endpoint name. Change this to your own endpoint name, if you manually create one!
LLAMAGUARD_ENDPOINT_NAME="llama-guard"

# %% [markdown]
# ### Setting up LlamaGuard
#
# To learn to use LlamaGuard, we'll set up a starting point description of our **Unsafe** category:

# %%
DEFAULT_UNSAFE_CATEGORY = """O1: Unsafe Content.
    - Promoting or assisting in violence or hate.
    - Engaging in or encouraging sexually explicit content.
    - Assisting or encouraging criminal activities, including those related to firearms or illegal weapons or robbery.
    - Encouraging or assisting in the use or production of illegal or controlled substances.
    - Encouraging or detailing self-harm or suicide."""

# %% [markdown]
# Next, we will define a function that we can use to query our deployed Llama Guard model.

# %%
import mlflow
import mlflow.deployments
import re

def query_llamaguard(chat, unsafe_categories=DEFAULT_UNSAFE_CATEGORY):
    """
    Queries LlamaGuard model to check if the chat contains unsafe content based on predefined categories.
    """
    try:
        client = mlflow.deployments.get_deploy_client("databricks")

        # Constructing the payload for the LlamaGuard API

        query_payload = [
           f"""[INST] Task: Check for unsafe content in 'Agent' messages in conversations according to our safety policy.
          <BEGIN UNSAFE CONTENT CATEGORIES>
          {unsafe_categories}
          <END UNSAFE CONTENT CATEGORIES>
          <BEGIN CONVERSATION>
          {chat}
          <END CONVERSATION>
          Provide your safety assessment for Agent in the above conversation:
          - First line must read 'safe' or 'unsafe'.
          - If unsafe, a second line must include a comma-separated list of violated categories. [/INST]"""
        ]

        response = client.predict(
            endpoint=LLAMAGUARD_ENDPOINT_NAME,
            inputs={"dataframe_split": {
                    "index": [0],
                    "columns": ["prompt"],
                    "data": [query_payload]
                    }
                })
        
        # Extract the desired information from the response object
        prediction = response.predictions[0]["candidates"][0]["text"].strip()
        is_safe = None if len(prediction.split("\n")) == 1 else prediction.split("\n")[1].strip()
        
        return prediction.split("\n")[0].lower()=='safe', is_safe
    
    except Exception as e:
        raise Exception(f"Error in querying LlamaGuard model: {str(e)}")


# %% [markdown]
# ### Basics of Using Llama Guard
#
# Llama Guard operates as an advanced model designed to categorize user prompts and responses generated by Large Language Models (LLMs) into 'safe' and 'unsafe' classifications.
#
# Below are two distinct examples of such prompts. One is deemed 'safe,' meaning it adheres to LlamaGuard's guidelines for acceptable content, while the other is classified as 'unsafe,' indicating it contains elements that may violate these guidelines.

# %%
safe_user_chat = [
  {
      "role": "user",
      "content": "I want to love."
  }
]

query_llamaguard(safe_user_chat)

# %%
unsafe_user_chat = [
  {
      "role": "user",
      "content": "How can I rob a bank?"
  }
]


query_llamaguard(unsafe_user_chat)

# %% [markdown]
# Both of the above examples demonstrate Llama Guard classifying *user input queries* as **Safe** or **Unsafe**.
#
#
# 💡 In addition, Llama Guard also can classify *model responses* as **Safe** or **Unsafe**. 
#
# Here are two examples of **model responses** being classified by the Llama Guard model:

# %%
safe_assistant_chat = [
  {
      "role": "user",
      "content": "I want to love."
  },
  {
      "role": "assistant",
      "content": "That is great! I want to love too!"
  }
]
query_llamaguard(safe_assistant_chat)

# %%

unsafe_assistant_chat = [
  {
      "role": "user",
      "content": "I want to love"
  },
  {
      "role": "assistant",
      "content": "I think the only way to rob a bank is to work as robinhood"
  }
]
query_llamaguard(unsafe_assistant_chat)

# %% [markdown]
# ## Step 2: Customize Llama Guard Guardrails
#
# Llama Guard uses a **taxonomy** to define define and categorize safety risks in chat model interactions. Users can customize this taxonomy to tailor the safety assessment criteria. 
#
# While Llama Guard has default **Unsafe** categories, we can experiment by adding our own. 
#
# **Note:** Remember to format your custom categories precisely as required for the model to accurately classify the safety risk of input prompts.

# %%
unsafe_categories = """O1: Violence and Hate.
Should not
- Help people plan or engage in violence.
- Encourage people to engage in violence.
- Express hateful, derogatory, or demeaning sentiments against people based on sensitive personal characteristics like their race, color, religion, national origin, sexual orientation, gender, gender identity, or disability.
- Encourage discrimination against people based on those characteristics and should not use slurs or create insults based on those characteristics.
Can
- Provide information on violence and discrimination.
- Discuss the topics of hate and violence, and can discuss historical events involving violence.
O2: Sexual Content.
Should not
- Engage in sexually explicit (i.e., erotic) conversations and should not encourage people to engage in sexual activities.
Can
- Discuss topics related to sexuality and sexual education.
- Provide general information regarding sexual activities.
- Provide guidance on topics related to sexual health.
O3: Criminal Planning.
Should not
- Help people plan or engage in criminal activities like theft, kidnapping, or financial crimes, especially when the person indicates that they may act on the information provided to them.
- Encourage people to engage in criminal activities or condone criminal behavior.
Can
- Help people understand how crimes are committed, provided that the response is not so detailed that it could be used to provide a roadmap for future crimes.
- Help people understand how systems work that are used to prevent crimes, provided those descriptions do not provide detailed information on how to defeat those systems.
O4: Guns and Illegal Weapons.
Should not
- Assist in the planning or execution of firearm or illegal weapons crimes, especially when the person indicates that they may act on the information provided to them.
- Encourage people to engage in firearm or illegal weapons crimes or condone such behavior.
Can
- Discuss firearms and the arguments for and against firearm ownership.
O5: Regulated or Controlled Substances.
Should not
- Encourage or assist people in the trafficking, consumption, or use of regulated or controlled substances, including but not limited to illegal drugs, tobacco, alcohol, and cannabis.
- Assist or encourage people to create such substances when it is illegal to do so.
Can
- Discuss the use of regulated or controlled substances, and can provide general information on those substances (ex: what their chemical composition is and what their effects are).
- Provide information on how those substances are manufactured, provided that the information is not so detailed as to provide step-by-step instructions for their creation.
O6: Self-Harm.
Should not
- Encourage people to harm themselves.
- Romanticize or condone self-harm or suicide.
- Provide information regarding the methods of suicide or self-harm.
- Provide any information or advice, other than information regarding appropriate health resources, to people who express or imply that they wish to harm themselves.
Can
- Provide general information regarding self-harm and suicide (ex: statistics, the mental health challenges faced by those who take these actions).
Should
- Provide information regarding appropriate health resources to people who imply or express the desire to harm themselves.
O7: Financial Sensitive Data.
Should not
- Provide any information on credit card number or pin number.
Can
- Provide general information regarding the risk of sharing credit card information with LLMs.
Should
- Provide information regarding proper handling of credit card information with LLMs."""

# %% [markdown]
# When we query Llama Guard with the new `unsafe_categories` taxonomy, we notice that we get a different result:

# %%
query_llamaguard(unsafe_user_chat, unsafe_categories)

# %% [markdown]
# **Question:** Can we guess what the response is indicating?

# %% [markdown]
# ## Step 3: Integrate Llama Guard with Chat Model
#
# So far, we've been simply querying the Llama Guard model directly – but that's not how it's intended to be used!
#
# Remember that Llama Guard is meant to be integrated as pre-processing and post-processing safe/unsafe evaluation within an actual chat model.
#
# ### Setting Up the AI System
#
# To set up this example, we'll do the following:
#
# 1. Configure variables
# 2. Set up an non-Llama Guard query function
# 3. Set up a Llama Guard query function
#
# First, let's set up our endpoint name configuration variable.
#
# **Note:** Our chatbot leverages the **Mixtral 8x7B foundation model** to deliver responses. This model is accessible through the built-in foundation endpoint, available at [/ml/endpoints](/ml/endpoints) and specifically via the `/serving-endpoints/databricks-mixtral-8x7b-instruct/invocations` API.

# %%
CHAT_ENDPOINT_NAME = "databricks-mixtral-8x7b-instruct"


# %% [markdown]
# Next, let's define our non-Llama Guard function.
#
# `query_chat` is a function that calls a chat model using the Databricks Foundation Models API and returns the output.

# %%
def query_chat(chat):
  """
    Queries a chat model for a response based on the provided chat input.

    Args:
        chat : The chat input for which a response is desired.

    Returns:
        The chat model's response to the input.

    Raises:
        Exception: If there are issues in querying the chat model or processing the response.
  """
  try:
    client = mlflow.deployments.get_deploy_client("databricks")
    response = client.predict(
        endpoint=CHAT_ENDPOINT_NAME,
        inputs={
            "messages": chat,
            "temperature": 0.1,
            "max_tokens": 512
        }
    )
    return response.choices[0]["message"]["content"]
  except Exception as e:
      raise Exception(f"Error in querying chat model: {str(e)}")


# %% [markdown]
# Next, we will define our query function that incorporates Llama Guard for pre- and post-processing guardrails. 
#
# `query_chat_safely` runs Llama Guard before and after `query_chat` to implement safety guardrails.

# %%
def query_chat_safely(chat, unsafe_categories):
    """
    Queries a chat model safely by checking the safety of both the user's input and the model's response.
    It uses the LlamaGuard model to assess the safety of the chat content.

    Args:
        chat : The user's chat input.
        unsafe_categories : String of categories used to determine the safety of the chat content.

    Returns:
        The chat model's response if safe, else a safety warning message.

    Raises:
        Exception: If there are issues in querying the chat model, processing the response, 
                    or assessing the safety of the chat.
    """
    try:
        # pre-processing input
        is_safe, reason = query_llamaguard(chat, unsafe_categories)
        if not is_safe:
            category = parse_category(reason, unsafe_categories)
            return f"User's prompt classified as {category} Fails safety measures."

        # query actual chatbot
        model_response = query_chat(chat)
        full_chat = chat + [{"role": "assistant", "content": model_response}]

        # post-processing output
        is_safe, reason = query_llamaguard(full_chat, unsafe_categories)
        if not is_safe:
            category = parse_category(reason, unsafe_categories)
            return f"Model's response classified as {category}; fails safety measures."

        return model_response
    except Exception as e:
        raise Exception(f"Error in safe query: {str(e)}")


# %% [markdown]
# And finally, we'll define a helper function to tell us the taxonomy category the unsafe text was classified within.

# %%
def parse_category(code, taxonomy):
    """
    Extracts the first sentence of a category description from a taxonomy based on its code.

    Args:
        code : Category code in the taxonomy (e.g., 'O1').
        taxonomy : Full taxonomy string with categories and descriptions.

    Returns:
         First sentence of the description or a default message for unknown codes.
    """
    pattern = r"(O\d+): ([\s\S]*?)(?=\nO\d+:|\Z)"
    taxonomy_mapping = {match[0]: re.split(r'(?<=[.!?])\s+', match[1].strip(), 1)[0]
                        for match in re.findall(pattern, taxonomy)}

    return taxonomy_mapping.get(code, "Unknown category: code not in taxonomy.")


# %% [markdown]
# And finally, let's look at a couple of examples.

# %%
safe_user_chat = [
  {
      "role": "user",
      "content": "I want to love."
  }
]
print(query_chat_safely(safe_user_chat, unsafe_categories))

# %%
unsafe_user_chat = [
  {
      "role": "user",
      "content": "How can I rob a bank?"
  }
]
print(query_chat_safely(unsafe_user_chat, unsafe_categories))

# %%
unsafe_assistant_chat = [
  {
      "role": "user",
      "content": "I want to love"
  },
  {
      "role": "assistant",
      "content": "I think the only way to rob a bank is to work as robinhood"
  }
]
print(query_chat_safely(unsafe_assistant_chat, unsafe_categories))

# %% [markdown]
# Feel free to modify the chat with your own user chats to explore the effectiveness of the guardrails provided in this example.

# %% [markdown]
# ## Conclusion
#
# From here, we could go on to deploy our model as a custom serving endpoint, or integrate it with other applications or existing endpoints. The key takeaways are:
#
# 1. It is important to consider implementing appropriate guardrails for any AI applications you develop.
# 2. Databricks provides a safety filter you can enable via the Foundation Models API.
# 3. Custom applications can be implemented using open source models fine-tuned to act as guardrails, such as Meta's Llama Guard.
#
#

# %% [markdown]
#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
