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
# # Abandoned Carts Lab
# Get abandoned cart items for email without purchases.
# 1. Get emails of converted users from transactions
# 2. Join emails with user IDs
# 3. Get cart item history for each user
# 4. Join cart item history with emails
# 5. Filter for emails with abandoned cart items
#
# ##### Methods
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.join.html#pyspark.sql.DataFrame.join" target="_blank">DataFrame</a>: **`join`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html" target="_blank">Built-In Functions</a>: **`collect_set`**, **`explode`**, **`lit`**
# - <a href="https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameNaFunctions.html#pyspark.sql.DataFrameNaFunctions" target="_blank">DataFrameNaFunctions</a>: **`fill`**

#
#
# ### Setup
# Run the cells below to create DataFrames **`sales_df`**, **`users_df`**, and **`events_df`**.

# %run ../Includes/Classroom-Setup

# sale transactions at BedBricks
sales_df = spark.read.format("delta").load(DA.paths.sales)
display(sales_df)

# user IDs and emails at BedBricks
users_df = spark.read.format("delta").load(DA.paths.users)
display(users_df)

# events logged on the BedBricks website
events_df = spark.read.format("delta").load(DA.paths.events)
display(events_df)

#
#
# ### 1: Get emails of converted users from transactions
# - Select the **`email`** column in **`sales_df`** and remove duplicates
# - Add a new column **`converted`** with the boolean **`True`** for all rows
#
# Save the result as **`converted_users_df`**.

# +
# TODO
from pyspark.sql.functions import *

converted_users_df = (sales_df.select("email").dropDuplicates()
                              .withColumn("converted", lit(True))
                     )
display(converted_users_df)
# -

#
#
# #### 1.1: Check Your Work
#
# Run the following cell to verify that your solution works:

# +
expected_columns = ["email", "converted"]

expected_count = 210370

assert converted_users_df.columns == expected_columns, "converted_users_df does not have the correct columns"

assert converted_users_df.count() == expected_count, "converted_users_df does not have the correct number of rows"

assert converted_users_df.select(col("converted")).first()[0] == True, "converted column not correct"
print("All test pass")
# -

#
#
# ### 2: Join emails with user IDs
# - Perform an outer join on **`converted_users_df`** and **`users_df`** with the **`email`** field
# - Filter for users where **`email`** is not null
# - Fill null values in **`converted`** as **`False`**
#
# Save the result as **`conversions_df`**.

# TODO
conversions_df = (users_df.join(converted_users_df, "email", "outer")
                          .filter(col("email").isNotNull())
                          .na.fill({"converted": False})
                 )
display(conversions_df)

#
#
# #### 2.1: Check Your Work
#
# Run the following cell to verify that your solution works:

# +
expected_columns = ["email", "user_id", "user_first_touch_timestamp", "converted"]

expected_count = 782749

expected_false_count = 572379

assert conversions_df.columns == expected_columns, "Columns are not correct"

assert conversions_df.filter(col("email").isNull()).count() == 0, "Email column contains null"

assert conversions_df.count() == expected_count, "There is an incorrect number of rows"

assert conversions_df.filter(col("converted") == False).count() == expected_false_count, "There is an incorrect number of false entries in converted column"
print("All test pass")
# -

#
#
# ### 3: Get cart item history for each user
# - Explode the **`items`** field in **`events_df`** with the results replacing the existing **`items`** field
# - Group by **`user_id`**
#   - Collect a set of all **`items.item_id`** objects for each user and alias the column to "cart"
#
# Save the result as **`carts_df`**.

# TODO
carts_df = (events_df.withColumn("items", explode(events_df['items']))
                     .groupBy('user_id')
                     .agg(collect_set("items.item_id").alias("cart"))
)
display(carts_df)

#
#
# #### 3.1: Check Your Work
#
# Run the following cell to verify that your solution works:

# +
expected_columns = ["user_id", "cart"]

expected_count = 488403

assert carts_df.columns == expected_columns, "Incorrect columns"

assert carts_df.count() == expected_count, "Incorrect number of rows"

assert carts_df.select(col("user_id")).drop_duplicates().count() == expected_count, "Duplicate user_ids present"
print("All test pass")
# -

#
#
# ### 4: Join cart item history with emails
# - Perform a left join on **`conversions_df`** and **`carts_df`** on the **`user_id`** field
#
# Save result as **`email_carts_df`**.

# TODO
email_carts_df = conversions_df.join(carts_df, ["user_id"], "left_outer")
display(email_carts_df)

#
#
# #### 4.1: Check Your Work
#
# Run the following cell to verify that your solution works:

# +
expected_columns = ["user_id", "email", "user_first_touch_timestamp", "converted", "cart"]

expected_count = 782749

expected_cart_null_count = 397799

assert email_carts_df.columns == expected_columns, "Columns do not match"

assert email_carts_df.count() == expected_count, "Counts do not match"

assert email_carts_df.filter(col("cart").isNull()).count() == expected_cart_null_count, "Cart null counts incorrect from join"
print("All test pass")
# -

#
#
# ### 5: Filter for emails with abandoned cart items
# - Filter **`email_carts_df`** for users where **`converted`** is False
# - Filter for users with non-null carts
#
# Save result as **`abandoned_carts_df`**.

# TODO
abandoned_carts_df = (email_carts_df.filter(col("converted") == False)
                                    .filter(col("cart").isNotNull())
)
display(abandoned_carts_df)

#
#
# #### 5.1: Check Your Work
#
# Run the following cell to verify that your solution works:

# +
expected_columns = ["user_id", "email", "user_first_touch_timestamp", "converted", "cart"]

expected_count = 204272

assert abandoned_carts_df.columns == expected_columns, "Columns do not match"

assert abandoned_carts_df.count() == expected_count, "Counts do not match"
print("All test pass")
# -

#
#
# ### 6: Bonus Activity
# Plot number of abandoned cart items by product

# TODO
abandoned_items_df = (abandoned_carts_df.select(explode("cart").alias("items"))
                                       .groupBy("items")
                                       .agg(count("items").alias("count"))
                     )
display(abandoned_items_df)

#
#
# #### 6.1: Check Your Work
#
# Run the following cell to verify that your solution works:

abandoned_items_df.count()

# +
expected_columns = ["items", "count"]

expected_count = 12

assert abandoned_items_df.count() == expected_count, "Counts do not match"

assert abandoned_items_df.columns == expected_columns, "Columns do not match"
print("All test pass")
# -

#
#
# ### Clean up classroom

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
