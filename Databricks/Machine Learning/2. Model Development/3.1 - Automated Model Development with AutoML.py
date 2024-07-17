# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.3
# ---

#
# <div style="text-align: center; line-height: 0; padding-top: 9px;">
#   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning" style="width: 600px">
# </div>

#
# # Automated Model Development with AutoML
#
# In this demo, we will demonstrate how to initiate AutoML experiments both through the user-friendly AutoML UI and programmatically using the AutoML API. 
#
# **Learning Objectives:**
#
# *By the end of this demo, you will be able to;*
#
# * Start an AutoML experiment via the AutoML UI.
#
# * Start an AutoML experiment via the AutoML API.
#
# * Open and edit a notebook generated by AutoML.
#
# * Identify the best model generated by AutoML based on a given metric.
#
# * Modify the best model generated by AutoML.
#
#

# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **13.3.x-cpu-ml-scala2.12**

#
# ## Classroom Setup
#
# Before starting the demo, run the provided classroom setup script. This script will define configuration variables necessary for the demo. Execute the following cell:

# %run ../Includes/Classroom-Setup-03

# **Other Conventions:**
#
# Throughout this demo, we'll refer to the object `DA`. This object, provided by Databricks Academy, contains variables such as your username, catalog name, schema name, working directory, and dataset locations. Run the code block below to view these details:

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")
print(f"User DB Location:  {DA.paths.datasets}")

#
# ## Prepare Data
#
# For this demonstration, we will utilize a fictional dataset from a Telecom Company, which includes customer information. This dataset encompasses **customer demographics**, including gender, as well as internet subscription details such as subscription plans and payment methods.
#
# A table with all features is already created for you.
#
# **Table name: `customer_churn`**
#
# To get started, execute the code block below and review the dataset schema.

churn_data = spark.sql("SELECT * FROM customer_churn")
display(churn_data)

# ## AutoML Experiment with UI
#
# Databricks AutoML supports experimentation via the UI and the API. Thus, **in the first section of this demos we will demonstrate how to create an experiment using the UI**. Then, we will show to how to create the same experiment via the API.

#
# ### Create AutoML Experiment
#
# Let's initiate an AutoML experiment to construct a baseline model for predicting customer churn. The target field for this prediction will be the `Churn` field.
#
# Follow these step-by-step instructions to create an AutoML experiment:
#
# 1. Navigate to the **Experiments** section in Databricks.
#
#
# 2. Click on **Create AutoML Experiment** located in the top-right corner.
# <img src = "https://files.training.databricks.com/images/automl-create-experiment-v1.png" width = 1000>
#
# 3. Choose a cluster to execute the experiment.
#
# 4. For the ML problem type, opt for **Classification**.
#
#
# 5. Select the **catalog > schema > `customers_churb` table**, which was created in the previous step, as the input training dataset.
#
# 6. Specify **`Churn`** as the prediction target.
#
# 7. Deselect the **CustomerID** field as it's not needed as a feature.
#
# 8. In the **Advanced Configuration** section, set the **Timeout** to **5 minutes**.
#
# 9. Enter a name for your experiment. Let's enter `Churn_Prediction_AutoML_Experiment` as experiment name.
#
# <img src = "https://files.training.databricks.com/images/automl-input-fields-v1.png" >
#
#
# **Optional Advanced Configuration:**
# <img src ="https://files.training.databricks.com/images/automl-advanced-configuration-optional-v1.png"> 
# - You have the flexibility to choose the **evaluation metric** and your preferred **training framework**.
#
# - If your dataset includes a timeseries field, you can define it when splitting the dataset.

#
# ### View the Best Run
#
# Once the experiment is finished, it's time to examine the best run:
#
# 1. Access the completed experiment in the **Experiments** section.
# <img src = "https://files.training.databricks.com/images/automl-completed-experiment-v1.png" width = 1000>
#
# 2. Identify the best model run by evaluating the displayed **metrics**. Alternatively, you can click on **View notebook for the best model** to access the automatically generated notebook for the top-performing model.
# <img src ="https://files.training.databricks.com/images/automl-metrics-v1.png" width = 1000>
#
# 3. Utilize the **Chart** tab to compare and contrast the various models generated during the experiment.
#
# You can find all details for the run  on the experiment page. There are different columns such as the framework used (e.g., `Scikit-Learn`, `XGBoost`), evaluation metrics (e.g., `Accuracy`, `F1 Score`), and links to the corresponding notebooks for each model. This allows you to make informed decisions about selecting the best model for your specific use case.

# ### View the Notebook
#
# ####**Instruction for viewing the notebook of the best run:**
#
#
#
# + **Click on the `"View notebook for best model"` link.**
#
# + **Review the notebook that created the best model.**
#
# <img src ="https://files.training.databricks.com/images/automl-best-model-notebook-v1.png" width= 1000>
#
#
# + **Edit the notebook as required.**
#     + Identify the best model generated by AutoML based on a given metric and modify it as needed. The best model details, including the associated run ID, can be found in the MLflow experiment logs. Use the run ID to load the best model, make modifications, and save the modified model for deployment or further use. 

# ## AutoML Experiment with API
#
# In this section we will use AutoML API to start and AutoML job and retreive the experiment results.

# ### Start an Experiment

from databricks import automl
from datetime import datetime
automl_run = automl.classify(
    dataset = spark.table("customer_churn"),
    target_col = "Churn",
    exclude_cols=["CustomerID"], # Exclude columns as needed
    timeout_minutes = 5
) 

# ### Search for the Best Run
#
# The search for the best run in this experiment, we need to first **get the experiment ID** and then **search for the runs** by experiment. 

import mlflow
# Get the experiment path by experiment ID
exp_path = mlflow.get_experiment(automl_run.experiment.experiment_id).name
# Find the most recent experiment in the AutoML folder
filter_string=f'name LIKE "{exp_path}"'
automl_experiment_id = mlflow.search_experiments(
  filter_string=filter_string,
  max_results=1,
  order_by=["last_update_time DESC"])[0].experiment_id


# +
from mlflow.entities import ViewType

# Find the best run ...
automl_runs_pd = mlflow.search_runs(
  experiment_ids=[automl_experiment_id],
  filter_string=f"attributes.status = 'FINISHED'",
  run_view_type=ViewType.ACTIVE_ONLY,
  order_by=["metrics.val_f1_score DESC"]
)
# -

#
# **Print information about the best trial from the AutoML experiment.**
#

print(automl_run.best_trial)

# **Explanation**
#
#
# - **`print(automl_run.best_trial)`**: This prints information about the best trial or run from the AutoML experiment.
#
#     - **Model:** Specifies the machine learning model that performed the best. 
#
#     - **Model path:** The MLflow artifact URL of the model trained in this trial.
#
#     - **Preprocessors:** Description of the preprocessors run before training the model.
#
#     - **Training duration:** Displays the duration it took to train the best model.
#
#     - **Evaluation metric score:** Shows the value of the evaluation metric used to determine the best model. 
#
#     - **Evaluation metric:** Score of primary metric, evaluated for the validation dataset.

# **Import notebooks for other runs in AutoML.**
#
# For classification and regression experiments, AutoML generated notebooks for data exploration and the best trial in your experiment are automatically imported to your workspace. Generated notebooks for other experiment trials are saved as MLflow artifacts on DBFS instead of auto-imported into your workspace. 
#
# For all trials besides the best trial, the **`notebook_path`** and **`notebook_url`** in the TrialInfo Python API are not set. If you need to use these notebooks, you can manually import them into your workspace with the AutoML experiment UI or the **`automl.import_notebook`** Python API.
#
# **🚨 Notice:** `destination_path` takes Workspace as root.

# +
# Create the Destination path for storing the best run notebook
destination_path = f"/Users/{DA.username}/imported_notebooks/demo-3.1-{datetime.now().strftime('%Y%m%d%H%M%S')}"

# Get the path and url for the generated notebook
result = automl.import_notebook(automl_run.trials[5].artifact_uri, destination_path)
print(f"The notebook is imported to: {result.path}")
print(f"The notebook URL           : {result.url}")
# -

#
# ## Clean up Classroom
#
# Run the following cell to remove lessons-specific assets created during this lesson.

DA.cleanup()

#
# ## Conclusion
#
# In this demo, we show how to use AutoML UI and AutoML API for creating classification model and how we can retrieve the best run and access the generated notebook, and how we can modify the parameters of the best model. 

# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
