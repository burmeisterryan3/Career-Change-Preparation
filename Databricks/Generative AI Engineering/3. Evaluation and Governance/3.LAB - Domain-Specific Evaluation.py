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
# # LAB - Domain-Specific Evaluation 
#
#
# In this lab, you will have the opportunity to evaluate a large language model on a specific task **using a dataset designed for this exact evaluation.**
#
# **Lab Outline:**
#
# *In this lab, you will need to complete the following tasks:*
#
# - **Task 1:** Create a Benchmark Dataset
# - **Task 2:** Compute ROUGE on Custom Benchmark Data
# - **Task 3:** Use an LLM-as-a-Judge approach to evaluate custom metrics

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
# %pip install mlflow==2.12.1 evaluate==0.4.1 databricks-sdk==0.28.0 rouge_score
dbutils.library.restartPython()

# %% [markdown]
# Before starting the Lab, run the provided classroom setup script. This script will define configuration variables necessary for the lab. Execute the following cell:

# %%
# %run ../Includes/Classroom-Setup-03

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
# # Lab Overview
#
# In this lab, you will again be evaluating the performance of an AI system designed to summarize text.

# %%
query_product_summary_system(
    "This is the best frozen pizza I've ever had! Sure, it's not the healthiest, but it tasted just like it was delivery from our favorite pizzeria down the street. The cheese browned nicely and fresh tomatoes are a nice touch, too! I would buy it again despite it's high price. If I could change one thing, I'd made it a little healthier – could we get a gluten-free crust option? My son would love that."
)

# %% [markdown]
# However, you will evaluate the LLM using a curated benchmark set specific to our evaluation.
#
# This lab will follow the below steps:
#
# 1. Create a custom benchmark dataset specific to the use case
# 2. Compute summarization-specific evaluation metrics using the custom benchmark data set
# 3. Use an LLM-as-a-Judge approach to evaluate custom metrics

# %% [markdown]
# ## Task 1: Create a Benchmark Dataset
#
# Recall that ROUGE requires reference sets to compute scores. In our demo, we used a large, generic benchmark set.
#
# In this lab, you have to use a domain-specific benchmark set specific to the use case.
#
# ### Case-Specific Benchmark Set
#
# While the base-specific data set likely won't be as large, it does have the advantage of being **more representative of the task we're actually asking the LLM to perform.**
#
# Below, we've started to create a dataset for grocery product review summaries. It's your task to create **two more** product summaries to this dataset.
#
# **Hint:** Try opening up another tab and using AI Playground to generate some examples! Just be sure to manually check them since this is our *ground-truth evaluation data*.
#
# **Note:** For this task, we're creating an *extremely small* reference set. In practice, you'll want to create one with far more example records.

# %%

import pandas as pd

eval_data = pd.DataFrame(
    {
        "inputs": [
            "This coffee is exceptional. Its intensely bold flavor profile is both nutty and fruity – especially with notes of plum and citrus. While the price is relatively good, I find myself needing to purchase bags too often. If this came in 16oz bags instead of just 12oz bags, I'd purchase it all the time. I highly recommend they start scaling up their bag size.",
            "The moment I opened the tub of Chocolate-Covered Strawberry Delight ice cream, I was greeted by the enticing aroma of fresh strawberries and rich chocolate. The appearance of the ice cream was equally appealing, with a swirl of pink strawberry ice cream and chunks of chocolate-covered strawberries scattered throughout. The first bite did not disappoint. The strawberry ice cream was creamy and flavorful, with a natural sweetness that was not overpowering. The chocolate-covered strawberries added a satisfying crunch fruity bite.",
            "Arroz Delicioso is a must-try for Mexican cuisine enthusiasts! This authentic Mexican rice, infused with a blend of tomatoes, onions, and garlic, brings a burst of flavor to any meal. Its vibrant color and delightful aroma will transport you straight to the heart of Mexico. The rice cooks evenly, resulting in separate, fluffy grains that hold their shape, making it perfect for dishes like arroz con pollo or as a side for tacos. With a cook time of just 20 minutes, Arroz Delicioso is a convenient and delicious addition to your pantry. Give it a try and elevate your Mexican food game!",
            "FreshCrunch salad mixes are revolutionizing the way we think about packaged salads! Each bag is packed with a vibrant blend of crisp, nutrient-rich greens, including baby spinach, arugula, and kale. The veggies are pre-washed and ready to eat, making meal prep a breeze. FreshCrunch sets itself apart with its innovative packaging that keeps the greens fresh for up to 10 days, reducing food waste and ensuring you always have a healthy option on hand. The salad mixes are versatile and pair well with various dressings and toppings. Try FreshCrunch for a convenient, delicious, and nutritious meal solution that doesn't compromise on quality or taste!",
            <FILL_IN>,
            <FILL_IN>
        ],
        "ground_truth": [
            "This bold, nutty, and fruity coffee is delicious, and they need to start selling it in larger bags.",
            "Chocolate-Covered Strawberry Delight ice cream looks delicious with its aroma of strawberry and chocolate, and its creamy, naturally sweet taste did not disappoint.",
            "Arroz Delicioso offers authentic, flavorful Mexican rice with a blend of tomatoes, onions, and garlic, cooking evenly into separate, fluffy grains in just 20 minutes, making it a convenient and delicious choice for dishes like arroz con pollo or as a side for tacos.",
            "FreshCrunch salad mixes offer convenient, pre-washed, nutrient-rich greens in an innovative packaging that keeps them fresh for up to 10 days, providing a versatile, tasty, and waste-reducing healthy meal solution.",
            <FILL_IN>,
            <FILL_IN>
        ],
    }
)

display(eval_data)

# %% [markdown]
# **Question:** What are some strategies for evaluating your custom-generated benchmark data set? For example:
# * How can you scale the curation?
# * How do you know if the ground truth is correct?
# * Who should have input?
# * Should it remain static over time?
#
# Next, we're saving this reference data set for future use.

# %%
spark_df = spark.createDataFrame(eval_data)
spark_df.write.mode("overwrite").saveAsTable(f"{DA.catalog_name}.{DA.schema_name}.case_spec_summ_eval")


# %% [markdown]
# ## Task 2: Compute ROUGE on Custom Benchmark Data
#
# Next, we will want to compute our ROUGE-N metric to understand how well our system summarizes grocery product reviews based on the reference of reviews that was just created.
#
# Remember that the `mlflow.evaluate` function accepts the following parameters for this use case:
#
# * An LLM model
# * Reference data for evaluation
# * Column with ground truth data
# * The model/task type (e.g. `"text-summarization"`)
#

# %% [markdown]
# ### Step 2.1: Run the Evaluation
#
# Instead of using the generic benchmark dataset like in the demo, your task is to **compute ROUGE metrics using the case-specific benchmark data that we just created.**
#
# **Note:** If needed, refer back to the demo to complete the below code blocks.
#
# First, the function that you can use to iterate through rows for `mlflow.evaluate`.

# %%

# A custom function to iterate through our eval DF
def query_iteration(inputs):
    answers = []

    for index, row in inputs.iterrows():
        <FILL_IN>

    return answers

# Test query_iteration function – it needs to return a list of output strings
query_iteration(eval_data)

# %% [markdown]
# Next, use the above function and `mlflow.evaluate` to perform the `text-summarization` evaluation.

# %%

import mlflow

# Evaluate with a custom function
results = <FILL_IN>

# %% [markdown]
# ### Step 2.2: Evaluate the Results
#
# Next, take a look at the results.

# %%

display(results<FILL_IN>)

# %% [markdown]
# **Question:** How do we interpret these results? What does it tell us about the summarization quality? About our LLM?
#
# Next, compute the summarized metrics to view the performance of the LLM on the entire dataset.

# %%
<FILL_IN>

# %% [markdown]
# **Bonus:** Take a look at the results in the Experiment Tracking UI.
#
# Do you see any summaries that you think are particularly good or problematic?

# %% [markdown]
# ## Task 3: Use an LLM-as-a-Judge Approach to Evaluate Custom Metrics
#
# In this task, you will define and evaluate a custom metric called "professionalism" using an LLM-as-a-Judge approach. The goal is to assess how professionally written the summaries generated by the language model are, based on a set of predefined criteria.
#

# %% [markdown]
# ### Step 3.1: Define a Humor Metric
#
# - Define humor and create a grading prompt.
#
#   **To Do:**
#
#   For this task, you are provided with an initial example of humor (humor_example_score_1). Your task is to generate another evaluation example (humor_example_score_2). 
#
#   **Hint:** You can use AI Playground for this. Ensure that the generated example is relevant to the prompt and reflects a different humor score. Manually verify the generated example to ensure its correctness.
#

# %%

# Define an evaluation example for humor with a score of 2
humor_example_score_1 = mlflow.metrics.genai.EvaluationExample(
    input="Tell me a joke!",  
    output=(
        "Why don't scientists trust atoms? Because they make up everything!"  
    ),
    score=2,  # Humor score assigned to the output
    justification=(
        "The joke uses a common pun and is somewhat humorous, but it may not elicit strong laughter or amusement from everyone."  # Justification for the assigned score
    ),
)

# Define another evaluation example for humor with a score of 4
humor_example_score_2 = <FILL_IN>
    input=<FILL_IN>,  
    output=(
        <FILL_IN> 
    ),
    score=<FILL_IN>  # Humor score assigned to the output
    justification=(
        <FILL_IN>
         # Justification for the assigned score
    ),
)

# %% [markdown]
# ### Step 3.2: LLM-as-a-Judge to Compare Metric
#
# * **3.2.1:  Create a metric for comparing the responses for humor**
#
#   Define a custom metric to evaluate the humor in generated responses. This metric will assess the level of humor present in the responses generated by the language model.

# %%

# Define the metric for the evaluation
comparison_humor_metric = mlflow.metrics.genai.make_genai_metric(
    name="comparison_humor",
    definition=(
        "Humor refers to the ability to evoke laughter, amusement, or enjoyment through cleverness, wit, or unexpected twists."
    ),
    grading_prompt=(
        "Humor: If the response is funny and induces laughter or amusement, below are the details for different scores: "
        "- Score 1: The response attempts humor but falls flat, eliciting little to no laughter or amusement."
        "- Score 2: The response is somewhat humorous, eliciting mild laughter or amusement from some individuals."
        "- Score 3: The response is moderately funny, eliciting genuine laughter or amusement from most individuals."
        "- Score 4: <FILL_IN>"
        "- Score 5: <FILL_IN>"
    ),
    # Examples for humor
    examples=[
        <FILL_IN>
    ],
    model="endpoints:/databricks-dbrx-instruct",
    parameters={"temperature": 0.0},
    aggregations=["mean", "variance"],
    greater_is_better=True,
)

# %% [markdown]
# * **3.2.3: Generate data with varying humor levels**
#
#   Add input prompts and corresponding output responses with different levels of humor. 
#   
#   **Hint:** You can utilize AI playgrounds to generate these values.

# %%
# Define testing data with different humor scores for comparison
humor_data = pd.DataFrame(
    {
        "inputs": [
            
            <FILL_IN>
        ],
        "ground_truth": [
            <FILL_IN>
        ],
    }
)

# %% [markdown]
# * **3.2.4: Evaluate the Comparison**
#
#   Next, evaluate the comparison between the responses generated by the language model. This evaluation will provide you with a metric for assessing the professionalism of the generated summaries based on predefined criteria.
#

# %%
benchmark_comparison_results = <FILL_IN>

# %% [markdown]
# * **3.2.5: View Comparison Results**
#
#   Now, let's take a look at the results of the comparison between the responses generated by the language model. This comparison provides insights into the professionalism of the generated summaries based on the predefined criteria.
#

# %%
display(benchmark_comparison_results.<FILL_IN>)

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
# This lab provided a hands-on experience in creating and evaluating a custom benchmark dataset, computing task-specific evaluation metrics, and leveraging an LLM-as-a-Judge approach to assess custom metrics. These techniques are essential for evaluating the performance of AI systems in domain-specific tasks and ensuring their effectiveness in real-world applications.

# %% [markdown]
#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
