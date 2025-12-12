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
# # LAB - Feature Engineering with Feature Store
#
# Welcome to the "Feature Engineering with Feature Store" In this lesson, you will learn how to load and prepare a dataset for feature selection, explore and manipulate a feature table through Databricks UI, perform feature selection on specific columns, create a new feature table, access feature table details using both UI and API, merge two feature tables based on a common identifier, and efficiently delete unnecessary feature tables. Get ready to enhance your feature engineering skills—let's dive in!
#
# **Lab Outline:**
#
# In this Lab, you will learn how to:
#
# 1. Load and Prepare Dataset for Feature Selection
# 2. Explore Feature Table through UI
# 3. Access Feature Table Information
# 4. Create Feature Table from Existing UC Table
# 5. Enhance Feature Table with New Features
# 6. Efficient Feature Table Deletion

# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **13.3.x-cpu-ml-scala2.12**

#
# ## Classroom Setup
#
# Before starting the demo, run the provided classroom setup script. This script will define configuration variables necessary for the demo. Execute the following cell:

# %run ../Includes/Classroom-Setup-03L

# **Other Conventions:**
#
# Throughout this demo, we'll refer to the object `DA`. This object, provided by Databricks Academy, contains variables such as your username, catalog name, schema name, working directory, and dataset locations. Run the code block below to view these details:

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")
print(f"User DB Location:  {DA.paths.datasets}")

# ## Data Preparation
#

# load dataset
dataset_path = f"{DA.paths.datasets}/cdc-diabetes/diabetes_binary_5050split_BRFSS2015.csv"
silver_df = spark.read.csv(dataset_path, header="true", inferSchema="true", multiLine="true", escape='"')
display(silver_df)

# ## Task1: Feature Selection
#
# The dataset is loaded and ready. We are assuming that most of the data cleaning and feature computation is already done and data is saved to "silver" table.
#
# Select these features from the dataset; **"HighBP", "HighChol", "BMI", "Stroke", "PhysActivity", "GenHlth", "Sex", "Age", "Education", "Income".**
#
# Create a `UID` column to be used as primary key.

# +
from pyspark.sql.functions import monotonically_increasing_id

# select features we are interested in
silver_df = silver_df.select("HighBP", "HighChol", "BMI", "Stroke", "PhysActivity", "GenHlth", "Sex", "Age", "Education", "Income")

# drop the target column - not needed as we can simply choose to not select it above
# silver_df = silver_df.drop("Diabetes_binary")

# create an UID column to be used as primary key
silver_df = silver_df.withColumn("UID", monotonically_increasing_id())

display(silver_df)
# -

#
# ## Task 2: Create a Feature Table
#
#
# Create a feature table from the `silver_df` dataset. Define description and tags as you wish.
#
# New feature table name must be **`diabetes_features`**.
#
# **Note:** Don't define partition column.

# +
from databricks.feature_engineering import FeatureEngineeringClient

fe = FeatureEngineeringClient()

diabetes_table_name = f"{DA.catalog_name}.{DA.schema_name}.diabetes_features"

fe.create_table(
  name=diabetes_table_name,
  primary_keys=["UID"],
  df=silver_df,
  description="Features for diabetes prediction",
  tags= {"team": "lakehouse", "use_case": "healthcare"} # examples
)
# -

#
# ## Task 3: Explore Feature Table with the UI
#
# Now that the feature table is created, visit **Features** page from the left panel and review following information;
#
# * Check table columns, identify **primary key** and **partition** columns.
#
# * View **sample data**.
#
# * View table **details**. 
#
# * View **history**.

# ## Task 4: Retrieve Feature Table Details
#
# Another way of accessing the feature table is using the API. Let's **list `features` and `primary_keys`** of the table.

ft = fe.get_table(name=diabetes_table_name)
print(f"Features: {ft.features}")
print(f"Primary Keys: {ft.primary_keys}")

# ## Task 5: Create a Feature Table from an Existing UC Table
#
# There is a table already created for you which includes diet related features. The table name is **`diet_features`**. Create a feature table for this existing table.

display(spark.sql("SELECT * FROM diet_features"))

# %sql
ALTER TABLE diet_features ALTER COLUMN UID SET NOT NULL;
ALTER TABLE diet_features ADD CONSTRAINT diet_features_pk_constraint PRIMARY KEY (UID);

# ## Task 6: Add New Features to Existing Table
#
# Let's collect diet features and merge them to the existing `diabetes_features` table. As both tables has `UID` as unique identifier, we will merge them based on this column.

# +
diet_features = spark.sql("SELECT * FROM diet_features")

# Update diabetes feature table by adding diet features table
fe.write_table(
  name=diabetes_table_name,
  df=diet_features.select("*"), # Will merge on UID as common column
  mode="merge",
)

# Read and display the merged feature table
display(fe.read_table(name=diabetes_table_name))
# -

# ## Task 7: Delete a Feature Table
#
# We merged both feature tables and we no longer need the `diet_features` table. Thus, let's delete this table.

# +
diet_table_name = f"{DA.catalog_name}.{DA.schema_name}.diet_features"

# drop the table
fe.drop_table(name=diet_table_name)
# -

#
# ## Clean up Classroom
#
# Run the following cell to remove lessons-specific assets created during this lesson.

DA.cleanup()

#
# ## Conclusion
#
# In this lab, you demonstrated the use of Databricks Feature Store to perform feature engineering tasks. You executed the loading, preparation, and selection of features from a dataset, created a feature table, explored and accessed table details through both the UI and API, merged tables, and efficiently removed unnecessary ones. 
#
# This hands-on experience enhanced your feature engineering skills on the Databricks platform.

# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
