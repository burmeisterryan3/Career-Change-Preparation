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
# # LAB - Build a  Feature Engineering Pipeline
#
# Welcome to the "Build a Feature Engineering Pipeline" lab! In this hands-on session, we'll dive into the essential steps of creating a robust feature engineering pipeline. From data loading and preparation to fitting a pipeline and saving it for future use, this lab equips you with fundamental skills in crafting efficient and reproducible machine learning workflows. Let's embark on the journey of transforming raw data into meaningful features for predictive modeling.
#
# **Lab Outline**
#
# + **Task 1:** Load Dataset and Data Preparation
#   + **1.1.** Load Dataset
#   + **1.2.** Data Preparation
# + **Task 2:** Split Dataset
# + **Task 3:** Create Pipeline for Data Imputation and Transformation
# + **Task 4:** Fit the Pipeline
# + **Task 5:** Show Transformation Results
# + **Task 6:** Save Pipeline
#
#
#

#
# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **13.3.x-cpu-ml-scala2.12**

#
# ## Lab Setup
#
# Before starting the Lab, run the provided classroom setup script. This script will establish necessary configuration variables tailored to each user. Execute the following code cell:

# %run ../Includes/Classroom-Setup-01

# **Other Conventions:**
#
# Throughout this demo, we'll refer to the object `DA`. This object, provided by Databricks Academy, contains variables such as your username, catalog name, schema name, working directory, and dataset locations. Run the code block below to view these details:

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")
print(f"Dataset Location:  {DA.paths.datasets}")

# ## Task 1: Load Dataset and Data Preparation
#
#
# **1.1. Load Dataset:**
# + Load a dataset with features that require imputation and transformation
# + Display basic information about the dataset (e.g., schema, summary statistics)
#
# **1.2. Data Preparation:**
#
# + Examine the dataset.
# + Identify and discuss the features that need data preparation.
# + Convert data types: Demonstrate converting data types for selected columns (e.g., String to Int, Int to Boolean).
# + Remove a column: Discuss and remove a column with too many missing values.
# + Remove outliers: Implement a threshold-based approach to remove outlier records for a specific column.
# + Save cleaned dataset as "silver table."

# **1.1. Load Dataset:**
#
# + Load a dataset with features that require imputation and transformation
# + Display basic information about the dataset (e.g., schema, summary statistics)
#

# +
# Set the path of the dataset
dataset_path = f"{DA.paths.datasets}/cdc-diabetes/diabetes_binary_5050_raw.csv"

# Read the CSV file using the Spark read.csv function
cdc_df = spark.read.csv(path=dataset_path, header=True, inferSchema=True, multiLine=True)

# Display the resulting dataframe
display(cdc_df)
# -

display(cdc_df.select(*cdc_df.columns).describe())

# **1.2. Data Preparation:**
#
# + Examine the dataset.
# + Identify the features that need data preparation.
# + Convert data types: Demonstrate converting data types for selected columns (e.g., String to Int, Double to Boolean).

# +
from pyspark.sql.types import IntegerType, BooleanType, StringType, DoubleType

# Method for selecting all columns of a particular type... we need to have more granual parsing by types as implemented below
print([f.name for f in cdc_df.schema.fields if isinstance(f.dataType, DoubleType)])
print([f.name for f in cdc_df.schema.fields if isinstance(f.dataType, StringType)])


# +
from pyspark.sql.types import IntegerType, BooleanType, StringType, DoubleType
from pyspark.sql.functions import col

# Convert string columns to integer type
# List of string columns to convert: (HighBP, CholCheck, PhysActivity, MentlHlth, Age)
string_columns = ["MentHlth", "Age"]

# Iterate over string columns and cast to integer type
for column in string_columns:
   cdc_df = cdc_df.withColumn(column, col(column).cast(IntegerType()))

# Convert string columns to double type
# List of string columns to convert: (Smoker, NoDocbcCost)
string_columns = ["Smoker", "NoDocbcCost"]

# Iterate over string columns and cast to integer type
for column in string_columns:
   cdc_df = cdc_df.withColumn(column, col(column).cast(DoubleType()))

# Convert double columns to BooleanType (Diabetes_binary, GenHlth, HeartDiseaseorAttack, Sex)
double_columns = ["Diabetes_binary", "GenHlth", "HeartDiseaseorAttack", "Sex", "HighBP", "CholCheck", "PhysActivity", "Stroke", "Fruits", "Veggies", "hvyalcoholconsump", "DiffWalk"]
for column in double_columns:
    cdc_df = cdc_df.withColumn(column, col(column).cast(BooleanType()))

# Check against schema printed with original read above to ensure changes were properly implemented
cdc_df.printSchema()

# + **Remove a column with too many missing values.**

# +
from pyspark.sql.functions import col, when, count, concat_ws, collect_list

# First, get the count of missing values per column to create a singleton row DataFrame
missing_cdc_df = cdc_df.select([count(when(col(c).contains('null') | (col(c) == '') | col(c).isNull(), c)).alias(c) for c in cdc_df.columns])

# Define a helper function to transpose the DataFrame for better readability
def TransposeDF(df, columns, pivotCol):
    """Helper function to transpose Spark DataFrame"""
    columnsValue = [f"'{column}',{column}" for column in columns]
    stackCols = ','.join(x for x in columnsValue) # create one string to use in PySpark SQL call
    df_1 = df.selectExpr(pivotCol, "stack(" + str(len(columns)) + "," + stackCols + ")")

    # Comment this out -- for pedagogical reasons only
    # display(df_1.agg(collect_list(col("col1"))))

    # Use collect_list(col("col1")) to allow for aggregation over non-groupBy'd column
    # Use agg with concat_ws to allow for general transpose function... sum would also work for this example but would only work in the future for numeric columns
    final_df = df_1.groupby("col0")\
                   .pivot(pivotCol)\
                   .agg(concat_ws("", collect_list(col("col1"))))\
                   .withColumnRenamed("col0", pivotCol)
    return final_df

# Transpose the missing_cdc_df for better readability
missing_df_T = TransposeDF(spark.createDataFrame([{"Column": "Missing Value Counts"}]).join(missing_cdc_df),
                           missing_cdc_df.columns,
                           "Column")

# Display the count of missing values per column
display(missing_cdc_df)

# Set a threshold for missing data to drop columns
per_thresh = 0.6

# Calculate the total count of rows in the DataFrame
N = cdc_df.count()

# Identify columns with more than the specified percentage of missing data
to_drop_missing = missing_df_T.select("Column").where((col("Missing Value Counts") / N) >= per_thresh).toPandas()["Column"].values

# Drop columns with more than 60% missing data
print(f"Dropping columns {to_drop_missing} with more than {per_thresh * 100}% missing data")
cdc_no_missing_df = cdc_df.drop(*to_drop_missing)

# Display the DataFrame after dropping columns with excessive? missing data
display(cdc_no_missing_df)


# + **Remove outliers: Implement a threshold-based approach to remove outlier records for a specific column.**

display(cdc_no_missing_df.select(col("MentHlth"), col("BMI")).describe())

# +
# Remove listings with MentHlth < -40
MentHlth_cutoff = -40
cdc_no_outliers_df = cdc_no_missing_df.where(col("MentHlth") >= MentHlth_cutoff)

# Remove listings with BMI > 110
BMI_cutoff = 110
cdc_no_outliers_df = cdc_no_outliers_df.where(col("BMI") <= BMI_cutoff)

# Display the count before and after removing outliers
print("Before: {} rows, After: {} rows".format(cdc_no_missing_df.count(), cdc_no_outliers_df.count()))

# Display the DataFrame after removing outliers
display(cdc_no_outliers_df)

# + **Save the cleaned dataset as the "silver table" for further analysis**

# +
cdc_df_full = "cdc_df_full"

# Save as DELTA table (silver)
cdc_df_full_silver = cdc_df_full + "_silver"
cdc_no_outliers_df.write.mode("overwrite").option("mergeSchema", True).saveAsTable(cdc_df_full_silver)

# Print the resulting DataFrame
display(spark.table(cdc_df_full_silver))
# -

# ## Task 2: Split Dataset
#
# **2.1. Split Dataset:**
#
# + Split the cleaned dataset into training and testing sets in 80:20 ratio

# +
# Split with 80 percent of the data in train_df and 20 percent of the data in test_df
train_df, test_df = cdc_no_outliers_df.randomSplit([0.8, 0.2], seed=12345)

# Materialize the split DataFrames as DELTA tables
train_df.write.mode("overwrite").option("overwriteSchema", True).saveAsTable(cdc_df_full + "_train")
test_df.write.mode("overwrite").option("overwriteSchema", True).saveAsTable(cdc_df_full + "_test")
# -

# ## Task 3: Create Pipeline using Data Imputation and Transformation
#
# **3.1. Create Pipeline:**
#
# + Create a pipeline with the following tasks:
#   + StringIndexer
#   + Imputer
#   + Scaler
#   + One-Hot Encoder
#

# +
from pyspark.sql.types import IntegerType, BooleanType, StringType, DoubleType
from pyspark.sql.functions import col, count, when

# Get a list of integer & boolean columns
integer_cols = [c.name for c in train_df.schema.fields if isinstance(c.dataType, IntegerType | BooleanType)]

# Loop through integer columns to cast each one to double
for column in integer_cols:
    train_df = train_df.withColumn(column, col(column).cast("double"))
    test_df = test_df.withColumn(column, col(column).cast("double"))

# Get a list of string, numeric columns
string_cols = [c.name for c in train_df.schema.fields if c.dataType == StringType()]
num_cols = [c.name for c in train_df.schema.fields if c.dataType == DoubleType()]

# Get a list of columns with missing values - Numerical
# Return a list of Columns with the counts of Null values
num_missing_values_logic = [count(when(col(column).isNull(),column)).alias(column) for column in num_cols]
# Select returns a DataFrame (singleton row in this case) of the numerical columns' Null value counts
# First returns a Row object (the only row in this case)
# asDict cast the Row object to a dictionary with column names as keys
row_dict_num = train_df.select(num_missing_values_logic).first().asDict()
# Get a list of numerical column names with missing values
num_missing_cols = [column for column in row_dict_num if row_dict_num[column] > 0]

# # String -- no string columns - kept for pedagogical purposes
# DA intent may not have been to convert 0,1 columns to boolean initially
string_missing_values_logic = [count(when(col(column).isNull(), column)).alias(column) for column in string_cols]
row_dict_string = train_df.select(string_missing_values_logic).first().asDict()
string_missing_cols = [column for column in row_dict_string if row_dict_string[column] > 0]

# Print columns with missing values
print(f"Numeric columns with missing values: {num_missing_cols}")
print(f"String columns with missing values: {string_missing_cols}")

# +
# import required libraries
from pyspark.ml import Pipeline
from pyspark.ml.feature import Imputer, VectorAssembler, RobustScaler, StringIndexer, OneHotEncoder

# String/Cat Indexer
# create an additional column to index string columns
# these columns will retain their original null values via 'handleInvalid="keep"'
string_cols_indexed = [c + '_index' for c in string_cols]
string_indexer = StringIndexer(inputCols=string_cols, outputCols=string_cols_indexed, handleInvalid="keep")

# Imputer (same strategy for all double/indexes)
# create a list of columns containing missing values
# utilize the mode strategy to impute all the missing columns
to_impute = num_missing_cols

imputer = Imputer(inputCols=to_impute, outputCols=to_impute, strategy='mode')

# Scale numerical
# create a vector of numerical columns as an array in the 'numerical_assembled' column
# robustly scale all the numerical_scaled values for this array in the 'numerical_scaled' column
numerical_assembler = VectorAssembler(inputCols=num_cols, outputCol="numerical_assembled")
numerical_scaler = RobustScaler(inputCol="numerical_assembled", outputCol="numerical_scaled")

# OHE categoricals
# create an OHE encoder to turn the indexed string columns into binary vectors
ohe_cols = [column + '_ohe' for column in string_cols]
one_hot_encoder = OneHotEncoder(inputCols=string_cols_indexed, outputCols=ohe_cols, handleInvalid="keep")

# Assembler (All)
# re-collect all columns and create a 'features' column from them
feature_cols = ["numerical_scaled"] + ohe_cols
vector_assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")

# Instantiate the pipeline
# instantiate a pipeline with all the above stages
stages_list = [
    string_indexer,
    imputer,
    numerical_assembler,
    numerical_scaler,
    one_hot_encoder,
    vector_assembler
]

pipeline = Pipeline(stages=stages_list)
# -

# ##Task 4: Fit the Pipeline
# **4.1. Fit the Pipeline:**
#
# + Use the training dataset to fit the created pipeline.

# Fit the pipeline using the training dataset
pipeline_model = pipeline.fit(train_df)


# ##Task 5: Show Transformation Results
# **5.1. Transform Datasets:**
#
# + Apply the fitted pipeline to transform the training and testing datasets.
# + Apply these transformations to different sets (e.g., train, test, validation).

# +
# Transform both the training and test datasets using the previously fitted pipeline model
train_transformed_df = pipeline_model.transform(train_df)
test_transformed_df = pipeline_model.transform(test_df)

# Display the transformed features from the training dataset
train_transformed_df.select("features").show(3, truncate=False)
# -

# ##Task 6: Save Pipeline
# **6.1. Save Pipeline:**
#
# + Save the fitted pipeline to the working directory.
# + Explore the saved pipeline.

# Save the trained pipeline model to the specified directory in the working directory
pipeline_model.save(f"{DA.paths.working_dir}/spark_pipelines")

# +
# Load the previously saved pipeline model from the specified directory in the working directory
from pyspark.ml import PipelineModel

# Load the pipeline model
loaded_pipeline = PipelineModel.load(f"{DA.paths.working_dir}/spark_pipelines")

# Display the stages of the loaded pipeline
loaded_pipeline.stages
# -

#
# ## Clean up Classroom
#
# Run the following cell to remove lessons-specific assets created during this lesson.

DA.cleanup()

# ## Conclusion
#
# In conclusion, this lab demonstrated the crucial steps in preparing and transforming a dataset for machine learning. We covered data cleaning, splitting, and created a pipeline for tasks like imputation and scaling. Saving the pipeline ensures reproducibility, and these foundational concepts can be applied in various machine learning workflows.

# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
