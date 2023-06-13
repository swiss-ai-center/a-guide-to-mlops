# Chapter 10: Save and load the model with MLEM

## Introduction

The purpose of this chapter is to serve and use the model for usage outside of
the experiment context with the help of [MLEM](../../tools). MLEM allows to do this by saving
the model with metadata information that can be used to load the model for
future usage.

In this chapter, you will learn how to:

1. Install MLEM
2. Initialize and configure MLEM
3. Update and run the experiment to use MLEM to save and load the model

## Steps

### Install MLEM

Add the `mlem[fastapi]` package to install MLEM with FastAPI support.

```sh title="Execute the following command(s) in a terminal"
poetry add "mlem[fastapi]==0.4.3"
```

Check the differences with Git to validate the changes.

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff pyproject.toml
```

The output should be similar to this.

```diff
diff --git a/pyproject.toml b/pyproject.toml
index ff11768..f28f832 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -14,6 +14,7 @@ scikit-learn = "1.1.3"
scipy = "1.10.1"
matplotlib = "3.6.2"
dvc = {version = "2.37.0", extras = ["gs"]}
+mlem = {version = "0.4.3", extras = ["fastapi"]}

[build-system]
requires = ["poetry-core"]
```

### Initialize and configure MLEM.

```sh title="Execute the following command(s) in a terminal"
# Initialize MLEM
mlem init

# Set MLEM to use DVC
mlem config set core.storage.type dvc

# Add MLEM metafiles to dvcignore
echo "/**/?*.mlem" >> .dvcignore
```

The effect of the `mlem init` command is to create a `.mlem.yaml` file in the
working directory. This file contains the configuration of MLEM.

### Update the experiment

#### Update `src/featurization.py`


Update the `src/featurization.py` file to save the `CountVectorizer` and the
`TfidfTransformer` with MLEM.

```py title="src/featurization.py" hl_lines="11 74-75"
import os
import pickle
import sys

import numpy as np
import pandas as pd
import scipy.sparse as sparse
import yaml
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

from mlem.api import save

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

save(bag_of_words.transform, "data/features/vectorizer")
save(tfidf.transform, "data/features/tfidf")

save_matrix(df_train, train_words_tfidf_matrix, feature_names, train_output)

# Generate test feature matrix
df_test = get_df(test_input)
test_words = np.array(df_test.text.str.lower().values.astype("U"))
test_words_binary_matrix = bag_of_words.transform(test_words)
test_words_tfidf_matrix = tfidf.transform(test_words_binary_matrix)

save_matrix(df_test, test_words_tfidf_matrix, feature_names, test_output)
```

Check the differences with Git to better understand the changes.

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff src/featurization.py
```

The output should be similar to this.

```diff
diff --git a/src/featurization.py b/src/featurization.py
index 4afb10e..a61d371 100644
--- a/src/featurization.py
+++ b/src/featurization.py
@@ -8,6 +8,8 @@ import scipy.sparse as sparse
import yaml
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

+from mlem.api import save
+
params = yaml.safe_load(open("params.yaml"))["featurize"]

np.set_printoptions(suppress=True)
@@ -69,6 +71,9 @@ tfidf = TfidfTransformer(smooth_idf=False)
tfidf.fit(train_words_binary_matrix)
train_words_tfidf_matrix = tfidf.transform(train_words_binary_matrix)

+save(bag_of_words.transform, "data/features/vectorizer")
+save(tfidf.transform, "data/features/tfidf")
+
save_matrix(df_train, train_words_tfidf_matrix, feature_names, train_output)

# Generate test feature matrix
```

#### Update `src/train.py`

Update the `src/train.py` file to save the model with its artifacts with MLEM.

```py title="src/train.py" hl_lines="9 40-48"
import os
import pickle
import sys

import numpy as np
import yaml
from sklearn.ensemble import RandomForestClassifier

from mlem.api import load, save

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

tfidf = load("data/features/tfidf")
vectorizer = load("data/features/vectorizer")

save(
    clf,
    output,
    preprocess=lambda x: tfidf(vectorizer(x)),
    sample_data=["This is a sample text."]
)
```

!!! note

    Did you pay attention to the last lines? The
    `preprocess` lambda loads the `TfidfTransformer` with the `CountVectorizer`.
    These will be saved along the model for future predictions. The `sample_data`
    will be used to generate the right input for when the model is deployed (seen
    later on). MLEM will store the model's metadata in the `models/rf.mlem` file.

Check the differences with Git to better understand the changes.

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff src/train.py
```

The output should be similar to this.

```diff
diff --git a/src/train.py b/src/train.py
index 483fb50..fd1b6d9 100644
--- a/src/train.py
+++ b/src/train.py
@@ -6,6 +6,8 @@ import numpy as np
import yaml
from sklearn.ensemble import RandomForestClassifier

+from mlem.api import load, save
+
params = yaml.safe_load(open("params.yaml"))["train"]

if len(sys.argv) != 3:
@@ -35,5 +37,12 @@ clf = RandomForestClassifier(

clf.fit(x, labels)

-with open(output, "wb") as fd:
-    pickle.dump(clf, fd)
+tfidf = load("data/features/tfidf")
+vectorizer = load("data/features/vectorizer")
+
+save(
+    clf,
+    output,
+    preprocess=lambda x: tfidf(vectorizer(x)),
+    sample_data=["This is a sample text."]
+)
```

#### Update `src/evaluate.py`

Update the `src/evaluate.py` file to load the model from MLEM.

```py title="src/evaluate.py" hl_lines="13 23"
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

from mlem.api import load

if len(sys.argv) != 3:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython evaluate.py model features\n")
    sys.exit(1)

model_file = sys.argv[1]
matrix_file = os.path.join(sys.argv[2], "test.pkl")

model = load(model_file)

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

Check the differences with Git to better understand the changes.

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff src/evaluate.py
```

The output should be similar to this.

```diff
diff --git a/src/evaluate.py b/src/evaluate.py
index 89d616f..ba21f0e 100644
--- a/src/evaluate.py
+++ b/src/evaluate.py
@@ -10,6 +10,7 @@ from sklearn import tree
from dvclive import Live
from matplotlib import pyplot as plt

+from mlem.api import load

if len(sys.argv) != 3:
sys.stderr.write("Arguments error. Usage:\n")
@@ -19,8 +20,7 @@ if len(sys.argv) != 3:
model_file = sys.argv[1]
matrix_file = os.path.join(sys.argv[2], "test.pkl")

-with open(model_file, "rb") as fd:
-    model = pickle.load(fd)
+model = load(model_file)

with open(matrix_file, "rb") as fd:
matrix, feature_names = pickle.load(fd)
```

!!! info

    When a MLEM model is loaded with `mlem.api.load`, it
    will automatically load the artifacts as well. In this case,
    `mlem.api.load("models/rf")` will automatically load the `preprocess` lambda
    described earlier.

### Update the DVC pipeline


Update the DVC pipeline to reflect the changes in the stages.

```sh title="Execute the following command(s) in a terminal"
# Update the featurization stage
dvc stage add --force \
-n featurize \
-p featurize.max_features,featurize.ngrams \
-d src/featurization.py -d data/prepared \
-o data/features/test.pkl -o data/features/train.pkl -o data/features/vectorizer -o data/features/tfidf \
python src/featurization.py data/prepared data/features

# Update the train stage
dvc stage add --force \
-n train \
-p train.seed,train.n_est,train.min_split \
-d src/train.py -d data/features \
-o models/rf \
python src/train.py data/features models/rf

# Update the evaluate stage
dvc stage add --force \
-n evaluate \
-d src/evaluate.py -d models/rf \
-o evaluation/plots/metrics \
-o evaluation/report.html \
--metrics evaluation/metrics.json \
--plots evaluation/plots/prc.json \
--plots evaluation/plots/sklearn/roc.json \
--plots evaluation/plots/sklearn/confusion_matrix.json \
--plots evaluation/plots/importance.png \
python src/evaluate.py models/rf data/features

# Set the axes for the `precision_recall_curve`
dvc plots modify evaluation/plots/prc.json -x recall -y precision

# Set the axes for the `roc_curve`
dvc plots modify evaluation/plots/sklearn/roc.json -x fpr -y tpr

# Set the axes for the `confusion_matrix`
dvc plots modify evaluation/plots/sklearn/confusion_matrix.json -x actual -y predicted -t confusion
```

Check the differences with Git to better understand the changes.

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff dvc.yaml
```

The output should be similar to this.

```diff
diff --git a/dvc.yaml b/dvc.yaml
index fdb2bc3..3f2eaeb 100644
--- a/dvc.yaml
+++ b/dvc.yaml
@@ -19,9 +19,11 @@ stages:
- featurize.ngrams
outs:
- data/features/test.pkl
+    - data/features/tfidf
- data/features/train.pkl
+    - data/features/vectorizer
train:
-    cmd: python src/train.py data/features model.pkl
+    cmd: python src/train.py data/features models/rf
deps:
- data/features
- src/train.py
@@ -30,11 +32,11 @@ stages:
- train.n_est
- train.seed
outs:
-    - model.pkl
+    - models/rf
evaluate:
-    cmd: python src/evaluate.py model.pkl data/features
+    cmd: python src/evaluate.py models/rf data/features
deps:
-    - model.pkl
+    - models/rf
- src/evaluate.py
outs:
- evaluation/plots/metrics
```

### Run the experiment

```sh title="Execute the following command(s) in a terminal"
# Run the experiment. DVC will automatically run all required stages
dvc repro
```

The experiment now uses MLEM to save and load the model. DVC stores the model
and its metadata.

### Commit the changes to DVC and Git

Commit the changes to DVC and Git.

```sh title="Execute the following command(s) in a terminal"
# Upload the experiment data and cache to the remote bucket
dvc push

# Commit the changes
git commit -m "MLEM can save, load and serve the model"
```

## Summary

In this chapter, you have successfully:

1. Installed MLEM
2. Initialized and configuring MLEM
3. Updated and ran the experiment to use MLEM to save and load the model

You did fix some of the previous issues:

- ✅ Model can be saved and loaded with all required artifacts for future usage

You can now safely continue to the next chapter.

## State of the MLOps process

- ✅ Notebook has been transformed into scripts for production
- ✅ Codebase and dataset are versioned
- ✅ Steps used to create the model are documented and can be re-executed
- ✅ Changes done to a model can be visualized with parameters, metrics and plots to identify
differences between iterations
- ✅ Dataset can be shared among the developers and is placed in the right
directory in order to run the experiment
- ✅ Codebase can be shared and improved by multiple developers
- ✅ Experiment can be executed on a clean machine with the help of a CI/CD
pipeline
- ✅ Changes to model can be thoroughly reviewed and discussed before integrating them into the codebase
- ✅ Model can be saved and loaded with all required artifacts for future usage
- ❌ Model cannot be easily used from outside of the experiment context

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by:

* [_Get Started_ - mlem.ai](https://mlem.ai/doc/get-started)
* [_Saving models_ - mlem.ai](https://mlem.ai/doc/get-started/saving)
* [_Working with Data_ - mlem.ai](https://mlem.ai/doc/user-guide/data)
* [_`mlem.api.save()`_ - mlem.ai](https://mlem.ai/doc/api-reference/save)
* [_`mlem.api.load()`_ - mlem.ai](https://mlem.ai/doc/api-reference/load)
