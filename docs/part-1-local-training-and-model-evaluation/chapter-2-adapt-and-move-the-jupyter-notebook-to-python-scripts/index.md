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

In this chapter, you will learn how to:

1. Adapt the content of the Jupyter notebook into Python scripts
4. Set up a standardized Python environment using [poetry](https://python-poetry.org/)
5. Launch the experiment locally

Let's get started!

## Steps

### Split the notebook into scripts

You will split the notebook in a codebase made of separate Python scripts with
well defined role. These scripts will be able to be called on the command line,
making it ideal for automation tasks.

In addition, you will use [poetry](https://python-poetry.org/) to provide a
convenient and efficient approach to setting up Python environments, making the
process easier, more standardized and reproducible across different machines.

The following table describes the files that you will create in this codebase.

| **File**                | **Description**                                   | **Input**                             | **Output**                                                    |
| ----------------------- | ------------------------------------------------- | ------------------------------------- | ------------------------------------------------------------- |
| `src/prepare.py`        | Prepare the dataset to run the ML experiment      | The dataset to prepare as an XML file | The prepared data in `data/prepared` directory                |
| `src/featurization.py`  | Extract the features from the dataset             | The prepared dataset                  | The extracted features in `data/features` directory           |
| `src/train.py`          | Train the ML model                                | The extracted features                | The model trained with the dataset                            |
| `src/evaluate.py`       | Evaluate the ML model using DVC                   | The model to evaluate                 | The results of the model evaluation in `evaluation` directory |
| `params.yaml`           | The parameters to run the ML experiment           | -                                     | -                                                             |
| `poetry.lock`           | The Poetry lockfile of all dependencies           | -                                     | -                                                             |
| `pyproject.toml`        | The Poetry dependencies to run the ML experiment  | -                                     | -                                                             |

!!! info

    The `params.yaml` is the default file used by DVC. You can find the reference here: <https://dvc.org/doc/command-reference/params>.


#### Parameters section

Let's split the parameters to run the ML experiment with in a distinct file.

```yaml title="params.yaml"
prepare:
    split: 0.20
    seed: 20170428

featurize:
    max_features: 100
    ngrams: 1

train:
    seed: 20170428
    n_est: 50
    min_split: 2
```

#### Prepare section

The `src/prepare.py` script will prepare the dataset.

```py title="src/prepare.py"

import io
import os
import random
import re
import sys
import xml.etree.ElementTree

import yaml

params = yaml.safe_load(open("params.yaml"))["prepare"]

if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython prepare.py data-file\n")
    sys.exit(1)

# Test data set split ratio
split = params["split"]
random.seed(params["seed"])

input = sys.argv[1]
output_train = os.path.join("data", "prepared", "train.tsv")
output_test = os.path.join("data", "prepared", "test.tsv")


def process_posts(fd_in, fd_out_train, fd_out_test, target_tag):
    num = 1
    for line in fd_in:
        try:
            fd_out = fd_out_train if random.random() > split else fd_out_test
            attr = xml.etree.ElementTree.fromstring(line).attrib

            pid = attr.get("Id", "")
            label = 1 if target_tag in attr.get("Tags", "") else 0
            title = re.sub(r"\s+", " ", attr.get("Title", "")).strip()
            body = re.sub(r"\s+", " ", attr.get("Body", "")).strip()
            text = title + " " + body

            fd_out.write("{}\t{}\t{}\n".format(pid, label, text))

            num += 1
        except Exception as ex:
            sys.stderr.write(f"Skipping the broken line {num}: {ex}\n")


os.makedirs(os.path.join("data", "prepared"), exist_ok=True)

with io.open(input, encoding="utf8") as fd_in:
    with io.open(output_train, "w", encoding="utf8") as fd_out_train:
        with io.open(output_test, "w", encoding="utf8") as fd_out_test:
            process_posts(fd_in, fd_out_train, fd_out_test, "<r>")
```

#### Featurize section

The `src/featurization.py` script will extract the features from the dataset.

```py title="src/featurization.py"
import os
import pickle
import sys

import numpy as np
import pandas as pd
import scipy.sparse as sparse
import yaml
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

params = yaml.safe_load(open("params.yaml"))["featurize"]

np.set_printoptions(suppress=True)

if len(sys.argv) != 3 and len(sys.argv) != 5:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython featurization.py data-dir-path features-dir-path\n")
    sys.exit(1)

train_input = os.path.join(sys.argv[1], "train.tsv")
test_input = os.path.join(sys.argv[1], "test.tsv")
train_output = os.path.join(sys.argv[2], "train.pkl")
test_output = os.path.join(sys.argv[2], "test.pkl")

max_features = params["max_features"]
ngrams = params["ngrams"]


def get_df(data):
    df = pd.read_csv(
        data,
        encoding="utf-8",
        header=None,
        delimiter="\t",
        names=["id", "label", "text"],
    )
    sys.stderr.write(f"The input data frame {data} size is {df.shape}\n")
    return df


def save_matrix(df, matrix, names, output):
    id_matrix = sparse.csr_matrix(df.id.astype(np.int64)).T
    label_matrix = sparse.csr_matrix(df.label.astype(np.int64)).T

    result = sparse.hstack([id_matrix, label_matrix, matrix], format="csr")

    msg = "The output matrix {} size is {} and data type is {}\n"
    sys.stderr.write(msg.format(output, result.shape, result.dtype))

    with open(output, "wb") as fd:
        pickle.dump((result, names), fd)
    pass


os.makedirs(sys.argv[2], exist_ok=True)

# Generate train feature matrix
df_train = get_df(train_input)
train_words = np.array(df_train.text.str.lower().values.astype("U"))

bag_of_words = CountVectorizer(
    stop_words="english", max_features=max_features, ngram_range=(1, ngrams)
)

bag_of_words.fit(train_words)
train_words_binary_matrix = bag_of_words.transform(train_words)
feature_names = bag_of_words.get_feature_names_out()
tfidf = TfidfTransformer(smooth_idf=False)
tfidf.fit(train_words_binary_matrix)
train_words_tfidf_matrix = tfidf.transform(train_words_binary_matrix)

save_matrix(df_train, train_words_tfidf_matrix, feature_names, train_output)

# Generate test feature matrix
df_test = get_df(test_input)
test_words = np.array(df_test.text.str.lower().values.astype("U"))
test_words_binary_matrix = bag_of_words.transform(test_words)
test_words_tfidf_matrix = tfidf.transform(test_words_binary_matrix)

save_matrix(df_test, test_words_tfidf_matrix, feature_names, test_output)
```

#### Train section

The `src/train.py` script will train the ML model.

```py title="src/train.py"
import os
import pickle
import sys

import numpy as np
import yaml
from sklearn.ensemble import RandomForestClassifier

params = yaml.safe_load(open("params.yaml"))["train"]

if len(sys.argv) != 3:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython train.py features model\n")
    sys.exit(1)

input = sys.argv[1]
output = sys.argv[2]
seed = params["seed"]
n_est = params["n_est"]
min_split = params["min_split"]

with open(os.path.join(input, "train.pkl"), "rb") as fd:
    matrix, _ = pickle.load(fd)

labels = np.squeeze(matrix[:, 1].toarray())
x = matrix[:, 2:]

sys.stderr.write("Input matrix size {}\n".format(matrix.shape))
sys.stderr.write("X matrix size {}\n".format(x.shape))
sys.stderr.write("Y matrix size {}\n".format(labels.shape))

clf = RandomForestClassifier(
    n_estimators=n_est, min_samples_split=min_split, n_jobs=2, random_state=seed
)

clf.fit(x, labels)

with open(output, "wb") as fd:
    pickle.dump(clf, fd)
```

#### Evaluate section

The `src/evaluate.py` script will evaluate the ML model using DVC.

```py title="src/evaluate.py"
import json
import math
import os
import pickle
import sys

import pandas as pd
from sklearn import metrics
from sklearn import tree
from dvclive import Live
from matplotlib import pyplot as plt


if len(sys.argv) != 3:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython evaluate.py model features\n")
    sys.exit(1)

model_file = sys.argv[1]
matrix_file = os.path.join(sys.argv[2], "test.pkl")

with open(model_file, "rb") as fd:
    model = pickle.load(fd)

with open(matrix_file, "rb") as fd:
    matrix, feature_names = pickle.load(fd)

labels = matrix[:, 1].toarray().astype(int)
x = matrix[:, 2:]

predictions_by_class = model.predict_proba(x)
predictions = predictions_by_class[:, 1]

with Live("evaluation", report="html") as live:

    # Use dvclive to log a few simple metrics...
    avg_prec = metrics.average_precision_score(labels, predictions)
    roc_auc = metrics.roc_auc_score(labels, predictions)
    live.log_metric("avg_prec", avg_prec)
    live.log_metric("roc_auc", roc_auc)

    # ... and plots...
    live.log_sklearn_plot("roc", labels, predictions)

    # ... but actually it can be done with dumping data points into a file:
    # ROC has a drop_intermediate arg that reduces the number of points.
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html#sklearn.metrics.roc_curve.
    # PRC lacks this arg, so we manually reduce to 1000 points as a rough estimate.
    precision, recall, prc_thresholds = metrics.precision_recall_curve(labels,predictions)
    nth_point = math.ceil(len(prc_thresholds) / 1000)
    prc_points = list(zip(precision, recall, prc_thresholds))[::nth_point]
    prc_file = os.path.join("evaluation", "plots", "prc.json")
    with open(prc_file, "w") as fd:
        json.dump(
        {
            "prc": [
            {"precision": p, "recall": r, "threshold": t}
            for p, r, t in prc_points
            ]
        },
        fd,
        indent=4,
        )


    # ... confusion matrix plot
    live.log_sklearn_plot("confusion_matrix",
        labels.squeeze(),
        predictions_by_class.argmax(-1)
    )

    # ... and finally, we can dump an image, it's also supported:
    fig, axes = plt.subplots(dpi=100)
    fig.subplots_adjust(bottom=0.2, top=0.95)
    importances = model.feature_importances_
    forest_importances = pd.Series(importances, index=feature_names).nlargest(n=30)
    axes.set_ylabel("Mean decrease in impurity")
    forest_importances.plot.bar(ax=axes)
    fig.savefig(os.path.join("evaluation", "plots", "importance.png"))
```

### Set up standardized environment

You will now establish a convenient and efficient method for setting up Python
environments with all the required dependencies using [poetry](https://python-poetry.org/).
This approach aims to simplify the installation process, standardize the
environment across various machines, and ensure reproducibility within a
streamlined development workflow.

!!! question

    **Why Poetry?**

    Poetry is a tool to manage Python dependencies. It is a more robust and
    user-friendly alternative to `pip`. It is also more suitable for
    reproducibility and collaboration by creating a lock file that can be used
    to recreate the exact same environment.

    For example, freezing the version of a dependency in a `requirements.txt` file
    is not enough to ensure reproducibility. The `requirements.txt` file only
    specifies the version of the dependency at the time of installation. If dependencies
    of the dependency are updated, the version of the dependency might change
    without you knowing it. This is why Poetry creates a lock file that contains
    the exact version of all the dependencies and their dependencies.

Create the `pyproject.toml` file at the root of the directory.

```toml title="pyproject.toml"
[tool.poetry]
name = "a-guide-to-mlops"
version = "0.1.0"
description = "CSIA-PME - A Guide to MLOps"
authors = []
packages = [{include = "src"}]

[tool.poetry.dependencies]
python = ">=3.8,<3.12"
dvclive = "1.0.0"
pandas = "1.5.1"
pyaml = "21.10.1"
scikit-learn = "1.1.3"
scipy = "1.10.1"
matplotlib = "3.6.2"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

Compute necessary dependencies and create the `poetry.lock` file that define the
dependency requirements.

```sh title="Execute the following command(s) in a terminal"
# Lock the installation requirements.
poetry lock
```

### Check the results

Your working directory should now look like this:

```yaml hl_lines="2-10"
.
├── data
│   ├── data.xml
│   └── README.md
├── notebook.md
├── src # (1)!
│   ├── evaluate.py
│   ├── featurization.py
│   ├── prepare.py
│   └── train.py
├── params.yaml # (2)!
├── poetry.lock # (3)!
└── pyproject.toml # (4)!
```

1. This, and all its sub-directory, is new.
2. This is new.
3. This is new.
4. This is new.
5. This is new.

### Run the experiment

Awesome! You now have everything you need to run the experiment: the codebase and
the dataset are in place; and you are ready to run the experiment for the first
time.

Create the virtual environment and install necessary dependencies in your
working directory using these commands.

```sh title="Execute the following command(s) in a terminal"
# Install the dependencies in a virtual environment
poetry install

# Activate the virtual environment
poetry shell
```

You can now follow these steps to reproduce the experiment.

```sh title="Execute the following command(s) in a terminal"
# Prepare the dataset
python src/prepare.py data/data.xml

# Perform feature extraction
python src/featurization.py data/prepared data/features

# Train the model with the extracted features and save it
python src/train.py data/features model.pkl

# Evaluate the model performances - see below note
python src/evaluate.py model.pkl data/features
```

!!! info

    The `evaluate.py` Python script might display a
    warning regarding DVC. You can safely ignore it for now.

### Check the results


Your working directory should now be similar to this:

```yaml hl_lines="3-8 11-22 29"
.
├── data
│   ├── features # (1)!
│   │   ├── test.pkl
│   │   └── train.pkl
│   ├── prepared # (2)!
│   │   ├── test.tsv
│   │   └── train.tsv
│   ├── README.md
│   └── data.xml
├── evaluation # (3)!
│   ├── plots
│   │   ├── metrics
│   │   │   ├── avg_prec.tsv
│   │   │   └── roc_auc.tsv
│   │   ├── sklearn
│   │   │   ├── confusion_matrix.json
│   │   │   └── roc.json
│   │   ├── importance.png
│   │   └── prc.json
│   ├── metrics.json
│   └── report.html
├── src
│   ├── evaluate.py
│   ├── featurization.py
│   ├── prepare.py
│   └── train.py
├── README.md
├── model.pkl # (4)!
├── params.yaml
├── poetry.lock
└── pyproject.toml
```

1. This, and all its sub-directory, is new.
2. This, and all its sub-directory, is new.
3. This, and all its sub-directory, is new.
4. This is new.

Here, the following should be noted:

- the `prepare.py` script created the `data/prepared` directory and divided the
dataset into a training set and a test set
- the `featurization.py` script created the `data/features` directory and
extracted the features from the training and test sets
- the `train.py` script created the `model.pkl` file and trained the model with
the extracted features
- the `evaluate.py` script created the `evaluation` directory and generated some
plots and metrics to evaluate the model

Take some time to get familiar with the scripts and the results.

Running the `evaluate.py` also generates a report at `evaluation/report.html` with the metrics and plots.

Here is a preview of the report:

![Evaluation Report](../../assets/images/evaluation_report.png){ loading=lazy }

## Summary

Congratulations! You have successfully reproduced the experiment on your machine,
this time using a modular approach that can be put into production.

In this chapter, you have:

1. Adapted the content of the Jupyter notebook into Python scripts
2. Set up a standardized Python environment using poetry
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

!!! bug

`[TBD]`
