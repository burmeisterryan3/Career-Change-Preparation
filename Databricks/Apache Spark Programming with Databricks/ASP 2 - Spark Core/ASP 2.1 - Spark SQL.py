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
#
# # Spark SQL
#
# Demonstrate fundamental concepts in Spark SQL using the DataFrame API.
#
# ##### Objectives
# 1. Run a SQL query
# 1. Create a DataFrame from a table
# 1. Write the same query using DataFrame transformations
# 1. Trigger computation with DataFrame actions
# 1. Convert between DataFrames and SQL
#
# ##### Methods
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/spark_session.html" target="_blank">SparkSession</a>: **`sql`**, **`table`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/dataframe.html" target="_blank">DataFrame</a>:
#   - Transformations:  **`select`**, **`where`**, **`orderBy`**
#   - Actions: **`show`**, **`count`**, **`take`**
#   - Other methods: **`printSchema`**, **`schema`**, **`createOrReplaceTempView`**

# %run ../Includes/Classroom-Setup-SQL

#
#
# ## Multiple Interfaces
# Spark SQL is a module for structured data processing with multiple interfaces.
#
# We can interact with Spark SQL in two ways:
# 1. Executing SQL queries
# 1. Working with the DataFrame API.

#
#
# **Method 1: Executing SQL queries**
#
# This is how we interacted with Spark SQL in the previous lesson.

# %sql
SELECT name, price
FROM products
WHERE price < 200
ORDER BY price

#
#
#
# **Method 2: Working with the DataFrame API**
#
# We can also express Spark SQL queries using the DataFrame API.
# The following cell returns a DataFrame containing the same results as those retrieved above.

display(spark
        .table("products")
        .select("name", "price")
        .where("price < 200")
        .orderBy("price")
       )

#
#
#
# We'll go over the syntax for the DataFrame API later in the lesson, but you can see this builder design pattern allows us to chain a sequence of operations very similar to those we find in SQL.

#
#
# ## Query Execution
# We can express the same query using any interface. The Spark SQL engine generates the same query plan used to optimize and execute on our Spark cluster.
#
# ![query execution engine](https://files.training.databricks.com/images/aspwd/spark_sql_query_execution_engine.png)
#
# <img src="https://files.training.databricks.com/images/icon_note_32.png" alt="Note"> Resilient Distributed Datasets (RDDs) are the low-level representation of datasets processed by a Spark cluster. In early versions of Spark, you had to write <a href="https://spark.apache.org/docs/latest/rdd-programming-guide.html" target="_blank">code manipulating RDDs directly</a>. In modern versions of Spark you should instead use the higher-level DataFrame APIs, which Spark automatically compiles into low-level RDD operations.

#
#
# ## Spark API Documentation
#
# To learn how we work with DataFrames in Spark SQL, let's first look at the Spark API documentation.
# The main Spark <a href="https://spark.apache.org/docs/latest/" target="_blank">documentation</a> page includes links to API docs and helpful guides for each version of Spark.
#
# The <a href="https://spark.apache.org/docs/latest/api/scala/org/apache/spark/index.html" target="_blank">Scala API</a> and <a href="https://spark.apache.org/docs/latest/api/python/index.html" target="_blank">Python API</a> are most commonly used, and it's often helpful to reference the documentation for both languages.
# Scala docs tend to be more comprehensive, and Python docs tend to have more code examples.
#
# #### Navigating Docs for the Spark SQL Module
# Find the Spark SQL module by navigating to **`org.apache.spark.sql`** in the Scala API or **`pyspark.sql`** in the Python API.
# The first class we'll explore in this module is the **`SparkSession`** class. You can find this by entering "SparkSession" in the search bar.

#
#
# ## SparkSession
# The **`SparkSession`** class is the single entry point to all functionality in Spark using the DataFrame API.
#
# In Databricks notebooks, the SparkSession is created for you, stored in a variable called **`spark`**.

spark

#
#
#
# The example from the beginning of this lesson used the SparkSession method **`table`** to create a DataFrame from the **`products`** table. Let's save this in the variable **`products_df`**.

products_df = spark.table("products")

#
#
# Below are several additional methods we can use to create DataFrames. All of these can be found in the <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/spark_session.html" target="_blank">documentation</a> for **`SparkSession`**.
#
# #### **`SparkSession`** Methods
# | Method | Description |
# | --- | --- |
# | sql | Returns a DataFrame representing the result of the given query |
# | table | Returns the specified table as a DataFrame |
# | read | Returns a DataFrameReader that can be used to read data in as a DataFrame |
# | range | Create a DataFrame with a column containing elements in a range from start to end (exclusive) with step value and number of partitions |
# | createDataFrame | Creates a DataFrame from a list of tuples, primarily used for testing |

#
#
#
# Let's use a SparkSession method to run SQL.

# +
result_df = spark.sql("""
SELECT name, price
FROM products
WHERE price < 200
ORDER BY price
""")

display(result_df)
# -

#
#
# ## DataFrames
# Recall that expressing our query using methods in the DataFrame API returns results in a DataFrame. Let's store this in the variable **`budget_df`**.
#
# A **DataFrame** is a distributed collection of data grouped into named columns.

budget_df = (spark
             .table("products")
             .select("name", "price")
             .where("price < 200")
             .orderBy("price")
            )

#
#
#
# We can use **`display()`** to output the results of a dataframe.

display(budget_df)

#
#
#
# The **schema** defines the column names and types of a dataframe.
#
# Access a dataframe's schema using the **`schema`** attribute.

budget_df.schema

#
#
#
# View a nicer output for this schema using the **`printSchema()`** method.

budget_df.printSchema()

#
#
# ## Transformations
# When we created **`budget_df`**, we used a series of DataFrame transformation methods e.g. **`select`**, **`where`**, **`orderBy`**.
#
# <strong><code>products_df  
# &nbsp;  .select("name", "price")  
# &nbsp;  .where("price < 200")  
# &nbsp;  .orderBy("price")  
# </code></strong>
#     
# Transformations operate on and return DataFrames, allowing us to chain transformation methods together to construct new DataFrames.
# However, these operations can't execute on their own, as transformation methods are **lazily evaluated**.
#
# Running the following cell does not trigger any computation.

(products_df
  .select("name", "price")
  .where("price < 200")
  .orderBy("price"))

#
#
# ## Actions
# Conversely, DataFrame actions are methods that **trigger computation**.
# Actions are needed to trigger the execution of any DataFrame transformations.
#
# The **`show`** action causes the following cell to execute transformations.

(products_df
  .select("name", "price")
  .where("price < 200")
  .orderBy("price")
  .show()) # use display(query) for pretty table output

#
#
#
# Below are several examples of <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql.html#dataframe-apis" target="_blank">DataFrame</a> actions.
#
# ### DataFrame Action Methods
# | Method | Description |
# | --- | --- |
# | show | Displays the top n rows of DataFrame in a tabular form |
# | count | Returns the number of rows in the DataFrame |
# | describe,  summary | Computes basic statistics for numeric and string columns |
# | first, head | Returns the the first row |
# | collect | Returns an array that contains all rows in this DataFrame |
# | take | Returns an array of the first n rows in the DataFrame |

#
#
# **`count`** returns the number of records in a DataFrame.

budget_df.count()

#
#
# **`collect`** returns an array of all rows in a DataFrame.

budget_df.collect()

#
#
# ## Convert between DataFrames and SQL

#
#
# **`createOrReplaceTempView`** creates a temporary view based on the DataFrame. The lifetime of the temporary view is tied to the SparkSession that was used to create the DataFrame.

budget_df.createOrReplaceTempView("budget")

display(spark.sql("SELECT * FROM budget"))

#
#
# ### Classroom Cleanup

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
