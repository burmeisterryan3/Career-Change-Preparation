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
# # LAB - Hyperparameter Tuning with Hyperopt
#
# Welcome to the Hyperparameter Tuning with Hyperopt lab! In this hands-on session, you'll gain practical insights into **optimizing machine learning models using Hyperopt**. Throughout the lab, we'll cover key steps, from loading the dataset and creating training/test sets to **defining a hyperparameter search space and running optimization trials with Spark**. The primary objective is to equip you with the skills to fine-tune models effectively using Spark, hyperopt and MLflow.
#
# **Lab Outline:**
# 1. Load the dataset and create training/test sets.
#
# 1. Define the hyperparameter search space for optimization.
#
# 1. Define the optimization function to fine-tune the model.
#
# 1. Run hyperparameter tuning trials using Spark.
#
# 1. Show the best run's info.
#
# 1. Search for runs using the MLflow API.
#
# 1. Search for runs using the MLflow UI.

# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **13.3.x-cpu-ml-scala2.12**

#
# ## Classroom Setup
#
# Before starting the demo, run the provided classroom setup script. This script will define configuration variables necessary for the demo. Execute the following cell:

# %run ../Includes/Classroom-Setup-02.LAB

# **Other Conventions:**
#
# Throughout this demo, we'll refer to the object `DA`. This object, provided by Databricks Academy, contains variables such as your username, catalog name, schema name, working directory, and dataset locations. Run the code block below to view these details:

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")
print(f"Dataset Location:  {DA.paths.datasets}")

# ## Prepare Dataset
#
# In this lab you will be using a fictional dataset from a Telecom Company, which includes customer information. This dataset encompasses **customer demographics**, including gender, as well as internet subscription details such as subscription plans and payment methods.
#
# In this lab will create and tune a model that will predict customer churn based on **`Churn`** field. 
#
# A table with all features is already created for you.
#
# **Table name: `customer_churn`**

# +
import mlflow.data
from sklearn.model_selection import train_test_split

# load data from the feature table
table_name = f"{DA.catalog_name}.{DA.schema_name}.customer_churn"
dataset = mlflow.data.load_delta(table_name=table_name)
pd = dataset.df.drop("CustomerID").toPandas()

# split dataset to train/test 
target_col = "Churn"
X_all = pd.drop(labels=target_col, axis=1)
y_all = pd[target_col]

# test / train split
X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, train_size=0.95, random_state=42)
print(f"We have {X_train.shape[0]} records in our training dataset")
print(f"We have {X_test.shape[0]} records in our test dataset")
# -

# ## Task 1:  Define Hyperparameter Search Space
#
# Define the parameter search space for hyperopt. Define these hyperparameters and search space;
# * **`max_depth`:** 2 to 30
# * **`max_features`**: 5 to 10
#
# Note that both parameters are discrete values.

# +
from hyperopt import hp

# define param search space

dtc_param_space = {
  "max_depth": hp.uniformint("dtree_max_depth", 2, 30),
  "max_features": hp.uniformint("dtree_max_features", 5, 10)
}
# -

# ## Task 2: Define Optimization Function
#
# Next, define an optimization function that will be used by hyperopt for minimazing the loss. 
#
# Make sure to follow instructions;
#
# * Make sure to enable MLflow run as **`nested`** experiment. 
#
# * For each run log the cross-validation results for `accuracy`, `precision`, `recall` and `f1`
#
# * Use **3-fold** cross validation
#
# * Minimize loss based on the **`precision`** score

# +
from math import sqrt

import mlflow
import mlflow.data
import mlflow.sklearn

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import cross_validate

from hyperopt import STATUS_OK

def tuning_objective(params):
 # start an MLFlow run
 with mlflow.start_run(nested=True) as mlflow_run:
    
   # Enable automatic logging of input samples, metrics, parameters, and models
   mlflow.sklearn.autolog(
       disable=False,
       log_input_examples=True,
       silent=True,
       exclusive=False)

   # set up our model estimator
   dtc = DecisionTreeClassifier(random_state=42, **params)
    
   # cross-validated on the training set
   validation_scores = ["precision", "recall", "f1", "accuracy"]
   cv_results = cross_validate(dtc, X_train, y_train, cv=3, scoring=validation_scores)
   # log the average cross-validated results
   cv_score_results = {}
   for val_score in validation_scores:
     cv_score_results[val_score] = cv_results[f'test_{val_score}'].mean()
     mlflow.log_metric(f"cv_{val_score}", cv_score_results[val_score])

   # return the negative of our cross-validated precision score as the loss
   return {
     "loss": -cv_score_results["precision"],
     "status": STATUS_OK,
     "run": mlflow_run.info.run_id
   }


# -

# ## Task 3: Run Trials in Hyperopt
#
# After defining the *objective function*, we are ready to run this function with hyperopt. 
#
# * Use `SparkTrails` and run *3 trails* in parallel.
#
# * Use **TPE** algorithm for optimization.
#
# * Use maximum 3 evaluations.

# +
from hyperopt import SparkTrials, fmin, tpe

# set the path for mlflow experiment
mlflow.set_experiment(f"/Users/{DA.username}/LAB-2-Hyperparameter-Tuning-with-Hyperopt")

trials = SparkTrials(parallelism=3)
with mlflow.start_run(run_name="Model Tuning with Hyperopt Demo") as parent_run:
  fmin(
    fn=tuning_objective,
    space=dtc_param_space,
    algo=tpe.suggest,
    max_evals=3,
    trials=trials
  )
# -

# ## Task 4: Show the Best Run Info

# get best trail and show the info
best_run = trials.best_trial["result"]
best_run

# ## Task 5: Search for the Best Run with MLflow API
#
# We just got the best run based on the loss metric in the previous step. Sometimes we might need to search for runs using custom filters such as by parent run or by another metric. 
#
# In this step, search for runs of `parent_run` experiment and use following filters;
#
# * Filter by runs which as `FINISHED`
#
# * Order by **cross validation precision** score from **high to low**. 

# +
from mlflow.entities import ViewType

# search over all runs
hpo_runs_pd = mlflow.search_runs(
  experiment_ids=[parent_run.info.experiment_id],
  filter_string=f"tags.mlflow.parentRunId='{parent_run.info.run_id}' AND attributes.status = 'FINISHED'",
  run_view_type=ViewType.ACTIVE_ONLY,
  order_by=["metrics.cv_precision DESC"]
)

display(hpo_runs_pd)

# +
from pyspark.sql.functions import col

all_experiment_runs_df = spark.read.format("mlflow-experiment").load(parent_run.info.experiment_id)

hpo_runs_df = all_experiment_runs_df.where(f"tags['mlflow.parentRunId'] = '{parent_run.info.run_id}' AND status = 'FINISHED'")\
  .withColumn("cv_precision", col("metrics").getItem('cv_precision'))\
  .orderBy(col("cv_precision").desc())

display(hpo_runs_df)
# -

# ## Task 6: Search for the Best Run with MLflow UI
#
# Another way of searching for runs is to simply use the MLflow UI. In this section, we will need to review the experiment and runs and filter runs based on the same filters that are defined in the previous step but this time using the UI.

#
# ## Clean up Classroom
#
# Run the following cell to remove lessons-specific assets created during this lesson.

DA.cleanup()

#
# ## Conclusion
#
# In conclusion, you have successfully completed the Hyperparameter Tuning with Hyperopt lab, gaining practical insights into optimizing machine learning models. Throughout this hands-on session, you've mastered key steps, from defining a hyperparameter search space to executing optimization trials with Spark. Additionally, you searched for and analyzed the best model runs through both the MLflow API and the user-friendly MLflow UI. The primary objective was to empower you with the skills to fine-tune models effectively using Spark, Hyperopt, and MLflow. As you conclude this lab, you are now adept at these techniques. Congratulations on your achievement!

# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
