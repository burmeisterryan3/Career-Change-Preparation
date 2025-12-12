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
#
# # Databricks Platform
#
# Demonstrate basic functionality and identify terms related to working in the Databricks workspace.
#
#
# ##### Objectives
# 1. Execute code in multiple languages
# 1. Create documentation cells
# 1. Access DBFS (Databricks File System)
# 1. Create database and table
# 1. Query table and plot results
# 1. Add notebook parameters with widgets
#
#
# ##### Databricks Notebook Utilities
# - <a href="https://docs.databricks.com/notebooks/notebooks-use.html#language-magic" target="_blank">Magic commands</a>: **`%python`**, **`%scala`**, **`%sql`**, **`%r`**, **`%sh`**, **`%md`**
# - <a href="https://docs.databricks.com/dev-tools/databricks-utils.html" target="_blank">DBUtils</a>: **`dbutils.fs`** (**`%fs`**), **`dbutils.notebooks`** (**`%run`**), **`dbutils.widgets`**
# - <a href="https://docs.databricks.com/notebooks/visualizations/index.html" target="_blank">Visualization</a>: **`display`**, **`displayHTML`**

#
#
#
# ### Setup
# Run classroom setup to <a href="https://docs.databricks.com/data/databricks-file-system.html#mount-storage" target="_blank">mount</a> Databricks training datasets and create your own database for BedBricks.
#
# Use the **`%run`** magic command to run another notebook within a notebook

# %run ../Includes/Classroom-Setup

#
#
#
# ### Execute code in multiple languages
# Run default language of notebook

print("Run default language")

#
#
#
# Run language specified by language magic commands: **`%python`**, **`%scala`**, **`%sql`**, **`%r`**

# %python
print("Run python")

# %scala
println("Run scala")

# %sql
select "Run SQL"

# %r
print("Run R", quote=FALSE)

#
#
#
# Run shell commands on the driver using the magic command: **`%sh`**

# %sh ps | grep 'java'

#
#
#
# Render HTML using the function: **`displayHTML`** (available in Python, Scala, and R)

html = """<h1 style="color:orange;text-align:center;font-family:Courier">Render HTML</h1>"""
displayHTML(html)

#
#
#
# ## Create documentation cells
# Render cell as <a href="https://www.markdownguide.org/cheat-sheet/" target="_blank">Markdown</a> using the magic command: **`%md`**
#
# Below are some examples of how you can use Markdown to format documentation. Click this cell and press **`Enter`** to view the underlying Markdown syntax.
#
#
# # Heading 1
# ### Heading 3
# > block quote
#
# 1. **bold**
# 2. *italicized*
# 3. ~~strikethrough~~
#
# ---
#
# - <a href="https://www.markdownguide.org/cheat-sheet/" target="_blank">link</a>
# - `code`
#
# ```
# {
#   "message": "This is a code block",
#   "method": "https://www.markdownguide.org/extended-syntax/#fenced-code-blocks",
#   "alternative": "https://www.markdownguide.org/basic-syntax/#code-blocks"
# }
# ```
#
# ![Spark Logo](https://files.training.databricks.com/images/Apache-Spark-Logo_TM_200px.png)
#
# | Element         | Markdown Syntax |
# |-----------------|-----------------|
# | Heading         | `#H1` `##H2` `###H3` `#### H4` `##### H5` `###### H6` |
# | Block quote     | `> blockquote` |
# | Bold            | `**bold**` |
# | Italic          | `*italicized*` |
# | Strikethrough   | `~~strikethrough~~` |
# | Horizontal Rule | `---` |
# | Code            | ``` `code` ``` |
# | Link            | `[text](https://www.example.com)` |
# | Image           | `![alt text](image.jpg)`|
# | Ordered List    | `1. First items` <br> `2. Second Item` <br> `3. Third Item` |
# | Unordered List  | `- First items` <br> `- Second Item` <br> `- Third Item` |
# | Code Block      | ```` ``` ```` <br> `code block` <br> ```` ``` ````|
# | Table           |<code> &#124; col &#124; col &#124; col &#124; </code> <br> <code> &#124;---&#124;---&#124;---&#124; </code> <br> <code> &#124; val &#124; val &#124; val &#124; </code> <br> <code> &#124; val &#124; val &#124; val &#124; </code> <br>|

#
#
#
# ## Access DBFS (Databricks File System)
# The <a href="https://docs.databricks.com/data/databricks-file-system.html" target="_blank">Databricks File System</a> (DBFS) is a virtual file system that allows you to treat cloud object storage as though it were local files and directories on the cluster.
#
# Run file system commands on DBFS using the magic command: **`%fs`**
#
# <br/>
# <img src="https://files.training.databricks.com/images/icon_hint_24.png"/>
# Replace the instances of <strong>FILL_IN</strong> in the cells below with your email address:

# %fs mounts

# %fs ls

# %fs ls dbfs:/tmp

# %fs put dbfs:/tmp/FILL_IN.txt "This is a test of the emergency broadcast system, this is only a test" --overwrite=true

# %fs head dbfs:/tmp/FILL_IN.txt

# %fs ls dbfs:/tmp

#
#
#
# **`%fs`** is shorthand for the <a href="https://docs.databricks.com/dev-tools/databricks-utils.html" target="_blank">DBUtils</a> module: **`dbutils.fs`**

# %fs help

#
#
#
# Run file system commands on DBFS using DBUtils directly

dbutils.fs.ls("dbfs:/tmp")
# Equivalent to %fs ls dbfs:/tmp

#
#
#
# Visualize results in a table using the Databricks <a href="https://docs.databricks.com/notebooks/visualizations/index.html#display-function-1" target="_blank">display</a> function

files = dbutils.fs.ls("dbfs:/tmp")
display(files)

#
#
#
# Let's take one more look at our temp file...

# +
file_name = "dbfs:/tmp/FILL_IN.txt"
contents = dbutils.fs.head(file_name)

print("-"*80)
print(contents)
print("-"*80)
# -

#
#
#
# ## Our First Table
#
# Is located in the path identfied by **`DA.paths.events`** (a variable we created for you).
#
# We can see those files by running the following cell

files = dbutils.fs.ls(DA.paths.events)
display(files)

#
#
#
# ## But, Wait!
# I cannot use variables in SQL commands.
#
# With the following trick you can!
#
# Declare the python variable as a variable in the spark context which SQL commands can access:

spark.conf.set("whatever.events", DA.paths.events)

#
#
#
# <img src="https://files.training.databricks.com/images/icon_note_24.png"> In the above example we use **`whatever.`** to give our variable a "namespace".
#
# This is so that we don't accidently step over other configuration parameters.
#
# You will see throughout this course our usage of the "DA" namesapce as in **`DA.paths.some_file`**

#
#
#
# ## Create table
# Run <a href="https://docs.databricks.com/spark/latest/spark-sql/language-manual/index.html#sql-reference" target="_blank">Databricks SQL Commands</a> to create a table named **`events`** using BedBricks event files on DBFS.

# %sql
CREATE TABLE IF NOT EXISTS events
USING DELTA
OPTIONS (path = "${whatever.events}");

# %sql
DESCRIBE EXTENDED events;

#
#
#
# This table was saved in the database created for you in classroom setup.
#
# See database name printed below.

print(f"Database Name: {DA.schema_name}")

#
#
#
# ... or even the tables in that database:

# %sql
SHOW TABLES IN ${DA.schema_name}

#
#
#
# View your database and table in the Data tab of the UI.

#
#
#
# ## Query table and plot results
# Use SQL to query the **`events`** table

# %sql
SELECT * FROM events

#
#
#
# Run the query below and then <a href="https://docs.databricks.com/notebooks/visualizations/index.html#plot-types" target="_blank">plot</a> results by clicking the plus sign (+) and selecting *Visualization*. When presented with a bar chart, click *Save* to add it to the output window.

# %sql
SELECT traffic_source, SUM(ecommerce.purchase_revenue_in_usd) AS total_revenue
FROM events
GROUP BY traffic_source

#
#
#
# ## Add notebook parameters with widgets
# Use <a href="https://docs.databricks.com/notebooks/widgets.html" target="_blank">widgets</a> to add input parameters to your notebook.
#
# Create a text input widget using SQL.

# %sql
CREATE WIDGET TEXT state DEFAULT "CA"

#
#
#
# Access the current value of the widget using the function **`getArgument`**

# %sql
SELECT *
FROM events
WHERE geo.state = getArgument("state")

#
# Remove the text widget

# %sql
REMOVE WIDGET state

#
#
#
# To create widgets in Python, Scala, and R, use the DBUtils module: **`dbutils.widgets`**

dbutils.widgets.text("name", "Brickster", "Name")
dbutils.widgets.multiselect("colors", "orange", ["red", "orange", "black", "blue"], "Favorite Color?")

#
#
#
# Access the current value of the widget using the **`dbutils.widgets`** function **`get`**

# +
name = dbutils.widgets.get("name")
colors = dbutils.widgets.get("colors").split(",")

html = "<div>Hi {}! Select your color preference.</div>".format(name)
for c in colors:
    html += """<label for="{}" style="color:{}"><input type="radio" id="{}"> {}</label><br>""".format(c, c, c, c)

displayHTML(html)
# -

#
#
#
# Remove all widgets

dbutils.widgets.removeAll()

#
#
#
# ### Clean up classroom
# Clean up any temp files, tables and databases created by this lesson

DA.cleanup()

# &copy; 2023 Databricks, Inc. All rights reserved.<br/>
# Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="https://www.apache.org/">Apache Software Foundation</a>.<br/>
# <br/>
# <a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="https://help.databricks.com/">Support</a>
