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
# # Explore Datasets Lab
#
# We will use tools introduced in this lesson to explore the datasets used in this course.
#
# ### BedBricks Case Study
# This course uses a case study that explores clickstream data for the online mattress retailer, BedBricks.  
# You are an analyst at BedBricks working with the following datasets: **`events`**, **`sales`**, **`users`**, and **`products`**.
#
# ##### Tasks
# 1. View data files in DBFS using magic commands
# 1. View data files in DBFS using dbutils
# 1. Create tables from files in DBFS
# 1. Execute SQL to answer questions on BedBricks datasets

# %run ../Includes/Classroom-Setup

#
#
# ### 1. List files in DBFS using magic commands
# Use a magic command to display files located in the DBFS directory: **`dbfs:/mnt/dbacademy-users/`**
#
# <img src="https://files.training.databricks.com/images/icon_hint_32.png" alt="Hint"> You should see several user directories including your own. Depending on your permissions, you may see only your user directory.

# %fs
# ls dbfs:/mnt/dbacademy-users/

#
#
# ### 2. List files in DBFS using dbutils
# - Use **`dbutils`** to get the files at the directory above and assign it to the variable **`files`**
# - Use the Databricks display() function to display the contents in **`files`**
#
# <img src="https://files.training.databricks.com/images/icon_hint_32.png" alt="Hint"> Just as before, you should see several user directories including your own.

# TODO
files = dbutils.fs.ls("/mnt/dbacademy-users/")
display(files)

#
#
# ### 3. Create tables below from files in DBFS
# - Create the **`users`** table using the spark-context variable **`DA.paths.users`**
# - Create the **`sales`** table using the spark-context variable **`DA.paths.sales`**
# - Create the **`products`** table using the spark-context variable **`DA.paths.products`**
# - Create the **`events`** table using the spark-context variable **`DA.paths.events`**
#
# <img src="https://files.training.databricks.com/images/icon_hint_32.png"> Hint: We created the **`events`** table in the previous notebook but in a different database.

# +
# %sql
CREATE TABLE IF NOT EXISTS users
USING DELTA
OPTIONS (path = "${DA.paths.users}");

CREATE TABLE IF NOT EXISTS sales
USING DELTA
OPTIONS (path = "${DA.paths.sales}");

CREATE TABLE IF NOT EXISTS products
USING DELTA
OPTIONS (path = "${DA.paths.products}");

CREATE TABLE IF NOT EXISTS events
USING DELTA
OPTIONS (path = "${DA.paths.events}")
# -

#
#
#
# Use the data tab of the workspace UI to confirm your tables were created.

# %sql
DESCRIBE EXTENDED users;

# %sql
DESCRIBE EXTENDED sales;

# %sql
DESCRIBE EXTENDED products;

# %sql
DESCRIBE EXTENDED events;

#
#
# ### 4. Execute SQL to explore BedBricks datasets
# Run SQL queries on the **`products`**, **`sales`**, and **`events`** tables to answer the following questions. 
# - What products are available for purchase at BedBricks?
# - What is the average purchase revenue for a transaction at BedBricks?
# - What types of events are recorded on the BedBricks website?
#
# The schema of the relevant dataset is provided for each question in the cells below.

#
#
#
# #### 4.1: What products are available for purchase at BedBricks?
#
# The **`products`** dataset contains the ID, name, and price of products on the BedBricks retail site.
#
# | field | type | description
# | --- | --- | --- |
# | item_id | string | unique item identifier |
# | name | string | item name in plain text |
# | price | double | price of item |
#
# Execute a SQL query that selects all from the **`products`** table. 
#
# <img src="https://files.training.databricks.com/images/icon_hint_32.png" alt="Hint"> You should see 12 products.

# %sql
SELECT DISTINCT name
FROM products;

#
#
# #### 4.2: What is the average purchase revenue for a transaction at BedBricks?
#
# The **`sales`** dataset contains order information representing successfully processed sales.  
# Most fields correspond directly with fields from the clickstream data associated with a sale finalization event.
#
# | field | type | description|
# | --- | --- | --- |
# | order_id | long | unique identifier |
# | email | string | the email address to which sales configuration was sent |
# | transaction_timestamp | long | timestamp at which the order was processed, recorded in milliseconds since epoch |
# | total_item_quantity | long | number of individual items in the order |
# | purchase_revenue_in_usd | double | total revenue from order |
# | unique_items | long | number of unique products in the order |
# | items | array | provided as a list of JSON data, which is interpreted by Spark as an array of structs |
#
# Execute a SQL query that computes the average **`purchase_revenue_in_usd`** from the **`sales`** table.
#
# <img src="https://files.training.databricks.com/images/icon_hint_32.png" alt="Hint"> The result should be **`1042.79`**.

# %sql
SELECT ROUND(AVG(purchase_revenue_in_usd), 2)
FROM sales;

#
#
# #### 4.3: What types of events are recorded on the BedBricks website?
#
# The **`events`** dataset contains two weeks worth of parsed JSON records, created by consuming updates to an operational database.  
# Records are received whenever: (1) a new user visits the site, (2) a user provides their email for the first time.
#
# | field | type | description|
# | --- | --- | --- |
# | device | string | operating system of the user device |
# | user_id | string | unique identifier for user/session |
# | user_first_touch_timestamp | long | first time the user was seen in microseconds since epoch |
# | traffic_source | string | referral source |
# | geo (city, state) | struct | city and state information derived from IP address |
# | event_timestamp | long | event time recorded as microseconds since epoch |
# | event_previous_timestamp | long | time of previous event in microseconds since epoch |
# | event_name | string | name of events as registered in clickstream tracker |
# | items (item_id, item_name, price_in_usd, quantity, item_revenue in usd, coupon)| array | an array of structs for each unique item in the user’s cart |
# | ecommerce (total_item_quantity, unique_items, purchase_revenue_in_usd)  |  struct  | purchase data (this field is only non-null in those events that correspond to a sales finalization) |
#
# Execute a SQL query that selects distinct values in **`event_name`** from the **`events`** table
#
# <img src="https://files.training.databricks.com/images/icon_hint_32.png" alt="Hint"> You should see 23 distinct **`event_name`** values.

# %sql
SELECT DISTINCT event_name
FROM events;

#
#
# ### Clean up classroom

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
