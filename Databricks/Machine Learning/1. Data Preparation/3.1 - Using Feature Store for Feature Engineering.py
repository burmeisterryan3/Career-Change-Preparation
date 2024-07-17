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
# # Using Feature Store for Feature Engineering 
#
# In this demo, we will guide you to explore the use of Feature Stores to enhance feature engineering workflow and understand their crucial role in development of machine learning models. First we will create feature store tables for effective implementation in feature engineering processes and then discuss how to update features. Also, we will cover how to convert existing table to feature tables in Unity Catalog.
#
# **Learning Objectives:**
#
# *By the end of this demo, you will be able to;*
#
# 1. Create a Feature Store table from a PySpark DataFrame for training/modeling data and holdout data.
# 1. Identify the requirements for a Delta table in Unity Catalog to be automatically configured as a feature table.
# 1. Alter an existing Delta table in Unity Catalog so that it can be used as a feature table.
# 1. Add new features to an existing feature table in Unity Catalog.
# 1. Explore a Feature Store table in the user interface.
# 1. Upgrade a workspace feature table to a Unity Catalog feature table.
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

# %run ../Includes/Classroom-Setup-03.1

# **Other Conventions:**
#
# Throughout this demo, we'll refer to the object `DA`. This object, provided by Databricks Academy, contains variables such as your username, catalog name, schema name, working directory, and dataset locations. Run the code block below to view these details:

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")
print(f"Dataset Location:  {DA.paths.datasets}")

# ## Feature Engineering
#
# Before we save features to a feature table we need to create features that we are interested in. Feature selection criteria depend on your project goals and business problem. Thus, in this section, we will pick some features, however, it doesn't necessarily mean that these features are significant for our purpose.
#
# **One important point is that you need to exclude the target field from the feature table and you need to define a primary key for the table.**
#

# ### Load Dataset
#
# Typically, first, you will need to conduct data pre-processing and select features. As we covered data pre-processing and feature preparation, we will load a clean dataset which you would typically load from a **`silver`** table.
#
# Let's load in our dataset from a CSV file containing Telco customer churn data from the specified path using Apache Spark. **In this dataset the target column will be `Churn` and primary key will be `customerID`.** 

# +
# Load dataset
dataset_path = f"{DA.paths.datasets}/telco/telco-customer-churn.csv"
telco_df = spark.read.csv(dataset_path, header="true", inferSchema="true", multiLine="true", escape='"')

# Drop the taget column
telco_df = telco_df.drop("Churn")

# View dataset
display(telco_df)
# -

# ## Save Features to Feature Table
#
#
# Let's start creating a <a href="https://docs.databricks.com/en/machine-learning/feature-store/uc/feature-tables-uc.html#install-feature-engineering-in-unity-catalog-python-client" target="_blank">Feature Engineering Client</a> so we can populate our feature store.

# +
from databricks.feature_engineering import FeatureEngineeringClient


fe = FeatureEngineeringClient()

help(fe.create_table)
# -

#
# ### Create Feature Table
#
# Next, we can create the Feature Table using the **`create_table`** method.
#
# This method takes a few parameters as inputs:
# * **`name`** - A feature table name of the form **`<catalog>.<schema_name>.<table_name>`**
# * **`primary_keys`** - The primary key(s). If multiple columns are required, specify a list of column names.
# * **`timestamp_col`** - [OPTIONAL] any timestamp column which can be used for `point-in-time` lookup.
# * **`df`** - Data to insert into this feature table.  The schema of **`features_df`** will be used as the feature table schema.
# * **`schema`** - Feature table schema. Note that either **`schema`** or **`df`** must be provided.
# * **`description`** - Description of the feature table
# * **`partition_columns`** - Column(s) used to partition the feature table.
# * **`tags`** - Tag(s) to tag feature table

# +
# create a feature table from the dataset
table_name = f"{DA.catalog_name}.{DA.schema_name}.telco_customer_features"

fe.create_table(
    name=table_name,
    primary_keys=["customerID"],
    df=telco_df,
    #partition_columns=["InternetService"] for small datasets partitioning is not recommended
    description="Telco customer features",
    tags={"source": "bronze", "format": "delta"}
)
# -

#
# Alternatively, you can **`create_table`** with schema only (without **`df`**), and populate data to the feature table with **`fe.write_table`**, **`fe.write_table`** has **`merge`** mode ONLY (to overwrite, we should drop and then re-create the table).
#
#
# Example:
#
# ```
# # One time creation
# fs.create_table(
#     name=table_name,
#     primary_keys=["index"],
#     schema=telco_df.schema,
#     description="Original Telco data (Silver)"
# )
#
# # Repeated/Scheduled writes
# fs.write_table(
#     name=table_name,
#     df=telco_df,
#     mode="merge"
# )
# ```

# ### Explore Feature Table with the UI
#
# Now let's explore the UI and see how it tracks the tables that we created.
#
# * Click of **Features** from left panel.
#
# * Select the **catalog** that you used for creating the feature table.
#
# * Click on the feature table and you should see the table details as show below.
#
# <img src="https://s3.us-west-2.amazonaws.com/files.training.databricks.com/images/ml-01-feature-store-feature-table-v1.png" alt="Feature Store Table Details" width="1000"/>

#
# ### Load Feature Table
#
# We can also look at the metadata of the feature store via the FeatureStore client by using **`get_table()`**. *As feature table is a Delta table we can load it with Spark as normally we do for other tables*.

ft = fe.get_table(name=table_name)
print(f"Feature Table description: {ft.description}")
print(ft.features)

display(fe.read_table(name=table_name))
#display(spark.table(table_name)) # we could just read as delta table

#
# ## Update Feature Table
#
# In some cases we might need to update an existing feature table by adding new features or deleting existing features. In this section, we will show to make these type of changes. 

# ### Add a New Feature
#
# To illustrate adding a new feature, let's redefine an existing one. In this case, we'll transform the `tenure` column by categorizing it into three groups: `short`, `mid`, and `long`, representing different tenure durations. 
#
# Then we will write the dataset back to the feature table. The important parameter is the `mode` parameter, which we should set to `"merge"`.

# +
from pyspark.sql.functions import when

telco_df_updated = telco_df.withColumn("tenure_group", 
    when((telco_df.tenure >= 0) & (telco_df.tenure <= 25), "short")
    .when((telco_df.tenure > 25) & (telco_df.tenure <= 50), "mid")
    .when((telco_df.tenure > 50) & (telco_df.tenure <= 75), "long")
    .otherwise("invalid")
)
# -

# Selecting relevant columns. Use an appropriate mode (e.g., "merge") and display the written table for validation.
#
# NOTE: `FeatureEngineeringClient.write_table` parameter `df` must include `primary_key` established with `create_table`.

fe.write_table(
    name=table_name,
    df=telco_df_updated.select("customerID","tenure_group"), # primary_key and column to add
    mode="merge"
)

#
# ### Delete Existing Feature
#
# To remove a feature column from the table you can just drop the column. Let's drop the original `tenure` column.
#
# **💡 Note:** We need to set Delta read and write protocal version manually to support column mapping. If you want to learn more about this you can check related [documentation page](https://docs.databricks.com/en/delta/delta-column-mapping.html).

# %sql
ALTER TABLE telco_customer_features SET TBLPROPERTIES ('delta.columnMapping.mode' = 'name', 'delta.minReaderVersion' = '2', 'delta.minWriterVersion' = '5');
ALTER TABLE telco_customer_features DROP COLUMNS (tenure)

# ## Read Feature Table by Version
#
# As feature tables are based on Delta tables, we get all nice features of Delta including versioning. To demonstrate this, let's read from a snapshot of the feature table.

# Get timestamp for initial feature table
timestamp_v3 = spark.sql(f"DESCRIBE HISTORY {table_name}").orderBy("version").collect()[2].timestamp
print(timestamp_v3)

# +
# Read previous version using native spark API... a reminder that feature tables are delta tables with just a bit more metadata
telco_df_v3 = (spark
        .read
        .option("timestampAsOf", timestamp_v3)
        .table(table_name))

display(telco_df_v3)
# -

#
# The warning when displaying the older schema version below will show the expected output does not include the `tenure` column (as we dropped that above). It lets us know that the most current schema does not align with the version we are reading.

# +
# Display old version of feature table
feature_df = fe.read_table(
  name=table_name,
  as_of_delta_timestamp=timestamp_v3
)

feature_df.printSchema()
# -

#
# ## Create a Feature Table from Existing UC Table
#
# Alter/Change existing UC table to become a feature table
# Add a primary key (PK) with non-null constraint _(with timestamp if applicable)_ on any UC table to turn it into a feature table (more info [here](https://docs.databricks.com/en/machine-learning/feature-store/uc/feature-tables-uc.html#use-existing-uc-table))
#
# In this example, we have a table created in the beginning of the demo which contains security features. Let's convert this delta table to a feature table.
#
# For this, we need to do these two changes;
#
# 1. Set primary key columns to `NOT NULL`.
#
# 1. Alter the table to add the `Primary Key` Constraint

display(spark.sql("SELECT * FROM security_features"))

# %sql
ALTER TABLE security_features ALTER COLUMN customerID SET NOT NULL;
ALTER TABLE security_features ADD CONSTRAINT security_features_pk_constraint PRIMARY KEY(customerID);

#
# ## _[OPTIONAL]_ Migrate Workspace Feature Table to Unity Catalog
#
# If you have a classic/workspace feature table, you can migrate it to Unity Catalog feature store. To do that, first, you will need to upgarde the table to UC supported table and then use `UpgradeClient` to complete the upgrade. For instructions please visit [this documentation page](https://docs.databricks.com/en/machine-learning/feature-store/uc/feature-tables-uc.html#upgrade-a-workspace-feature-table-to-unity-catalog).
#
# A sample code snippet for upgrading classic workspace table;
#
# ```
# from databricks.feature_engineering import UpgradeClient
#
#
# upgrade_client = UpgradeClient()
#
# upgrade_client.upgrade_workspace_table(
#   source_workspace_table="database.test_features_table",
#   target_uc_table=f"{CATALOG}.{SCHEMA}.test_features_table"
# )
# ```

#
# ## Clean up Classroom
#
# Run the following cell to remove lessons-specific assets created during this lesson.

DA.cleanup()

#
# ## Conclusion
#
# In this demo, we learned about Feature Stores, essential for optimizing machine learning models. We explored their benefits, compared Workspace and Unity Catalog Feature Stores, and created feature store tables for effective feature engineering. Mastering these skills empowers efficient collaboration and enhances data consistency, contributing to the development of robust machine learning models.

# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
