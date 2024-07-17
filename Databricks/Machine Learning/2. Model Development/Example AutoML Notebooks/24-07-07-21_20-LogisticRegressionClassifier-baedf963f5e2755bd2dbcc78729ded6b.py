# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.3
# ---

# # Logistic Regression Classifier training
# - This is an auto-generated notebook.
# - To reproduce these results, attach this notebook to a cluster with runtime version **13.3.x-cpu-ml-scala2.12**, and rerun it.
# - Compare trials in the [MLflow experiment](#mlflow/experiments/1249599295316005).
# - Clone this notebook into your project folder by selecting **File > Clone** in the notebook toolbar.

# +
import mlflow
import databricks.automl_runtime

target_col = "Churn"
# -

# ## Load Data

# +
import mlflow
import os
import uuid
import shutil
import pandas as pd

# Create temp directory to download input data from MLflow
input_temp_dir = os.path.join(os.environ["SPARK_LOCAL_DIRS"], "tmp", str(uuid.uuid4())[:8])
os.makedirs(input_temp_dir)


# Download the artifact and read it into a pandas DataFrame
input_data_path = mlflow.artifacts.download_artifacts(run_id="ae107c444e80400b836a3f774360d077", artifact_path="data", dst_path=input_temp_dir)

df_loaded = pd.read_parquet(os.path.join(input_data_path, "training_data"))
# Delete the temp data
shutil.rmtree(input_temp_dir)

# Preview data
df_loaded.head(5)
# -

# ### Select supported columns
# Select only the columns that are supported. This allows us to train a model that can predict on a dataset that has extra columns that are not used in training.
# `[]` are dropped in the pipelines. See the Alerts tab of the AutoML Experiment page for details on why these columns are dropped.

from databricks.automl_runtime.sklearn.column_selector import ColumnSelector
supported_cols = ["Contract", "TotalCharges", "Partner", "PaymentMethod", "PaperlessBilling", "Tenure", "InternetService", "Gender", "SeniorCitizen"]
col_selector = ColumnSelector(supported_cols)

# ## Preprocessors

# ### Boolean columns
# For each column, impute missing values and then convert into ones and zeros.

# +
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import OneHotEncoder as SklearnOneHotEncoder


bool_imputers = []

bool_pipeline = Pipeline(steps=[
    ("cast_type", FunctionTransformer(lambda df: df.astype(object))),
    ("imputers", ColumnTransformer(bool_imputers, remainder="passthrough")),
    ("onehot", SklearnOneHotEncoder(handle_unknown="ignore", drop="first")),
])

bool_transformers = [("boolean", bool_pipeline, ["Gender", "SeniorCitizen", "Partner", "PaperlessBilling"])]
# -

# ### Numerical columns
#
# Missing values for numerical columns are imputed with mean by default.

# +
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, StandardScaler

num_imputers = []
num_imputers.append(("impute_mean", SimpleImputer(), ["SeniorCitizen", "Tenure", "TotalCharges"]))

numerical_pipeline = Pipeline(steps=[
    ("converter", FunctionTransformer(lambda df: df.apply(pd.to_numeric, errors='coerce'))),
    ("imputers", ColumnTransformer(num_imputers)),
    ("standardizer", StandardScaler()),
])

numerical_transformers = [("numerical", numerical_pipeline, ["Tenure", "SeniorCitizen", "TotalCharges"])]
# -

# ### Categorical columns

# #### Low-cardinality categoricals
# Convert each low-cardinality categorical column into multiple binary columns through one-hot encoding.
# For each input categorical column (string or numeric), the number of output columns is equal to the number of unique values in the input column.

# +
from databricks.automl_runtime.sklearn import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

one_hot_imputers = []

one_hot_pipeline = Pipeline(steps=[
    ("imputers", ColumnTransformer(one_hot_imputers, remainder="passthrough")),
    ("one_hot_encoder", OneHotEncoder(handle_unknown="indicator")),
])

categorical_one_hot_transformers = [("onehot", one_hot_pipeline, ["Contract", "InternetService", "PaymentMethod"])]

# +
from sklearn.compose import ColumnTransformer

transformers = bool_transformers + numerical_transformers + categorical_one_hot_transformers

preprocessor = ColumnTransformer(transformers, remainder="passthrough", sparse_threshold=0)
# -

# ## Train - Validation - Test Split
# The input data is split by AutoML into 3 sets:
# - Train (60% of the dataset used to train the model)
# - Validation (20% of the dataset used to tune the hyperparameters of the model)
# - Test (20% of the dataset used to report the true performance of the model on an unseen dataset)
#
# `_automl_split_col_0000` contains the information of which set a given row belongs to.
# We use this column to split the dataset into the above 3 sets. 
# The column should not be used for training so it is dropped after split is done.

# +
# AutoML completed train - validation - test split internally and used _automl_split_col_0000 to specify the set
split_train_df = df_loaded.loc[df_loaded._automl_split_col_0000 == "train"]
split_val_df = df_loaded.loc[df_loaded._automl_split_col_0000 == "val"]
split_test_df = df_loaded.loc[df_loaded._automl_split_col_0000 == "test"]

# Separate target column from features and drop _automl_split_col_0000
X_train = split_train_df.drop([target_col, "_automl_split_col_0000"], axis=1)
y_train = split_train_df[target_col]

X_val = split_val_df.drop([target_col, "_automl_split_col_0000"], axis=1)
y_val = split_val_df[target_col]

X_test = split_test_df.drop([target_col, "_automl_split_col_0000"], axis=1)
y_test = split_test_df[target_col]
# -

# ## Train classification model
# - Log relevant metrics to MLflow to track runs
# - All the runs are logged under [this MLflow experiment](#mlflow/experiments/1249599295316005)
# - Change the model parameters and re-run the training cell to log a different trial to the MLflow experiment
# - To view the full list of tunable hyperparameters, check the output of the cell below

# +
from sklearn.linear_model import LogisticRegression

help(LogisticRegression)
# -

# ### Define the objective function
# The objective function used to find optimal hyperparameters. By default, this notebook only runs
# this function once (`max_evals=1` in the `hyperopt.fmin` invocation) with fixed hyperparameters, but
# hyperparameters can be tuned by modifying `space`, defined below. `hyperopt.fmin` will then use this
# function's return value to search the space to minimize the loss.

# +
import mlflow
from mlflow.models import Model, infer_signature, ModelSignature
from mlflow.pyfunc import PyFuncModel
from mlflow import pyfunc
import sklearn
from sklearn import set_config
from sklearn.pipeline import Pipeline

from hyperopt import hp, tpe, fmin, STATUS_OK, Trials

def objective(params):
  with mlflow.start_run(experiment_id="1249599295316005") as mlflow_run:
    sklr_classifier = LogisticRegression(**params)

    model = Pipeline([
        ("column_selector", col_selector),
        ("preprocessor", preprocessor),
        ("classifier", sklr_classifier),
    ])

    # Enable automatic logging of input samples, metrics, parameters, and models
    mlflow.sklearn.autolog(
        log_input_examples=True,
        silent=True)

    model.fit(X_train, y_train)

    
    # Log metrics for the training set
    mlflow_model = Model()
    pyfunc.add_to_model(mlflow_model, loader_module="mlflow.sklearn")
    pyfunc_model = PyFuncModel(model_meta=mlflow_model, model_impl=model)
    training_eval_result = mlflow.evaluate(
        model=pyfunc_model,
        data=X_train.assign(**{str(target_col):y_train}),
        targets=target_col,
        model_type="classifier",
        evaluator_config = {"log_model_explainability": False,
                            "metric_prefix": "training_" , "pos_label": "Yes" }
    )
    sklr_training_metrics = training_eval_result.metrics
    # Log metrics for the validation set
    val_eval_result = mlflow.evaluate(
        model=pyfunc_model,
        data=X_val.assign(**{str(target_col):y_val}),
        targets=target_col,
        model_type="classifier",
        evaluator_config = {"log_model_explainability": False,
                            "metric_prefix": "val_" , "pos_label": "Yes" }
    )
    sklr_val_metrics = val_eval_result.metrics
    # Log metrics for the test set
    test_eval_result = mlflow.evaluate(
        model=pyfunc_model,
        data=X_test.assign(**{str(target_col):y_test}),
        targets=target_col,
        model_type="classifier",
        evaluator_config = {"log_model_explainability": False,
                            "metric_prefix": "test_" , "pos_label": "Yes" }
    )
    sklr_test_metrics = test_eval_result.metrics

    loss = -sklr_val_metrics["val_f1_score"]

    # Truncate metric key names so they can be displayed together
    sklr_val_metrics = {k.replace("val_", ""): v for k, v in sklr_val_metrics.items()}
    sklr_test_metrics = {k.replace("test_", ""): v for k, v in sklr_test_metrics.items()}

    return {
      "loss": loss,
      "status": STATUS_OK,
      "val_metrics": sklr_val_metrics,
      "test_metrics": sklr_test_metrics,
      "model": model,
      "run": mlflow_run,
    }
# -

# ### Configure the hyperparameter search space
# Configure the search space of parameters. Parameters below are all constant expressions but can be
# modified to widen the search space. For example, when training a decision tree classifier, to allow
# the maximum tree depth to be either 2 or 3, set the key of 'max_depth' to
# `hp.choice('max_depth', [2, 3])`. Be sure to also increase `max_evals` in the `fmin` call below.
#
# See https://docs.databricks.com/applications/machine-learning/automl-hyperparam-tuning/index.html
# for more information on hyperparameter tuning as well as
# http://hyperopt.github.io/hyperopt/getting-started/search_spaces/ for documentation on supported
# search expressions.
#
# For documentation on parameters used by the model in use, please see:
# https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html
#
# NOTE: The above URL points to a stable version of the documentation corresponding to the last
# released version of the package. The documentation may differ slightly for the package version
# used by this notebook.

space = {
  "C": 98.82237378192596,
  "l1_ratio": 3.003570665583487e-08,
  "penalty": "elasticnet",
  "solver": "saga",
  "random_state": 686878987,
}

# ### Run trials
# When widening the search space and training multiple models, switch to `SparkTrials` to parallelize
# training on Spark:
# ```
# from hyperopt import SparkTrials
# trials = SparkTrials()
# ```
#
# NOTE: While `Trials` starts an MLFlow run for each set of hyperparameters, `SparkTrials` only starts
# one top-level run; it will start a subrun for each set of hyperparameters.
#
# See http://hyperopt.github.io/hyperopt/scaleout/spark/ for more info.

# +
trials = Trials()
fmin(objective,
     space=space,
     algo=tpe.suggest,
     max_evals=1,  # Increase this when widening the hyperparameter search space.
     trials=trials)

best_result = trials.best_trial["result"]
model = best_result["model"]
mlflow_run = best_result["run"]

display(
  pd.DataFrame(
    [best_result["val_metrics"], best_result["test_metrics"]],
    index=["validation", "test"]))

set_config(display="diagram")
model
# -

# ### Patch pandas version in logged model
#
# Ensures that model serving uses the same version of pandas that was used to train the model.

# +
import mlflow
import os
import shutil
import tempfile
import yaml

run_id = mlflow_run.info.run_id

# Set up a local dir for downloading the artifacts.
tmp_dir = str(tempfile.TemporaryDirectory())
os.makedirs(tmp_dir)

client = mlflow.tracking.MlflowClient()

# Fix conda.yaml
conda_file_path = mlflow.artifacts.download_artifacts(artifact_uri=f"runs:/{run_id}/model/conda.yaml", dst_path=tmp_dir)
with open(conda_file_path) as f:
  conda_libs = yaml.load(f, Loader=yaml.FullLoader)
pandas_lib_exists = any([lib.startswith("pandas==") for lib in conda_libs["dependencies"][-1]["pip"]])
if not pandas_lib_exists:
  print("Adding pandas dependency to conda.yaml")
  conda_libs["dependencies"][-1]["pip"].append(f"pandas=={pd.__version__}")

  with open(f"{tmp_dir}/conda.yaml", "w") as f:
    f.write(yaml.dump(conda_libs))
  client.log_artifact(run_id=run_id, local_path=conda_file_path, artifact_path="model")

# Fix requirements.txt
venv_file_path = mlflow.artifacts.download_artifacts(artifact_uri=f"runs:/{run_id}/model/requirements.txt", dst_path=tmp_dir)
with open(venv_file_path) as f:
  venv_libs = f.readlines()
venv_libs = [lib.strip() for lib in venv_libs]
pandas_lib_exists = any([lib.startswith("pandas==") for lib in venv_libs])
if not pandas_lib_exists:
  print("Adding pandas dependency to requirements.txt")
  venv_libs.append(f"pandas=={pd.__version__}")

  with open(f"{tmp_dir}/requirements.txt", "w") as f:
    f.write("\n".join(venv_libs))
  client.log_artifact(run_id=run_id, local_path=venv_file_path, artifact_path="model")

shutil.rmtree(tmp_dir)
# -

# ## Feature importance
#
# SHAP is a game-theoretic approach to explain machine learning models, providing a summary plot
# of the relationship between features and model output. Features are ranked in descending order of
# importance, and impact/color describe the correlation between the feature and the target variable.
# - Generating SHAP feature importance is a very memory intensive operation, so to ensure that AutoML can run trials without
#   running out of memory, we disable SHAP by default.<br />
#   You can set the flag defined below to `shap_enabled = True` and re-run this notebook to see the SHAP plots.
# - To reduce the computational overhead of each trial, a single example is sampled from the validation set to explain.<br />
#   For more thorough results, increase the sample size of explanations, or provide your own examples to explain.
# - SHAP cannot explain models using data with nulls; if your dataset has any, both the background data and
#   examples to explain will be imputed using the mode (most frequent values). This affects the computed
#   SHAP values, as the imputed samples may not match the actual data distribution.
#
# For more information on how to read Shapley values, see the [SHAP documentation](https://shap.readthedocs.io/en/latest/example_notebooks/overviews/An%20introduction%20to%20explainable%20AI%20with%20Shapley%20values.html).

# Set this flag to True and re-run the notebook to see the SHAP plots
shap_enabled = False

if shap_enabled:
    mlflow.autolog(disable=True)
    mlflow.sklearn.autolog(disable=True)
    from shap import KernelExplainer, summary_plot
    # SHAP cannot explain models using data with nulls.
    # To enable SHAP to succeed, both the background data and examples to explain are imputed with the mode (most frequent values).
    mode = X_train.mode().iloc[0]

    # Sample background data for SHAP Explainer. Increase the sample size to reduce variance.
    train_sample = X_train.sample(n=min(100, X_train.shape[0]), random_state=686878987).fillna(mode)

    # Sample some rows from the validation set to explain. Increase the sample size for more thorough results.
    example = X_val.sample(n=min(100, X_val.shape[0]), random_state=686878987).fillna(mode)

    # Use Kernel SHAP to explain feature importance on the sampled rows from the validation set.
    predict = lambda x: model.predict_proba(pd.DataFrame(x, columns=X_train.columns))
    explainer = KernelExplainer(predict, train_sample, link="logit")
    shap_values = explainer.shap_values(example, l1_reg=False, nsamples=500)
    summary_plot(shap_values, example, class_names=model.classes_)

# ## Inference
# [The MLflow Model Registry](https://docs.databricks.com/applications/mlflow/model-registry.html) is a collaborative hub where teams can share ML models, work together from experimentation to online testing and production, integrate with approval and governance workflows, and monitor ML deployments and their performance. The snippets below show how to add the model trained in this notebook to the model registry and to retrieve it later for inference.
#
# > **NOTE:** The `model_uri` for the model already trained in this notebook can be found in the cell below
#
# ### Register to Model Registry
# ```
# model_name = "Example"
#
# model_uri = f"runs:/{ mlflow_run.info.run_id }/model"
# registered_model_version = mlflow.register_model(model_uri, model_name)
# ```
#
# ### Load from Model Registry
# ```
# model_name = "Example"
# model_version = registered_model_version.version
#
# model_uri=f"models:/{model_name}/{model_version}"
# model = mlflow.pyfunc.load_model(model_uri=model_uri)
# model.predict(input_X)
# ```
#
# ### Load model without registering
# ```
# model_uri = f"runs:/{ mlflow_run.info.run_id }/model"
#
# model = mlflow.pyfunc.load_model(model_uri=model_uri)
# model.predict(input_X)
# ```

# model_uri for the generated model
print(f"runs:/{ mlflow_run.info.run_id }/model")

# ## Confusion matrix, ROC and Precision-Recall curves for validation data
#
# We show the confusion matrix, ROC and Precision-Recall curves of the model on the validation data.
#
# For the plots evaluated on the training and the test data, check the artifacts on the MLflow run page.

# Click the link to see the MLflow run page
displayHTML(f"<a href=#mlflow/experiments/1249599295316005/runs/{ mlflow_run.info.run_id }/artifactPath/model> Link to model run page </a>")

# +
import uuid
from IPython.display import Image

# Create temp directory to download MLflow model artifact
eval_temp_dir = os.path.join(os.environ["SPARK_LOCAL_DIRS"], "tmp", str(uuid.uuid4())[:8])
os.makedirs(eval_temp_dir, exist_ok=True)

# Download the artifact
eval_path = mlflow.artifacts.download_artifacts(run_id=mlflow_run.info.run_id, dst_path=eval_temp_dir)
# -

# ### Confusion matrix for validation dataset

# + large_display_output=true
eval_confusion_matrix_path = os.path.join(eval_path, "val_confusion_matrix.png")
display(Image(filename=eval_confusion_matrix_path))
# -

# ### ROC curve for validation dataset

# + large_display_output=true
eval_roc_curve_path = os.path.join(eval_path, "val_roc_curve_plot.png")
display(Image(filename=eval_roc_curve_path))
# -

# ### Precision-Recall curve for validation dataset

# + large_display_output=true
eval_pr_curve_path = os.path.join(eval_path, "val_precision_recall_curve_plot.png")
display(Image(filename=eval_pr_curve_path))
