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
#   <img src="https://databricks.com/wp-content/uploads/2018/03/db-academy-rgb-1200px.png" alt="Databricks Learning">
# </div>
#

#
# # LAB - Batch Deployment
#
# Welcome to the "Batch Deployment" lab! This lab focuses on batch deployment of machine learning models using Databricks. you will engage in tasks related to model inference, model registry, and explore performance results for feature such as Liquid Clustering using `CLUSTER BY`.
#
# **Learning Objectives:**
#
# By the end of this lab, you will be able to;
#
# + **Task 1: Load Dataset**
#     + Load Dataset
#     + Split the dataset to features and response sets
#
# + **Task 2: Inference with feature table**
#
#     + Create Feature Table
#     + Setup Feature Lookups
#     + Fit and Register a Model with UC using Feature Table
#     + Perform batch inference using Feature Engineering's  **`score_batch`** method.
#
# + **Task 3: Assess Liquid Clustering:**
#
#     + Evaluate the performance results for specific optimization techniques:
#         + Liquid Clustering
#

# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **13.3.x-cpu-ml-scala2.12**

#
# ## Classroom Setup
#
# Before starting the Lab, run the provided classroom setup script. This script will define configuration variables necessary for the demo. Execute the following cell:

# %run ../Includes/Classroom-Setup-02Lab

# **Other Conventions:**
#
# Throughout this Lab, we'll refer to the object `DA`. This object, provided by Databricks Academy, contains variables such as your username, catalog name, schema name, working directory, and dataset locations. Run the code block below to view these details:

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")
print(f"User DB Location:  {DA.paths.datasets}")

# ## Task 1: Load Dataset
#
# + Load a dataset:
#   + Define the dataset path
#   + Define the primary key (`customerID`), response variable (`Churn`), and feature variables (`SeniorCitizen`, `tenure`, `MonthlyCharges`, `TotalCharges`) for further processing.
#   + Read the dataset, casting relevant columns to the correct data types, and drop any rows with missing values
# + Split the dataset into training and testing sets
#   + Separate the features and the response for the training set
#

# +
from pyspark.sql.functions import col
# dataset path
dataset_p_telco = f"{DA.paths.datasets}/telco/telco-customer-churn.csv"

# Features to use
primary_key = "customerID"
response = "Churn"
features = ["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]

# Read dataset (and drop nan)
telco_df = spark.read.csv(dataset_p_telco, inferSchema=True, header=True, multiLine=True, escape='"')\
            .withColumn("TotalCharges", col("TotalCharges").cast('double'))\
            .withColumn("SeniorCitizen", col("SeniorCitizen").cast('double'))\
            .withColumn("Tenure", col("tenure").cast('double'))\
            .na.drop(how='any')

# Split with 80 percent of the data in train_df and 20 percent of the data in test_df
train_df, test_df = telco_df.randomSplit([.8, .2], seed=42)

# Separate features and ground-truth
features_df = train_df.select(primary_key, *features)
response_df = train_df.select(primary_key, response)
# -

# ##Task 2: Inference with feature table
# In this task, you will perform batch inference using a feature table. Follow the steps below:
#
# + **Step 1: Create Feature Table**
#
# + **Step 2: Setup Feature Lookups**
#
# + **Step 3: Fit and Register a Model with UC using Feature Table**
#
# + **Step 4: Use the Model for Inference**
#

# **Step 1: Create Feature Table**
#   + Begin by creating a feature table that incorporates the relevant features for inference. This involves selecting the appropriate columns, performing any necessary transformations, and storing the resulting data in a feature table.

# +
from databricks.feature_engineering import FeatureEngineeringClient

# Prepare feature set
features_df_all = telco_df.select(primary_key, *features)

# Feature table definition
fe = FeatureEngineeringClient()
feature_table_name = f"{DA.catalog_name}.{DA.schema_name}.features"

# Drop table if exists
try:
    fe.drop_table(name=feature_table_name)
except:
    pass

# Create feature table
fe.create_table(
    name=feature_table_name,
    df=features_df_all,
    primary_keys=[primary_key],
    description="Telco customer features",
    tags={"team": "telecom"},
)
# -

# **Step 2: Setup Feature Lookups**
#   + Set up a feature lookup to create a training set from the feature table. 
#   + Specify the `lookup_key` based on the columns that uniquely identify records in your feature table.

# +
from databricks.feature_engineering import FeatureLookup

# Goal - limit feature definition in multiple places... define it once when creating the dataset and training the model. At production, we simply read the schema
fl_handle = FeatureLookup(
    table_name=feature_table_name,
    lookup_key=primary_key,
)

# Create a training set based on feature lookup
# NOTE: Because response_df uses the split train_df above, the training_set_spec will be split accounting for 80% of the dataset
training_set_spec = fe.create_training_set(
    df=response_df, # features will be joined into this table... should only include labels and keys for joining to allow for feature adaption
    label=response,
    feature_lookups=[fl_handle], # Can include multiple FeatureLookup objects if pulling features from multiple tables
    exclude_columns=[primary_key], #customerID
)

# Load training dataframe based on defined feature-lookup specification
training_df = training_set_spec.load_df()
# -

print("Total size:\n\t{0:,} records".format(features_df_all.count()))
print("From csv file:\n\t{0:,} training records".format(train_df.count()))
print("\t{0:,} test records".format(test_df.count()))
print("From feature store:\n\t{0:,} training records".format(training_df.count()))

# **Step 3: Fit and Register a Model with UC using Feature Table**
#   + Fit and register a Machine Learning Model using the created training set.
#   + Train a model on the training set and register it in the model registry.

# +
import mlflow
import warnings
from mlflow.types.utils import _infer_schema

# Point to UC model registry
mlflow.set_registry_uri("databricks-uc")
client = mlflow.MlflowClient()

# Helper function that we will use for getting latest version of a model
def get_latest_model_version(model_name):
    """Helper function to get latest model version"""
    model_version_infos = client.search_model_versions("name = '%s'" % model_name) # f"name='{model_name}'" is equivalent
    return max([model_version_info.version for model_version_info in model_version_infos])

# Train a sklearn Decision Tree Classification model
from sklearn.tree import DecisionTreeClassifier

# Convert data to pandas dataframes
# NOTE: If using in production, we would need to consider the flow of this logic... above we read from csv to create the training dataframe, which should be read from the feature table once created
X_train_pdf = training_df.drop(primary_key, response).toPandas()
Y_train_pdf = training_df.select(response).toPandas()
clf = DecisionTreeClassifier(max_depth=3, random_state=42)

# End the active MLflow run before starting a new one
mlflow.end_run()

with mlflow.start_run(run_name="Model-Batch-Deployment-lab-With-FS") as mlflow_run:

    # Enable automatic logging of input samples, metrics, parameters, and models
    mlflow.sklearn.autolog(
        log_input_examples=True,
        log_models=False,
        log_post_training_metrics=True,
        silent=True)
    
    clf.fit(X_train_pdf, Y_train_pdf)

    # Infer output schema
    try:
        output_schema = _infer_schema(Y_train_pdf)
    except Exception as e:
        warnings.warn(f"Could not infer model output schema: {e}")
        output_schema = None

    model_name = f"{DA.catalog_name}.{DA.schema_name}.ml_model"
    
    # Log using feature engineering client and push to registry
    fe.log_model(
        model=clf,
        artifact_path="decision_tree",
        flavor=mlflow.sklearn,
        training_set= training_set_spec,
        output_schema=output_schema,
        registered_model_name=model_name,
    )

    # Set model alias (i.e. Champion)
    client.set_registered_model_alias(model_name, "Champion", get_latest_model_version(model_name))
# -

# **Step 4: Use the Model for Inference**
#   + Utilize the feature engineering client's `score_batch()` method for inference.
#   + Provide the model URI and a dataframe containing primary key information for the inference.

# +
# Load the model
model_uri = f"models:/{model_name}@champion"

# Filter feature store on a set of customerIDs - in production, likely filtering on the same table used for training to get test_df
# Training Table = Real Data Table - A subset of the table would have been used for training
# Labels will be a table collected separately after the fact and joined to the original table to create our training, validation, and test sets
# In production we only have the features... back to the original table where the label is joined or added post-hoc
test_features_df = test_df.select("customerID")

# Perform batch inference using Feature Engineering's score_batch method
result_df = fe.score_batch(
  model_uri=model_uri,
  df=test_features_df,
  result_type="string"
)

# Display the inference results
display(result_df)
# -

# ## Task 3: Assess Liquid Clustering:
#
# Evaluate the performance results for specific optimization techniques, such as: Liquid Clustering Follow the step-wise instructions below:  
# + **Step 1:** Create `batch_inference_liquid_clustering` table and import the following columns: `customerID`, `Churn`, `SeniorCitizen`, `tenure`, `MonthlyCharges`, `TotalCharges`, and `prediction`.
# + **Step 2:**  Begin by assessing Liquid Clustering, an optimization technique for improving performance by physically organizing data based on a specified clustering column.
# + **Step 3:**  Optimize the target table for Liquid Clustering.
# + **Step 4:** Specify the `CLUSTER BY` clause with the desired columns (e.g., (customerID, tenure)) to enable Liquid Clustering on the table.

# Seems like we should only need to run this once... Test this. In production, this below table creation/replacement should not be needed as the table would have been previously created.

# %sql
CREATE OR REPLACE TABLE batch_inference_liquid_clustering(
  customerID STRING,
  Churn STRING,
  SeniorCitizen DOUBLE,
  tenure DOUBLE,
  MonthlyCharges DOUBLE,
  TotalCharges DOUBLE,
  prediction STRING
);

# %sql
OPTIMIZE batch_inference_liquid_clustering;
ALTER TABLE batch_inference_liquid_clustering
CLUSTER BY (customerID, tenure);

#
# ## Clean up Classroom
#
# Run the following cell to remove lessons-specific assets created during this lesson.

DA.cleanup()

#
# ## Conclusion
#
# This lab provides you with hands-on experience in batch deployment, covering model inference, Model Registry usage, and the impact of features like Liquid Clustering on performance. you will gain practical insights into deploying models at scale in a batch-oriented environment.

#
# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the 
# <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | 
# <a href="https://databricks.com/terms-of-use">Terms of Use</a> | 
# <a href="https://help.databricks.com/">Support</a>
