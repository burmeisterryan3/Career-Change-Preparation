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
# # Data Preparation and Feature Engineering
#
# In this demo, we'll delve into techniques such as preparing modeling data, including splitting data, handling missing values, encoding categorical features, and standardizing features. We will also discuss outlier removal and coercing columns to the correct data type. By the end, you will have a comprehensive understanding of data preparation for modeling and feature preparation.
#
# **Learning Objectives:**
#
# By the end of this demo, you will be able to: 
#
# - Coerce columns to be the correct data type based on feature or target variable type.
# - Identify and remove outliers from the modeling data.
# - Drop rows/columns that contain missing values.
# - Impute categorical missing values with the mode value.
# - Replace missing values with a specified replacement value.
# - One-hot encode categorical features.
# - Perform ordered indexing as an alternative categorical feature preparation for random forest modeling.
# - Apply pre-existing embeddings to categorical features.
# - Standardize features in a training set.
# - Split modeling data into a train-test-holdout split as part of a modeling process.
# - Split training data into cross-validation sets as part of a modeling process.

# ## Requirements
#
# Please review the following requirements before starting the lesson:
#
# * To run this notebook, you need to use one of the following Databricks runtime(s): **13.3.x-cpu-ml-scala2.12**

#
# ## Classroom Setup
#
# Before starting the demo, run the provided classroom setup script. This script will define configuration variables necessary for the demo. Execute the following cell:

# %run ../Includes/Classroom-Setup-01

# **Other Conventions:**
#
# Throughout this demo, we'll refer to the object `DA`. This object, provided by Databricks Academy, contains variables such as your username, catalog name, schema name, working directory, and dataset locations. Run the code block below to view these details:

print(f"Username:          {DA.username}")
print(f"Catalog Name:      {DA.catalog_name}")
print(f"Schema Name:       {DA.schema_name}")
print(f"Working Directory: {DA.paths.working_dir}")
print(f"Dataset Location:  {DA.paths.datasets}")

#
# ## Data Cleaning and Imputation
#
# - Load the dataset from the specified path using Spark and read it as a DataFrame.
#
# - Drop any rows with missing values from the DataFrame using the **`dropna()`** method.
#
# - Fill any remaining missing values in the DataFrame with the 0 using the **`fillna()`** method.
#
# - Create a temporary view named as **`telco_customer_churn`**

# +
dataset_path = f"{DA.paths.datasets}/telco/telco-customer-churn-noisy.csv"
telco_df = spark.read.csv(dataset_path, header="true", inferSchema="true", multiLine="true", escape='"')

# telco_df.printSchema()
display(telco_df)
# -

#
# ### Coerce/Fix Data Types
#
# Even though most of the data types are correct let's do the following to have a better memory footprint of the dataframe in memory
#
# * Convert **`SeniorCitizen`** and **`Churn`** binary columns to boolean type.
#
# * Converting the **`tenure`** column to a long integer using **`.selectExpr`** and reordering the columns.
#
# * Using **`spark.sql`** to convert **`Partner`** , **`Dependents`**, **`PhoneService`** and **`PaperlessBilling`** columns to boolean, and reordering the columns. Then, saving the dataframe as a DELTA table.

# +
from pyspark.sql.types import BooleanType, ShortType, IntegerType
from pyspark.sql.functions import col, when

# METHOD 1 - col().cast() - If values cannot be directly cast to type with additional assumptions, then this will not work. An alternative method must be used
binary_columns = ["SeniorCitizen", "Churn"]
telco_customer_churn_df = telco_df
for column in binary_columns:
    telco_customer_churn_df = telco_df.withColumn(column, col(column).cast(BooleanType()))

telco_customer_churn_df.select(*binary_columns).printSchema()
# -

# Casting didn't work on `SeniorCitizen` most probably because there was some null values or values which couldn't be encoded correctly, we can force coerce using a simple filter method (assuming missing values in this column can be encoded as `False`)

# +
# METHOD 2 - Make the assumptions needed to cast using METHOD 1 explicit to force the conversions (accounts for NULL values)
telco_customer_churn_df = telco_customer_churn_df.withColumn(\
    "SeniorCitizen", when(col("SeniorCitizen")==1, True).otherwise(False))

telco_customer_churn_df.select("SeniorCitizen").printSchema()

# +
# Create a temporary view within the Schema
# Unlike a traditional temp table, a temp view is NOT materialized at all even to memory. It's useful for accessing data in SQL but understand that its statements have to be evaluated EVERY time it's accessed
telco_customer_churn_df.createOrReplaceTempView("telco_customer_churn_temp_view")

# METHOD 3: Explicitly cast using SQL in Spark SQL
# Reorder the columns as desired while casting other columns to the Boolean type
# * Except graps all the columsn less the ones in the except clause
telco_customer_casted_df = spark.sql("""
    SELECT
        customerID,
        BOOLEAN(Dependents),
        BOOLEAN(Partner),
        BOOLEAN(PhoneService),
        BOOLEAN(PaperlessBilling),
        * 
        EXCEPT (customerID, Dependents, Partner, PhoneService, PaperlessBilling, Churn),
        Churn
    FROM telco_customer_churn_temp_view
""")

telco_customer_casted_df.select("Dependents","Partner","PaperlessBilling", "PhoneService").printSchema()
# -

# ### [Saving to Persistent Tables](https://spark.apache.org/docs/latest/sql-data-sources-load-save-functions.html#saving-to-persistent-tables)
# DataFrames can also be saved as persistent tables into Hive metastore using the saveAsTable command. Notice that an existing Hive deployment is not necessary to use this feature. Spark will create a default local Hive metastore (using Derby) for you. Unlike the `createOrReplaceTempView` command, `saveAsTable` will materialize the contents of the DataFrame and create a pointer to the data in the Hive metastore. Persistent tables will still exist even after your Spark program has restarted, as long as you maintain your connection to the same metastore. A DataFrame for a persistent table can be created by calling the table method on a SparkSession with the name of the table.
#
# For file-based data source, e.g. text, parquet, json, etc. you can specify a custom table path via the path option, e.g. `df.write.option("path", "/some/path").saveAsTable("t")`.
#
# See this [StackOverflow Question](https://stackoverflow.com/questions/44011846/how-does-createorreplacetempview-work-in-spark) also - "Unlike a traditional temp table, a temp view is NOT materialized at all even to memory. It's useful for accessing data in SQL but understand that its statements have to be evaluated EVERY time it's accessed."

# METHOD 4 - Cast using SQL in PySpark directly against a Spark Dataframe
# Tenure months to Long/Integer using .selectExpr
telco_customer_casted_df = telco_customer_churn_df.selectExpr("* except(tenure)", "cast(tenure as long) tenure")
telco_customer_casted_df.select("tenure").printSchema()

# +
telco_customer_name_full = "telco_customer_full"

# [OPTIONAL] Save as DELTA table (silver) in the Hive Metastore
telco_customer_full_silver = f"{telco_customer_name_full}_silver"
telco_customer_casted_df.write.mode("overwrite").option("mergeSchema",True).saveAsTable(telco_customer_full_silver)
# print(telco_customer_casted_df)
# -

# ### [How Does Schema Evolution Work?](https://www.databricks.com/blog/2019/09/24/diving-into-delta-lake-schema-enforcement-evolution.html)
#
# By including the mergeSchema option in your query, any columns that are present in the DataFrame but not in the target table are automatically added on to the end of the schema as part of a write transaction. Nested fields can also be added, and these fields will get added to the end of their respective struct columns as well.
#
# Data engineers and scientists can use this option to add new columns (perhaps a newly tracked metric, or a column of this month's sales figures) to their existing machine learning production tables without breaking existing models that rely on the old columns.
#
# The following types of schema changes are eligible for schema evolution during table appends or overwrites:
#
# - Adding new columns (this is the most common scenario)
# - Changing of data types from NullType -> any other type, or upcasts from ByteType -> ShortType -> IntegerType
#
# Other changes, which are not eligible for schema evolution, require that the schema and data are overwritten by adding .option("overwriteSchema", "true"). For example, in the case where the column "Foo" was originally an integer data type and the new schema would be a string data type, then all of the Parquet (data) files would need to be re-written.  Those changes include:
#
# - Dropping a column
# - Changing an existing column's data type (in place)
# - Renaming column names that differ only by case (e.g. "Foo" and "foo")

#
# ### Handling Outliers
#
# We will see how to handle outliers in column by identifying and addressing data points that fall far outside the typical range of values in a dataset. Common methods for handling outliers include removing them, filtering, transforming the data, or replacing outliers with more representative values. 
#
# Follow these steps for handling outliers:
# * Create a new silver table named as **`telco_customer_full_silver`** by appending **`silver`** to the original table name and then accessing it using Spark SQL. (NOTE: This was done above.)
#
# * Filtering out outliers from the **`TotalCharges`** column by removing rows where the column value exceeds the specified cutoff value.

# Filtering out outliers from the **`TotalCharges`** column by removing rows where the column value exceeds the specified cutoff value (e.g. negative values)

telco_customer_casted_df.select("TotalCharges", "tenure").display()

# +
from pyspark.sql.functions import col


# Remove customers with negative TotalCharges 
TotalCharges_cutoff = 0

print(f"Initial # of rows in df: {telco_customer_casted_df.count()}")

# Use .filter method and SQL col() function
# Charges < $0 are removed as a business rule
# Null values are kept to allow for further processing and analysis to develop a data imputation scheme
telco_no_outliers_df = telco_customer_casted_df.filter(\
    (col("TotalCharges") >= TotalCharges_cutoff) | \
    (col("TotalCharges").isNull())) # Keep Nulls

print(f"# rows after removing outliers from 'Total Charges' column: {telco_no_outliers_df.count()}")
# -

# **Removing outliers from PaymentMethod**
# * Identify the two lowest occurrence groups in the **`PaymentMethod`** column and calculating the total count and average **`MonthlyCharges`** for each group.
#
# * Remove customers from the identified low occurrence groups in the **`PaymentMethod`** column to filter out outliers.
#
# * Create a new dataframe **`telco_filtered_df`** containing the filtered data.
#
# * Comparing the count of records before and after by divinding the count of **`telco_casted_full_df`** and **`telco_no_outliers_df`** dataframe removing outliers and then materializing the resulting dataframe as a new table.

# +
from pyspark.sql.functions import col, count, avg


# Identify 2 lowest group occurences
group_var = "PaymentMethod"
stats_df = telco_no_outliers_df.groupBy(group_var) \
                      .agg(count("*").alias("Total"),\
                           avg("MonthlyCharges").alias("MonthlyCharges")) \
                      .orderBy(col("Total").desc())

# Display
display(stats_df)
# -

# Gather 2 lowest groups name assuming count threshold is below 20% of full dataset and monthly charges <20$
# NOTE: This shows the logic, but no rows actually meet the two conditions. Thus, no rows are removed in this example
N = telco_no_outliers_df.count()  # total count
lower_groups = [elem[group_var] for elem in stats_df.tail(2) if elem['Total']/N < 0.2 and elem['MonthlyCharges'] < 20]
print(f"Removing groups: {','.join(lower_groups)}")

# +
print(f"Initial # of rows in df: {telco_customer_casted_df.count()}")
print(f"# rows after removing outliers from 'Total Charges' column: {telco_no_outliers_df.count()}")

# Filter/Remove listings from these low occurence groups
# Keep null occurences to allow for data imputation later
telco_no_outliers_df = telco_no_outliers_df.filter( \
    ~col(group_var).isin(lower_groups) | \
    col(group_var).isNull())

print(f"# rows after also removing outliers by counts of total payments and monthly charges: {telco_no_outliers_df.count()}")
# -

# Count/Compare datasets before/after removing outliers
print(f"Count - Before: {telco_customer_casted_df.count()} / After: {telco_no_outliers_df.count()}")

# Materialize/Snap table [OPTIONAL/for instructor only]
telco_no_outliers_df.write.mode("overwrite").saveAsTable(telco_customer_full_silver)

#
# ### Handling Missing Values
#
# To Handle missing values in dataset we need to identify columns with high percentages of missing data and drops those columns. Then, it removes rows with missing values. Numeric columns are imputed with 0, and string columns are imputed with 'N/A'. Overall, the code demonstrates a comprehensive approach to handling missing values in the dataset.

#
# #### Delete Columns 
#
# * Create a DataFrame called **`missing_df`** to count the missing values per column in the **`telco_no_outliers_df`** dataset.
#
# * The **`missing_df`** DataFrame is then transposed for better readability using the TransposeDF function, which allows for easier analysis of missing values.

# +
from pyspark.sql.functions import col, when, count, concat_ws, collect_list # isnan


def calculate_missing(input_df, show=True):
  """
  Helper function to calculate and display missing data
  """

  # First get count of missing values per column to get a singleton row DF
  missing_df_ = input_df.select([count(when(col(c).contains('None') | \
                                                  col(c).contains('NULL') | \
                                                  (col(c) == '' ) | \
                                                  col(c).isNull(), c)).alias(c) \
                                                  for c in input_df.columns
                                            ])

  # Transpose for better readability
  def TransposeDF(df, columns, pivotCol):
    """Helper function to transpose spark dataframe"""
    columnsValue = list(map(lambda x: str("'") + str(x) + str("',")  + str(x), columns)) # E.g., ["'customer_ID',customerID", "'Dependents',Dependents",...]
    stackCols = ','.join(x for x in columnsValue) # Change list to string and join values using ',', e.g., "'customer_ID',customerID,'Dependents',Dependents,..."
    
    # SQL stack call - https://spark.apache.org/docs/latest/api/sql/index.html#stack
    #   str(len(columns)) = number of rows desired
    #   stackCols = expressions to evaluate and place into rows
    #   col0 = column name, e.g., 'InternetService'
    #   col1 = column value, e.g., 6570
    # pivotCol will be column with name, e.g., "Column" and values of, e.g., "Number of Missing Values"
    df_1 = df.selectExpr(pivotCol, "stack(" + str(len(columns)) + "," + stackCols + ")")\
            .select(pivotCol, "col0", "col1") # Don't think this term is required but included in review

    # concat_ws is a "trick" that allows us to aggregate the counts as strings... could redo as sum to make it more interpretable; type will be bigint... string probably makes this function more general though
    # col0 - has column names
    # pivotCol - has "Number of Missing Values" for each row (stack created many rows with "Column" column extended)
    final_df = df_1.groupBy(col("col0")).pivot(pivotCol).agg(concat_ws("", collect_list(col("col1")))).withColumnRenamed("col0", pivotCol)
    #final_df = df_1.groupBy(col("col0")).pivot(pivotCol).agg({"col1": "sum"}).withColumnRenamed("col0", pivotCol)
    return final_df

  missing_df_out_T = TransposeDF(
    spark.createDataFrame([{"Column":"Number of Missing Values"}]).join(missing_df_), # Add "Column" column with a value of "Number of Missing Values" to missing_df_ (a singleton row df)
    missing_df_.columns,
    "Column"
  ).withColumn("Number of Missing Values", col("Number of Missing Values").cast("long"))

  if show:
    display(missing_df_out_T.orderBy("Number of Missing Values", ascending=False))

  return missing_df_out_T

missing_df = calculate_missing(telco_no_outliers_df)
# -

# **Drop columns with more than x% of missing rows**
#
# Columns with more than 60% missing data are identified and stored in the **`to_drop_missing`** list, and these columns are subsequently dropped from the **`telco_no_outliers_df`** dataset.

# +
per_thresh = 0.6  # Drop if column has more than 60% missing data

N = telco_no_outliers_df.count()  # total count

# Why are we looping... we should be able to exploit vectorization here
#to_drop_missing = [x.asDict()['Column'] for x in missing_df.select("Column").where(col("Number of Missing Values") / N >= per_thresh).collect()]

# My attempt
to_drop_missing = missing_df.select("Column").where(col("Number of Missing Values") / N >= per_thresh).toPandas()["Column"].values
# -

print(f"Dropping columns {to_drop_missing} for more than {per_thresh * 100}% missing data")
telco_no_missing_df = telco_no_outliers_df.drop(*to_drop_missing)
# display(telco_no_missing_df)

# **Drop rows containing specific numbers of missing columns/fields**
#
# Rows with more than 1/4 the columns missing values are dropped using the **`na.drop()`** and the remaining missing values in numeric columns are imputed with 0, while missing values in string columns are imputed with 'N/A'.

n_cols = len(telco_no_missing_df.columns)
telco_no_missing_df = telco_no_missing_df.na.drop(how='any', thresh=round(n_cols/4)) # Drop rows where at least a quarter of values are missing, how='all' can also be used

# +
# Count/Compare datasets before/after removing missing
print(f"Count - Before: {telco_no_outliers_df.count()} / After: {telco_no_missing_df.count()}")

# NOTE: In this example, none of the rows had more than 25% of their data missing, so no additional rows were dropped
# -

#
# #### Impute Missing Data
#
# Replace missing values with a specified replacement value.
#
# * The **`num_cols`** and **`string_cols`** lists are created to identify numeric and string columns in the dataset, respectively.
#
# * Finally, missing values in the numeric and string columns are imputed with appropriate values using the **`na.fill()`**, resulting in the **`telco_imputed_df`** dataset.
#
# NOTE: We are still focused on business rules at this point. We are not imputing with numerical values, e.g., mean and median, as that must be done when we split our data, i.e., create train, validation, and test sets, in order to avoid data leakage.

# **Replace numeric missing with constant/0**
#
# NOTE: not applicable in this dataset's case

# +
from pyspark.sql.types import DoubleType, IntegerType


# Get a list of numeric columns
num_cols = [c.name for c in telco_no_missing_df.schema.fields if (c.dataType == DoubleType() or c.dataType == IntegerType())]

# +
# Impute
telco_imputed_df = telco_no_missing_df.na.fill(value=0, subset=num_cols)

# NOTE: We are still focused on business rules at this point. We are not imputing with numerical values, e.g., mean and median, as that must be done when we split our data, i.e., create train, validation, and test sets, in order to avoid data leakage.
# This code serves as a template
# -

# **Replace boolean missing with `False`**

# +
from pyspark.sql.types import BooleanType


# Get a list of boolean columns
bool_cols = [c.name for c in telco_no_missing_df.schema.fields if (c.dataType == BooleanType())]

# Impute
telco_imputed_df = telco_no_missing_df.na.fill(value=False, subset=bool_cols)
# -

# **Replace string missing with `No`**
#
# All string cols except `gender`, `Contract` and `PaymentMethod`

# +
from pyspark.sql.types import StringType


# Get list of string cols
to_exclude = ["customerID", "gender", "Contract", "PaymentMethod"]
string_cols = [c.name for c in telco_no_missing_df.drop(*to_exclude).schema.fields if c.dataType == StringType()]

# Impute
telco_imputed_df = telco_imputed_df.na.fill(value='No', subset=string_cols)
# -

# Compare missing stats again
calculate_missing(telco_imputed_df)

telco_imputed_df.write.mode("overwrite").saveAsTable(f"{DA.catalog_name}.{DA.schema_name}.telco_imputed_silver")

#
# ## Encoding Categorical Features
#
# In this section, we will one-hot encode categorical/string features using Spark MLlib's `OneHotEncoder` estimator.
#
# If you are unfamiliar with one-hot encoding, there's a description below. If you're already familiar, you can skip ahead to the **One-hot encoding in Spark MLlib** section toward the bottom of the cell.
#
# #### Categorical features in machine learning
#
# Many machine learning algorithms are not able to accept categorical features as inputs. As a result, data scientists and machine learning engineers need to determine how to handle them. 
#
# An easy solution would be remove the categorical features from the feature set. While this is quick, **you are removing potentially predictive information** &mdash; so this usually isn't the best strategy.
#
# Other options include ways to represent categorical features as numeric features. A few common options are:
#
# 1. **One-hot encoding**: create dummy/binary variables for each category
# 2. **Target/label encoding**: replace each category value with a value that represents the target variable (e.g. replace a specific category value with the mean of the target variable for rows with that category value)
# 3. **Embeddings**: use/create a vector-representation of meaningful words in each category's value
#
# Each of these options can be really useful in different scenarios. We're going to focus on one-hot encoding here.
#
# #### One-hot encoding basics
#
# One-hot encoding creates a binary/dummy feature for each category in each categorical feature.
#
# In the example below, the feature **Animal** is split into three binary features &mdash; one for each value in **Animal**. Each binary feature's value is equal to 1 if its respective category value is present in **Animal** for each row. If its category value is not present in the row, the binary feature's value will be 0.
#
# ![One-hot encoding image](https://s3-us-west-2.amazonaws.com/files.training.databricks.com/images/mlewd/Scaling-Machine-Learning-Pipelines/one-hot-encoding.png)
#
# #### One-hot encoding in Spark MLlib
#
# Even if you understand one-hot encoding, it's important to learn how to perform it using Spark MLlib.
#
# To one-hot encode categorical features in Spark MLlib, we are going to use two classes: [the **`StringIndexer`** class](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.feature.StringIndexer.html#pyspark.ml.feature.StringIndexer) and [the **`OneHotEncoder`** class](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.feature.OneHotEncoder.html#pyspark.ml.feature.OneHotEncoder).
#
# * The `StringIndexer` class indexes string-type columns to a numerical index. Each unique value in the string-type column is mapped to a unique integer.
# * The `OneHotEncoder` class accepts indexed columns and converts them to a one-hot encoded vector-type feature.
#
# #### Applying the `StringIndexer` -> `OneHotEncoder` -> `VectorAssembler`workflow
#
# First, we'll need to index the categorical features of the DataFrame. `StringIndexer` takes a few arguments:
#
# 1. A list of categorical columns to index.
# 2. A list names for the indexed columns being created.
# 3. Directions for how to handle new categories when transforming data.
#
# Because `StringIndexer` has to learn which categories are present before indexing, it's an **estimator** &mdash; remember that means we need to call its `fit` method. Its result can then be used to transform our data.

# Create a sample df to apply StringIndexer to
sample_df = telco_imputed_df.select("Contract").distinct()
sample_df.show()

# +
from pyspark.ml.feature import StringIndexer
from pyspark.sql.functions import col


# StringIndexer
string_cols = ["Contract"]
index_cols = [column + "_index" for column in string_cols]

string_indexer = StringIndexer(inputCols=string_cols, outputCols=index_cols, handleInvalid="skip")
string_indexer_model = string_indexer.fit(sample_df)
indexed_df = string_indexer_model.transform(sample_df)

indexed_df.show()
# -

# Once our data has been indexed, we are ready to use the `OneHotEncoder` estimator.
#
# <img src="https://files.training.databricks.com/images/icon_hint_24.png"/>&nbsp;**Hint:** Look at the [`OneHotEncoder` documentation](https://spark.apache.org/docs/latest/api/python/reference/api/pyspark.ml.feature.OneHotEncoder.html#pyspark.ml.feature.OneHotEncoder) and our previous Spark MLlib workflows that use estimators for guidance.

# +
from pyspark.ml.feature import OneHotEncoder


# Create a list of one-hot encoded feature names
ohe_cols = [column + "_ohe" for column in string_cols]

# Instantiate the OneHotEncoder with the column lists
ohe = OneHotEncoder(inputCols=index_cols, outputCols=ohe_cols, handleInvalid="keep", dropLast=True)

# Fit the OneHotEncoder on the indexed data
ohe_model = ohe.fit(indexed_df)

# Transform indexed_df using the ohe_model
# NOTE: This will return a sparse representation of the ohe_model
ohe_df = ohe_model.transform(indexed_df)
ohe_df.show()

# +
from pyspark.ml.feature import VectorAssembler

# NOTE: This flow will transform the sparse representation into a humna readable format

selected_ohe_cols = ["Contract_ohe"]

# Use VectorAssembler to assemble the selected one-hot encoded columns into a dense vector
assembler = VectorAssembler(inputCols=selected_ohe_cols, outputCol="features")
result_df_dense = assembler.transform(ohe_df)

# Select relevant columns for display
result_df_display = result_df_dense.select("Contract", "features")

result_df_display.show(truncate=False)
result_df_display.printSchema()
# -

# To ensure we do not have any collinearity between our features in the onehot enconding, we should drop one of the columns within the array/vector to ensure the columns remain independent. In this case, we can see the columns are linearly dependent given they all sum to one.

# +
from pyspark.sql.functions import udf
from pyspark.sql.types import ArrayType, DoubleType
from pyspark.ml.linalg import VectorUDT, Vectors

# Define UDF to remove the last element from the vector
def remove_last_element(vector):
    array = vector.toArray()
    return Vectors.dense(array[:-1])

remove_last_element_udf = udf(remove_last_element, VectorUDT())

# Apply the UDF to the DataFrame column
temp_df = result_df_display.withColumn("features", remove_last_element_udf(col("features")))

temp_df.show(truncate=False)
# -

#
# ### Apply pre-existing embeddings to categorical/discrete features

# Let's bin **`tenure`** to convert the discrete data into bins/categories format for further analysis and modeling.

column_to_bin = "tenure"
display(telco_imputed_df.select(column_to_bin))

# +
from pyspark.ml.feature import Bucketizer
from pyspark.sql.functions import col


# Specify bin ranges and column to bin
bucketizer = Bucketizer(
    splits=[0, 24, 48, float('Inf')],
    inputCol=column_to_bin,
    outputCol=f"{column_to_bin}_bins"
)

# Apply the bucketizer to the DataFrame
bins_df = bucketizer.transform(telco_imputed_df.select(column_to_bin))

# Recast bin numbers to integer
bins_df = bins_df.withColumn(f"{column_to_bin}_bins", col(f"{column_to_bin}_bins").cast("integer"))

# Display the result
display(bins_df)

# -

# Map back to human-readable embedding scores

bins_embedded_df = (
  bins_df.withColumn(f"{column_to_bin}_embedded", col(f"{column_to_bin}_bins").cast(StringType()))
         .replace(to_replace = 
                  {
                    "0":"<2y",
                    "1":"2-4y",
                    "2":">4y"
                  },
                  subset=[f"{column_to_bin}_embedded"])
)
display(bins_embedded_df)

#
# ### Ordered Indexing
#
# Perform ordered indexing as an alternative categorical feature preparation for random forest modeling.
#
# Some categoricals are in fact `ordinal` and thus may require additional/manual encoding

ordinal_cat = "Contract"
telco_imputed_df.select(ordinal_cat).distinct().show(truncate=False)

# +
# Define Ordinal (category:index) map/dict
ordered_list = [
    "Month-to-month",
    "One year",
    "Two year"
]

ordinal_dict = {category: f"{index+1}" for index, category in enumerate(ordered_list)}
display(ordinal_dict)

# +
# Create a new column with ordered indexing
from pyspark.sql.functions import expr


ordinal_df = (
    telco_imputed_df
    .withColumn(f"{ordinal_cat}_ord", col(ordinal_cat)) # Duplicate
    .replace(to_replace=ordinal_dict, subset=[f"{ordinal_cat}_ord"]) # Map 
    .withColumn(f"{ordinal_cat}_ord", col(f"{ordinal_cat}_ord").cast('int')) # Cast to integer
)

display(ordinal_df.select(ordinal_cat, f"{ordinal_cat}_ord"))
# -

#
# ## Splitting Data (for Cross-Validation)
#
# Split modeling data into a train-test-holdout split as part of a modeling process
#
# In this section, we will perform the best-practice workflow for a train-test split using the Spark DataFrame API.
#
# Recall that due to things like changing cluster configurations and data partitioning, it can be difficult to ensure a reproducible train-test split. As a result, we recommend:
#
# 1. Split the data using the **same random seed**
# 2. Write out the train and test DataFrames
#
# <img src="https://files.training.databricks.com/images/icon_hint_24.png"/>&nbsp;**Hint:** Check out the [**`randomSplit`** documentation](https://spark.apache.org/docs/3.1.3/api/python/reference/api/pyspark.sql.DataFrame.randomSplit.html).

# Split with 80 percent of the data in train_df and 20 percent of the data in test_df
train_df, test_df = telco_imputed_df.randomSplit([.8, .2], seed=42)

# Materialize (OPTIONAL)
train_df.write.mode("overwrite").option("overwriteSchema", True).saveAsTable(f"{DA.catalog_name}.{DA.schema_name}.telco_customers_train")
test_df.write.mode("overwrite").option("overwriteSchema", True).saveAsTable(f"{DA.catalog_name}.{DA.schema_name}.telco_customers_baseline")

#
# ### Standardize Features in a Training Set
#
# For sake of example, we'll pick a column without missing data (e.g. `MonthlyCharges`)

# +
from pyspark.ml.feature import StandardScaler, RobustScaler, VectorAssembler


num_cols_to_scale = ["MonthlyCharges"] # num_cols
assembler = VectorAssembler().setInputCols(num_cols_to_scale).setOutputCol("numerical_assembled")
train_assembled_df = assembler.transform(train_df.select(*num_cols_to_scale))
test_assembled_df = assembler.transform(test_df.select(*num_cols_to_scale))

# Define scaler and fit on training set
# Robust Scaler - removes the median and scales by the IQR
scaler = RobustScaler(inputCol="numerical_assembled", outputCol="numerical_scaled")
scaler_fitted = scaler.fit(train_assembled_df)


# Apply to both training and test set
train_scaled_df = scaler_fitted.transform(train_assembled_df)
test_scaled_df = scaler_fitted.transform(test_assembled_df)
# -

print("Peek at Training set")
train_scaled_df.show(5)

print("Peek at Test set")
test_scaled_df.show(5)

# ### Impute categorical missing values with the mode value using sparkml
#
# How to handle missing data only at training time and bake as part of inference pipeline to avoid data leakage and ensure that observation with missing data is used for training.

# Index categoricals first as `Imputer` doesn't handle categoricals directly

# +
from pyspark.ml.feature import StringIndexer
from pyspark.sql.functions import col

categorical_cols_to_impute = ["PaymentMethod"] # string_cols

# Index categorical columns using StringIndexer
cat_index_cols = [column + "_index" for column in categorical_cols_to_impute]
cat_indexer = StringIndexer(
    inputCols=categorical_cols_to_impute,
    outputCols=cat_index_cols,
    handleInvalid="keep"
)

# Fit on training set
cat_indexer_model = cat_indexer.fit(train_df.select(categorical_cols_to_impute))
# -

# Transform both train & test set using the fitted StringIndexer model
cat_indexed_train_df = cat_indexer_model.transform(train_df.select(*categorical_cols_to_impute))
cat_indexed_test_df = cat_indexer_model.transform(test_df.select(*categorical_cols_to_impute))
# display(cat_indexed_train_df)

cat_indexed_train_df.display()

# The `StringIndexer` will create a new label (_e.g._ `4`) for missing when setting the `handleInvalid` flag to `keep` so it's important to keep track/revert indexes values back to `null` if we want to impute them, otherwise `null` will be treated as their own/separate category automatically.
#
# Alternatively for imputing categorical/strings, we can use `.fillna()` method by providing the `mode` value manually (as described above).

# Revert indexes to `null` for missing categories
for c in categorical_cols_to_impute:
    cat_indexed_train_df = cat_indexed_train_df.withColumn(f"{c}_index", when(col(c).isNull(), None).otherwise(col(f"{c}_index")))
    cat_indexed_test_df = cat_indexed_test_df.withColumn(f"{c}_index", when(col(c).isNull(), None).otherwise(col(f"{c}_index")))

cat_indexed_train_df.display()

# Fit the imputer on indexed categoricals

# +
from pyspark.ml.feature import Imputer


# Define 'mode' imputer
output_cat_index_cols_imputed = [col+'_imputed' for col in cat_index_cols]
mode_imputer = Imputer(
  inputCols=cat_index_cols,
  outputCols=output_cat_index_cols_imputed,
  strategy="mode"
  )

# Fit on training_df
mode_imputer_fitted = mode_imputer.fit(cat_indexed_train_df)
# -

# Transform both training & test sets
cat_indexed_train_imputed_df = mode_imputer_fitted.transform(cat_indexed_train_df)
cat_indexed_test_imputed_df  = mode_imputer_fitted.transform(cat_indexed_test_df)

# Peek at test set
# NOTE: The mode was PaymentMethod = Electronic check with a PaymentMethod_index of 0... null values will have a 0 value when imputed 
display(cat_indexed_test_imputed_df)

#
# ## Clean up Classroom
#
# Run the following cell to remove lessons-specific assets created during this lesson.

DA.cleanup()

#
# ## Conclusion
#
# This demo successfully provided a comprehensive understanding of data preparation for modeling and feature preparation, equipping you with the knowledge and skills to effectively prepare your data for modeling and analysis. We seamlessly saw how to correct data type, identifying and removing outliers, handling missing values through imputation or replacement, encoding categorical features, and standardizing features.

# &copy; 2024 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
