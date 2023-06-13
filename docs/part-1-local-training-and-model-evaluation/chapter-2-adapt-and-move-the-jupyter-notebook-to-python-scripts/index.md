# Chapter 2: Adapt and move the Jupyter Notebook to Python scripts

??? info "You want to take over from this chapter? Collapse this section and follow the instructions below."

    !!! warning

        It might be easier to start from the previous chapter(s). Only follow this section if you are confortable with the content of the previous chapter(s).

    Get the required files for this chapter.

    ```sh title="Execute the following command(s) in a terminal"
    # Clone the repository
    git clone \
        --no-checkout \
        --depth=1 \
        --filter=tree:0 \
        https://github.com/csia-pme/a-guide-to-mlops.git

    # Move to the cloned repository
    cd a-guide-to-mlops

    # Get the files for this chapter
    git sparse-checkout set --no-cone docs/the-guide/chapter-1-run-a-simple-ml-experiment

    # Clone the files locally
    git checkout

    # Move back to the root directory
    cd ..

    # Copy the chapter files to the working directory
    cp -r a-guide-to-mlops/docs/the-guide/chapter-1-run-a-simple-ml-experiment/* .

    # Delete the cloned repository
    rm -r a-guide-to-mlops
    ```

    Set up the environment.

    TODO FOR EACH CHAPTER

## Introduction

Jupyter Notebooks provide an interactive environment where code can be executed
and results can be visualized. They combine code, text explanations,
visualizations, and media in a single document, making it a flexible tool to
document a ML experiment.

However, they have severe limitations, such as challenges with reproducibility,
scalability, experiment tracking, and standardization. Integrating Jupyter
Notebooks into Python scripts suitable for running ML experiments in a more
modular and reproducible manner can help address these shortcomings and enhance
the overall ML development process.

pip is the standard package manager for Python. It is used to install and manage dependencies in a Python environment.

Yet, pip is not the best tool to manage Python dependencies. It is not user-friendly and it is not suitable for reproducibility and collaboration.

If you have a look at the `requirements.txt` file, you might notice the following issues:

- Which version of Python is required?
- Which version of the dependencies are required?
- Which dependencies are main dependencies and which are dependencies of dependencies?
- Where to install the dependencies (on my system, in a virtual environment)?
- How to ensure reproducibility?

This is why you will use [Poetry](https://python-poetry.org/) to manage Python dependencies.

Poetry is a tool to manage Python dependencies. It is a more robust and user-friendly alternative to pip. It is also more suitable for reproducibility and collaboration by creating a lock file that can be used to recreate the exact same environment on another machine.

For example, freezing the version of a dependency in a `requirements.txt` file is not enough to ensure reproducibility. The `requirements.txt` file only specifies the version of the dependency at the time of installation. If dependencies of the dependency are updated, the version of the dependency might change without you knowing it. This is why Poetry creates a lock file that contains the exact version of all the dependencies and their dependencies.

In this chapter, you will learn how to:

1. Set up a standardized Python environment using [Poetry](https://python-poetry.org/)
2. Adapt the content of the Jupyter Notebook into Python scripts
3. Launch the experiment locally

The following diagram illustrates control flow of the experiment at the end of
this chapter:

```mermaid
flowchart
    subgraph localGraph[LOCAL]
        data[data.csv] --> prepare
        prepare[prepare.py] --> train
        train[train.py] --> evaluate
        evaluate[evaluate.py]
        params[params.yaml] -.- prepare
        params -.- train
    end
    style data opacity:0.4,color:#7f7f7f80
```

Let's get started!

## Steps

### Move from pip to Poetry

Start by ensuring you have left the virtual environment created in the previous chapter.

```sh title="Execute the following command(s) in a terminal"
# Deactivate the virtual environment
deactivate
```

Remove the virtual environment and the `requirements.txt` file.

```sh title="Execute the following command(s) in a terminal"
# Remove the virtual environment
rm -r .venv

# Remove the requirements.txt file
rm requirements.txt
```

Initialize Poetry at the root of the directory.

```sh title="Execute the following command(s) in a terminal"
poetry init --no-interaction
```

This will create the `pyproject.toml` file that should look like this:

```toml title="pyproject.toml"
[tool.poetry]
name = "a-guide-to-mlops"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "a_guide_to_mlops"}]

[tool.poetry.dependencies]
python = "^3.11"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

Open a Poetry shell. This will automatically create and activate a virtual environment.

```sh title="Execute the following command(s) in a terminal"
# Open a Poetry shell in a new virtual environment
poetry shell
```

Install all the dependencies in the virtual environment.

```sh title="Execute the following command(s) in a terminal"
poetry add "jupyterlab==4.0.2" "pandas==2.0.2" "matplotlib==3.7.1" "scikit-learn==1.2.2" "seaborn==0.12.2"
```

This will install the dependencies in the virtual environment and update the `pyproject.toml` file. You should have something like this:

```toml title="pyproject.toml"
[tool.poetry]
name = "a-guide-to-mlops"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "a_guide_to_mlops"}]

[tool.poetry.dependencies]
python = "^3.11"
jupyterlab = "^4.0.2"
pandas = "^2.0.2"
matplotlib = "^3.7.1"
scikit-learn = "^1.2.2"
seaborn = "^0.12.2"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

A second `poetry.lock` file is also created. This file contains the exact version of all the dependencies and their dependencies.

TODO: Add the correct content of the poetry.lock file

```toml title="poetry.lock"
# This file is automatically @generated by Poetry 1.4.2 and should not be changed by hand.

[[package]]
name = "anyio"
version = "3.7.0"
description = "High level compatibility layer for multiple asynchronous event loop implementations"
category = "main"
optional = false
python-versions = ">=3.7"
files = [
    {file = "anyio-3.7.0-py3-none-any.whl", hash = "sha256:eddca883c4175f14df8aedce21054bfca3adb70ffe76a9f607aef9d7fa2ea7f0"},
    {file = "anyio-3.7.0.tar.gz", hash = "sha256:275d9973793619a5374e1c89a4f4ad3f4b0a5510a2b5b939444bee8f4c4d37ce"},
]

[package.dependencies]
idna = ">=2.8"
sniffio = ">=1.1"

[package.extras]
doc = ["Sphinx (>=6.1.0)", "packaging", "sphinx-autodoc-typehints (>=1.2.0)", "sphinx-rtd-theme", "sphinxcontrib-jquery"]
test = ["anyio[trio]", "coverage[toml] (>=4.5)", "hypothesis (>=4.0)", "mock (>=4)", "psutil (>=5.9)", "pytest (>=7.0)", "pytest-mock (>=3.6.1)", "trustme", "uvloop (>=0.17)"]
trio = ["trio (<0.22)"]

[[package]]
name = "appnope"
version = "0.1.3"
description = "Disable App Nap on macOS >= 10.9"
category = "main"
optional = false
# ... and so on
```

Now that Poetry is set up, accessing the virtual environment is now easier. Simply type `poetry shell` to open a Poetry shell in the virtual environment.

Installing dependencies is also easier. Simply type `poetry add <dependency>` to install a dependency in the virtual environment and update the `pyproject.toml` and `poetry.lock` files.

When accessing the virtual environment, you can also install all the dependencies listed in the `pyproject.toml` file by typing `poetry install`.

Once access to the virtual environment is no longer needed, simply type `exit` to exit the Poetry shell.

Dependencies are clearly listed in the `pyproject.toml` file and the `poetry.lock` file ensures reproducibility.

### Split the Jupyter Notebook into scripts

You will split the Jupyter Notebook in a codebase made of separate Python scripts with
well defined role. These scripts will be able to be called on the command line,
making it ideal for automation tasks.

The following table describes the files that you will create in this codebase.

| **File**                | **Description**                                   | **Input**                             | **Output**                                                    |
| ----------------------- | ------------------------------------------------- | ------------------------------------- | ------------------------------------------------------------- |
| `src/prepare.py`        | Prepare the dataset to run the ML experiment      | The dataset to prepare as an CSV file | The prepared data in `data/prepared` directory                |
| `src/train.py`          | Train the ML model                                | The prepared dataset                  | The model trained with the dataset                            |
| `src/evaluate.py`       | Evaluate the ML model using scikit-learn          | The model to evaluate                 | The results of the model evaluation in `evaluation` directory |
| `params.yaml`           | The parameters to run the ML experiment           | -                                     | -                                                             |

#### Move the parameters to its own file

Let's split the parameters to run the ML experiment with in a distinct file.

```yaml title="params.yaml"
prepare:
  seed: 20170428
  split: 0.2

train:
  seed: 20170428
  n_est: 100
  max_depth: 3
  min_split: 2
```

#### Move the preparation step to its own file

The `src/prepare.py` script will prepare the dataset.

```py title="src/prepare.py"
import json
import random
import sys
from pathlib import Path
from typing import Optional, Set

import numpy as np
import pandas as pd
import yaml
from sklearn.model_selection import train_test_split


def normalize_data(df: pd.DataFrame, columns: Set[str]) -> pd.DataFrame:
    """Normalize the data in the given columns to the range [0, 1]"""
    normalized_df = df.copy()
    for feature in columns:
        normalized_df[feature] = (df[feature] - df[feature].min()) / (
            df[feature].max() - df[feature].min()
        )
    return normalized_df


def shuffle_data(df: pd.DataFrame, seed: Optional[int] = None) -> pd.DataFrame:
    """Shuffle the data"""
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


def save_labels(df: pd.DataFrame, path: Path) -> None:
    """Save the dataframe columns to the given path"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(json.dumps(df.columns.tolist()))


def main() -> None:
    if len(sys.argv) != 3:
        print("Arguments error. Usage:\n")
        print("\tpython3 prepare.py <dataset-path> <prepared-dataset-folder>\n")
        exit(1)

    # Load parameters
    params = yaml.safe_load(open("params.yaml"))["prepare"]

    input_dataset_path = Path(sys.argv[1])
    prepared_dataset_folder = Path(sys.argv[2])
    seed = params["seed"]
    split = params["split"]

    # Set seed for reproducibility
    random.seed(seed)
    np.random.seed(seed)

    # Read data
    print("Preparing dataset...")
    df = pd.read_csv(input_dataset_path)
    df = normalize_data(df, columns=set(df.columns) - set(["Habitability"]))
    df = shuffle_data(df, seed=seed)

    # Split the dataset into features and labels
    X = df.drop(["Habitability"], axis=1).values
    y = df["Habitability"].values

    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=split, random_state=seed
    )

    print(f"Train set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")

    # Save the prepared dataset
    save_labels(df, prepared_dataset_folder / "labels.json")
    # Using np.save to save the numpy arrays as .npy files
    np.save(prepared_dataset_folder / "X_train.npy", X_train)
    np.save(prepared_dataset_folder / "X_test.npy", X_test)
    np.save(prepared_dataset_folder / "y_train.npy", y_train)
    np.save(prepared_dataset_folder / "y_test.npy", y_test)

    print(f"\nDataset saved at {prepared_dataset_folder.absolute()}")


if __name__ == "__main__":
    main()
```

#### Move the train step to its own file

The `src/train.py` script will train the ML model.

```py title="src/train.py"
import pickle
import random
import sys
from pathlib import Path

import numpy as np
import yaml
from sklearn.ensemble import RandomForestClassifier


def main() -> None:
    if len(sys.argv) != 3:
        print("Arguments error. Usage:\n")
        print("\tpython3 train.py <prepared-dataset-folder> <model-path>\n")
        exit(1)

    # Load parameters
    params = yaml.safe_load(open("params.yaml"))["train"]

    prepared_dataset_folder = Path(sys.argv[1])
    model_path = Path(sys.argv[2])
    seed = params["seed"]
    n_est = params["n_est"]
    max_depth = params["max_depth"]
    min_split = params["min_split"]

    # Set seed for reproducibility
    random.seed(seed)
    np.random.seed(seed)

    # Load data
    X_train = np.load(prepared_dataset_folder / "X_train.npy")
    y_train = np.load(prepared_dataset_folder / "y_train.npy")

    # Train the model
    print("Training model...")
    clf = RandomForestClassifier(
        n_estimators=n_est,
        max_depth=max_depth,
        min_samples_split=min_split,
        random_state=seed,
    )
    clf.fit(X_train, y_train)

    # Save the model
    model_path.parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(clf, f)

    print(f"\nModel saved at {model_path.absolute()}")


if __name__ == "__main__":
    main()
```

#### Move the evaluate step to its own file

The `src/evaluate.py` script will evaluate the ML model using DVC.

```py title="src/evaluate.py"
import json
import pickle
import sys
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier

# Matplotlib config
sns.set_style("whitegrid")


def get_model_metrics(y_test: np.ndarray, predictions: np.ndarray) -> dict[str, float]:
    """Calculate the model metrics

    accuracy: the fraction of predictions our model got right
    precision: the fraction of true positives out of all positive predictions
    avg_precision: the average precision across all possible thresholds
    recall: the fraction of true positives out of all the actual positives
    f1: the harmonic mean of precision and recall
    auc: the area under the ROC curve
    """
    return {
        "accuracy": metrics.accuracy_score(y_test, predictions),
        "precision": metrics.precision_score(y_test, predictions),
        "avg_precision": metrics.average_precision_score(y_test, predictions),
        "recall": metrics.recall_score(y_test, predictions),
        "f1": metrics.f1_score(y_test, predictions),
        "auc": metrics.roc_auc_score(y_test, predictions),
    }


def plot_feature_importances(
    model: RandomForestClassifier, columns: List[str]
) -> plt.Figure:
    """Plot the feature importances of the model"""
    # Calculate feature importances
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]

    # Rearrange feature names so they match the sorted feature importances
    names = [columns[i] for i in indices]

    # Plot feature importances
    fig = plt.figure(tight_layout=True)
    plt.bar(range(len(columns)), importances[indices])
    plt.xticks(range(len(columns)), names, rotation=90)
    plt.ylabel("Importance")
    plt.title("Feature Importance")

    return fig


def plot_roc_curve(y_test: np.ndarray, predictions_proba: np.ndarray) -> plt.Figure:
    """Plot the ROC curve"""
    fpr, tpr, _ = metrics.roc_curve(y_test, predictions_proba)

    fig = plt.figure(tight_layout=True)
    plt.plot(fpr, tpr, color="darkorange", lw=2, label="ROC curve")
    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC curve")
    plt.legend(loc="lower right")

    return fig


def plot_confusion_matrix(y_test: np.ndarray, predictions: np.ndarray) -> plt.Figure:
    """Plot the confusion matrix"""
    matrix = metrics.confusion_matrix(y_test, predictions)
    matrix = matrix.astype("float") / matrix.sum(axis=1)[:, np.newaxis]

    fig = plt.figure(figsize=(6, 5), tight_layout=True)
    sns.heatmap(matrix, annot=True, annot_kws={"size": 14}, cmap="coolwarm")
    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.title("Confusion Matrix")

    return fig


def main() -> None:
    if len(sys.argv) != 3:
        print("Arguments error. Usage:\n")
        print("\tpython3 evaluate.py <model-path> <prepared-dataset-folder>\n")
        exit(1)

    model_path = Path(sys.argv[1])
    prepared_dataset_folder = Path(sys.argv[2])
    evaluation_folder = Path("evaluation")
    plots_folder = Path("plots")

    # Create folders
    (evaluation_folder / plots_folder).mkdir(parents=True, exist_ok=True)

    # Load files
    labels = None
    with open(prepared_dataset_folder / "labels.json", "r") as f:
        labels = json.load(f)
        # Remove the "Habitability" label as this is what we are trying to predict
        labels = list(filter(lambda x: x != "Habitability", labels))

    X_test = np.load(prepared_dataset_folder / "X_test.npy")
    y_test = np.load(prepared_dataset_folder / "y_test.npy")

    # Load model
    model = None
    with open(model_path, "rb") as f:
        model = pickle.load(f)

    # Predict on test set
    y_pred = model.predict(X_test)
    preds_by_class = model.predict_proba(X_test)
    preds = preds_by_class[:, 1]

    # Log metrics
    model_metrics = get_model_metrics(y_test, y_pred)
    print("Model metrics:")
    for metric, value in model_metrics.items():
        print(f"  {metric}: {value}")

    # Plot feature importances
    fig = plot_feature_importances(model, labels)
    fig.savefig(evaluation_folder / plots_folder / "feature_importance.png")

    # Plot ROC curve with thresholds
    fig = plot_roc_curve(y_test, preds)
    fig.savefig(evaluation_folder / plots_folder / "roc_curve.png")

    # Calculate classification report
    cr = metrics.classification_report(y_test, y_pred, output_dict=True)
    cr_df = pd.DataFrame(cr).transpose()
    cr_df.to_csv(evaluation_folder / "classification_report.csv")

    # Plot confusion matrix
    fig = plot_confusion_matrix(y_test, y_pred)
    fig.savefig(evaluation_folder / plots_folder / "confusion_matrix.png")

    print(
        f"\nEvaluation metrics and plot files saved at {evaluation_folder.absolute()}"
    )


if __name__ == "__main__":
    main()
```

### Make usage of the scripts in the Jupyter Notebook

TODO: Update the notebook to use the scripts and the parameters file as well in a hybrid approach: Notebook to visualize the data and results and scripts to run the experiment.

### Check the results

Your working directory should now look like this:

TODO: Decide if we want to keep the notebook or not and the README from the notebook.

```yaml hl_lines="5-8 11-13"
.
├── data
│   ├── data.csv
│   └── README.md
├── src # (1)!
│   ├── evaluate.py
│   ├── prepare.py
│   └── train.py
├── README.md
├── notebook.ipynb
├── params.yaml # (2)!
├── poetry.lock # (3)!
└── pyproject.toml # (4)!
```

1. This, and all its sub-directory, is new.
2. This is new.
3. This is new.
4. This is new.

### Run the experiment

Awesome! You now have everything you need to run the experiment: the codebase and
the dataset are in place, the new virtual environment is set up, and you are ready to run the experiment for the first
time.

You can now follow these steps to reproduce the experiment.

```sh title="Execute the following command(s) in a terminal"
# Prepare the dataset
python3 src/prepare.py data/data.csv data/prepared

# Train the model with the train dataset and save it
python3 src/train.py data/prepared model.pkl

# Evaluate the model performances - see below note
python3 src/evaluate.py model.pkl data/prepared
```

### Check the results

Your working directory should now be similar to this:

TODO: Update the tree

```yaml hl_lines="3-8 11-16 22"
.
├── data
│   ├── prepared # (1)!
│   │   ├── X_test.npy
│   │   ├── X_train.npy
│   │   ├── labels.json
│   │   ├── y_test.npy
│   │   └── y_train.npy
│   ├── README.md
│   └── data.csv
├── evaluation # (2)!
│   ├── plots
│   │   ├── confusion_matrix.png
│   │   ├── feature_importance.png
│   │   └── roc_curve.png
│   └── classification_report.csv
├── src
│   ├── evaluate.py
│   ├── prepare.py
│   └── train.py
├── README.md
├── model.pkl # (4)!
├── notebook.ipynb
├── params.yaml
├── poetry.lock
└── pyproject.toml
```

1. This, and all its sub-directory, is new.
2. This, and all its sub-directory, is new.
3. This is new.

Here, the following should be noted:

- the `prepare.py` script created the `data/prepared` directory and divided the
dataset into a training set and a test set
- the `train.py` script created the `model.pkl` file and trained the model with
the extracted features
- the `evaluate.py` script created the `evaluation` directory and generated some
plots and metrics to evaluate the model

Take some time to get familiar with the scripts and the results.

## Summary

Congratulations! You have successfully reproduced the experiment on your machine,
this time using a modular approach that can be put into production.

In this chapter, you have:

1. Set up a standardized Python environment using Poetry
2. Adapted the content of the Jupyter Notebook into Python scripts
3. Launched the experiment locally

However, you may have identified the following areas for improvement:

- ❌ Codebase is not versioned
- ❌ Dataset still needs manual download and placement
- ❌ Steps to run the experiment were not documented
- ❌ Codebase is not easily sharable
- ❌ Dataset is not easily sharable

In the next chapters, you will enhance the workflow to fix those issues.

You can now safely continue to the next chapter.

## State of the MLOps process

- ✅ Notebook has been transformed into scripts for production
- ❌ Codebase and dataset are not versioned
- ❌ Model steps rely on verbal communication and may be undocumented
- ❌ Changes to model are not easily visualized
- ❌ Dataset requires manual download and placement
- ❌ Codebase requires manual download and setup
- ❌ Experiment may not be reproducible on other machines
- ❌ Changes to model are not thoroughly reviewed and discussed before integration
- ❌ Model may have required artifacts that are forgotten or omitted in saved/loaded state
- ❌ Model cannot be easily used from outside of the experiment context

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources
