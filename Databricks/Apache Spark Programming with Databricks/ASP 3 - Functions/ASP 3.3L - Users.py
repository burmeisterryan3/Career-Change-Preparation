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

# %run ../Includes/Classroom-Setup

# +
# Read in the dataset for the lab, along with all functions

from pyspark.sql.functions import *

df = spark.read.format("delta").load(DA.paths.sales)
display(df)
# -

#
#
# ### 1. Extract item details from purchases
#
# - Explode the **`items`** field in **`df`** with the results replacing the existing **`items`** field
# - Select the **`email`** and **`item.item_name`** fields
# - Split the words in **`item_name`** into an array and alias the column to "details"
#
# Assign the resulting DataFrame to **`details_df`**.

# +
# TODO

from pyspark.sql.functions import *

details_df = (df
              .withColumn("items", explode("items"))
              .select("email", "items.item_name")
              .withColumn("details", split(col("item_name"), " "))
             )
display(details_df)
# -

# Run this cell to check your work
assert details_df.count() == 235911

#
#
#
# So you can see that our **`details`** column is now an array containing the quality, size, and object type.

#
#
# ### 2. Extract size and quality options from mattress purchases
#
# - Filter **`details_df`** for records where **`details`** contains "Mattress"
# - Add a **`size`** column by extracting the element at position 2
# - Add a **`quality`** column by extracting the element at position 1
#
# Save the result as **`mattress_df`**.

# +
# TODO

mattress_df = (details_df
               .filter(array_contains(col("details"), "Mattress"))
               .withColumn("size", element_at(col("details"), 2))
               .withColumn("quality", element_at(col("details"), 1))
              )
display(mattress_df)
# -

# Run this cell to check your work
assert mattress_df.count() == 208384

#
#
#
# Next we're going to do the same thing for pillow purchases.

#
#
#
# ### 3. Extract size and quality options from pillow purchases
# - Filter **`details_df`** for records where **`details`** contains "Pillow"
# - Add a **`size`** column by extracting the element at position 1
# - Add a **`quality`** column by extracting the element at position 2
#
# Note the positions of **`size`** and **`quality`** are switched for mattresses and pillows.
#
# Save result as **`pillow_df`**.

# +
# TODO

pillow_df = (details_df
             .filter(array_contains(col("details"), "Pillow"))
             .withColumn("size", element_at(col("details"), 1))
             .withColumn("quality", element_at(col("details"), 2))
            )
display(pillow_df)
# -

# Run this cell to check your work
assert pillow_df.count() == 27527

#
#
#
# ### 4. Combine data for mattress and pillows
#
# - Perform a union on **`mattress_df`** and **`pillow_df`** by column names
# - Drop the **`details`** column
#
# Save the result as **`union_df`**.

# +
# TODO

union_df = mattress_df.unionByName(pillow_df).drop("details")
display(union_df)
# -

# Run this cell to check your work
assert union_df.count() == 235911

#
#
# ### 5. List all size and quality options bought by each user
#
# - Group rows in **`union_df`** by **`email`**
#   - Collect the set of all items in **`size`** for each user and alias the column to "size options"
#   - Collect the set of all items in **`quality`** for each user and alias the column to "quality options"
#
# Save the result as **`options_df`**.

# +
# TODO

options_df = (union_df
              .groupBy("email")
              .agg(collect_set("size").alias("size options"),
                   collect_set("quality").alias("quality options"))
             )
display(options_df)
# -

# Run this cell to check your work
assert options_df.count() == 210370

#
#
# ### Clean up classroom
#
# And lastly, we'll clean up the classroom.

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
