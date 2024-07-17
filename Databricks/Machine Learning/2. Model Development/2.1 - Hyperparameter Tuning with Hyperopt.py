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
# # Hyperparameter Tuning with Hyperopt
#
# In this hands-on demo, you will learn how to leverage **Hyperopt**, a powerful optimization library, for efficient model tuning. We'll guide you through the process of performing **Bayesian hyperparameter optimization, demonstrating how to define the search space, objective function, and algorithm selection**. Throughout the demo, you will utilize *MLflow* to seamlessly track the model tuning process, capturing essential information such as hyperparameters, metrics, and intermediate results. By the end of the session, you will not only grasp the principles of hyperparameter optimization but also be proficient in finding the best-tuned model using various methods such as the **MLflow API** and **MLflow UI**.
#
# **Learning Objectives:**
#
# *By the end of this demo, you will be able to;*
#
# * Utilize hyperopt for model tuning.
# * Perform a Bayesian hyperparameter optimization using Hyperopt.
# * Track model tuning process with MLflow.
# * Search and retrieve the best model.  
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

# %run ../Includes/Classroom-Setup-02

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
# Before we start fitting a model, we need to prepare dataset. First, we will load dataset, then we will split it to train and test sets.

# ### Load Dataset
#
# In this demo we will be using the CDC Diabetes dataset. This dataset has been loaded and loaded to a feature table. We will use this feature table to load data.

# +
import mlflow.data

# load data from the feature table
table_name = f"{DA.catalog_name}.{DA.schema_name}.diabetes"
diabetes_dataset = mlflow.data.load_delta(table_name=table_name)
diabetes_pd =diabetes_dataset.df.drop("unique_id").toPandas()

# review dataset and schema
display(diabetes_pd)
print(diabetes_pd.info())
# -

#
# ### Train/Test Split
#
# Next, we will divide the dataset to training and testing sets. 

# +
from sklearn.model_selection import train_test_split

print(f"We have {diabetes_pd.shape[0]} records in our source dataset")

# split target variable into it's own dataset
target_col = "Diabetes_binary"
X_all = diabetes_pd.drop(labels=target_col, axis=1)
y_all = diabetes_pd[target_col]

# test / train split
X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, train_size=0.95, random_state=42)
print(f"We have {X_train.shape[0]} records in our training dataset")
print(f"We have {X_test.shape[0]} records in our test dataset")
# -

# ## Hyperparameter Tuning

# ### Define the Hyperparameter Search Space
#
# Hyperopt uses a [Bayesian optimization algorithm](https://hyperopt.github.io/hyperopt/#algorithms) to perform a more intelligent search of the hyperparameter space. Therefore, **the initial space definition is effectively a prior distribution over the hyperparamters**, which will be used as the starting point for the Bayesian optimization process. 
#
# Instead of defining a range or grid for each hyperparameter, we use [Hyperopt's parameter expressions](https://hyperopt.github.io/hyperopt/getting-started/search_spaces/#parameter-expressions) to define such prior distributions over parameter values.
#

# +
from hyperopt import hp

dtc_param_space = {
  'criterion': hp.choice('dtree_criterion', ['gini', 'entropy']),
  'max_depth': hp.choice('dtree_max_depth',
                          [None, hp.uniformint('dtree_max_depth_int', 5, 50)]),
  'min_samples_split': hp.uniformint('dtree_min_samples_split', 2, 40),
  'min_samples_leaf': hp.uniformint('dtree_min_samples_leaf', 1, 20)
}
# -

# ### Define the Optimization Function
#
# We wrap our training code up as a function that we pass to hyperopt to optimize. The function takes a set of hyperparameter values as a `dict` and returns the validation loss score.
#
# **💡 Note:** We are using `f1` score as the cross-validated loss metric. As we goal of optimization function is to minimize the loss, we are returning `-f1`, in other words, **we want to maximize the `f1` score**.

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
    dtc = DecisionTreeClassifier(**params)
    
    # cross-validated on the training set
    validation_scores = ['accuracy', 'precision', 'recall', 'f1']
    cv_results = cross_validate(dtc, 
                                X_train, 
                                y_train, 
                                cv=5,
                                scoring=validation_scores)
    # log the average cross-validated results
    cv_score_results = {}
    for val_score in validation_scores:
      cv_score_results[val_score] = cv_results[f'test_{val_score}'].mean()
      mlflow.log_metric(f"cv_{val_score}", cv_score_results[val_score])

    #### NOT SURE WHY THIS IS HERE... SEEMS WE SHOULD DO THIS AFTER SELECTING THE BEST HYPERPARAMETERS ###
    # # fit the model on all training data
    # dtc_mdl = dtc.fit(X_train, y_train)

    # # evaluate the model on the test set
    # y_pred = dtc_mdl.predict(X_test)
    # accuracy_score(y_test, y_pred)
    # precision_score(y_test, y_pred)
    # recall_score(y_test, y_pred)
    # f1_score(y_test, y_pred)
    ######################################################################################################

    # return the negative of our cross-validated F1 score as the loss
    return {
      "loss": -cv_score_results['f1'],
      "status": STATUS_OK,
      "run": mlflow_run
    }


# -

# ### Run in Hyperopt
#
# After defining the *objective function*, we are ready to run this function with hyperopt. 
#
# As you may have noticed, tuning process will need to test many models. We are going to create an instance of **`SparkTrials()` to parallelize hyperparameter tuning trials using Spark**. This is useful for distributing the optimization process across a Spark cluster.
#
# `SparkTrials` takes a **`parallelism` parameter, which specifies how many trials are run in parallel**. This parameter will depend on the compute resources available for the cluster. You can read more about how to choose the optimal `parallelism` value in this [blog post](https://www.databricks.com/blog/2021/04/15/how-not-to-tune-your-model-with-hyperopt.html). 
#
# For search algorithm, we will choose the **TPE (Tree-structured Parzen Estimator) algorithm for optimization (`algo=tpe.suggest`)**.

# +
from hyperopt import SparkTrials, fmin, tpe

# set the path for mlflow experiment
mlflow.set_experiment(f"/Users/{DA.username}/Demo-2.1-Hyperparameter-Tuning-with-Hyperopt")

trials = SparkTrials(parallelism=4)
with mlflow.start_run(run_name="Model Tuning with Hyperopt Demo") as parent_run:
  fmin(tuning_objective,
      space=dtc_param_space,
      algo=tpe.suggest,
      max_evals=5,  # Increase this when widening the hyperparameter search space.
      trials=trials)

best_result = trials.best_trial["result"]
best_run = best_result["run"]
# -

# Note that we used a **nested run** while tracking the tuning process. This means we can access to the *parent_run* and child runs. One of the runs we would definitely interested in is the *best_run*. Let's check out these runs.

parent_run.info.run_id

best_run.info

# ## Find the Best Run
#
# In this section, we will search for registered models. There are couple ways for achieving this. We will show how to search runs using MLflow API, PySpark API and the UI. 

# ### Find the Best Run - MLFlow API
#
# Using the MLFlow API, you can search runs in an experiment, which returns results into a Pandas DafaFrame.

# +
from mlflow.entities import ViewType

# search over all runs
hpo_runs_pd = mlflow.search_runs(
  experiment_ids=[parent_run.info.experiment_id],
  filter_string=f"tags.mlflow.parentRunId = '{parent_run.info.run_id}' AND attributes.status = 'FINISHED'",
  run_view_type=ViewType.ACTIVE_ONLY,
  order_by=["metrics.cv_f1 DESC"]
)

display(hpo_runs_pd)

# NOTE 1: The experiment_id and tags.mlflow.parentRunId are the same for each run. The run_id differentiates them.
# NOTE 2: params.dtree_max_depth and params.dtree_criterion reflect the array "choice" index. See params.dtree_max_depth_int for the value selected when 1 was chosen initially, i.e., not None.
# -

# ### Find the Best Run - PySpark API
#
# Alternatively, you can read experiment results into a PySpark DataFrame and use standard Spark expressions to search runs in an experiment.

# +
all_experiment_runs_df = spark.read.format("mlflow-experiment").load(parent_run.info.experiment_id)
display(all_experiment_runs_df)

# NOTE: mlflow.search_runs and spark.read.format produce different df formats. spark.read.format groups metrics, params, and tags into single columns.

# +
from pyspark.sql.functions import col

hpo_runs_df = all_experiment_runs_df.where(f"tags['mlflow.parentRunId'] = '{parent_run.info.run_id}' AND status = 'FINISHED'")\
  .withColumn("cv_f1", col("metrics").getItem('cv_f1'))\
  .orderBy(col("cv_f1").desc())

display(hpo_runs_df)
# -

# ### Find the Best Run - MLflow UI
#
# The simplest way of seeing the tuning result is to use MLflow UI. 
#
# * Click on **Experiments** from left menu.
#
# * Select experiment which has the same name as this notebook's title (**2.1 - Hyperparameter Tuning with Hyperopt**).
#
# * View the **parent run** and **nested child runs**. 
#
# * You can filter and order by metrics and other model metadata.

#
# ## Clean up Classroom
#
# Run the following cell to remove lessons-specific assets created during this lesson.

DA.cleanup()

#
# ## Conclusion
#
# To sum it up, this demo has shown you the process of tuning your models using Hyperopt and MLflow. You've learned a method to fine-tune your model settings through Bayesian optimization and how to keep tabs on the whole tuning journey with MLflow. Moving forward, these tools will be instrumental in improving your model's performance and simplifying the process of fine-tuning machine learning models.

# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
