---
title: "Step 8: Serve the model with MLEM"
---

# {% $markdoc.frontmatter.title %}

## Summary

{% callout type="note" %}
Highly inspired by the [_Get Started_ - mlem.ai](https://mlem.ai/doc/get-started), [_Saving models_ - mlem.ai](https://mlem.ai/doc/get-started/saving), [_Working with Data_ - mlem.ai](https://mlem.ai/doc/user-guide/data), [_Serving models_ - mlem.ai](https://mlem.ai/doc/user-guide/serving), [_Versioning MLEM objects with DVC_ - mlem.ai](https://mlem.ai/doc/use-cases/dvc), [_`mlem.api.save()`_ - mlem.ai](https://mlem.ai/doc/api-reference/save) and [_`mlem.api.load()`_ - mlem.ai](https://mlem.ai/doc/api-reference/load) guides.
{% /callout %}

The purpose of this step is to serve and use the model for usage outside of the experiment context with the help of MLEM. MLEM allows to do this by saving the model with metadata information that can be used to load the model for future usage.

## Instructions

{% callout type="warning" %}
This guide has been written for macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use a decent terminal ([GitBash](https://gitforwindows.org/) for instance) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

### Setup MLEM

Install MLEM.

```sh
# Install MLEM
pip install "mlem[fastapi]==0.4.1"
```

Update the `src/requirements.txt` file to include the added packages.

```
dvc==2.37.0
dvc[gs]==2.37.0
dvclive==1.0.0
pandas==1.5.1
pyaml==21.10.1
scikit-learn==1.1.3
scipy==1.9.3
matplotlib==3.6.2
mlem[fastapi]==0.4.1
```

Initialize and configure MLEM.

```sh
# Initialize MLEM
mlem init

# Set MLEM to use DVC
mlem config set core.storage.type dvc

# Add MLEM metafiles to dvcignore
echo "/**/?*.mlem" >> .dvcignore
```

### Update the experiment

Update the `src/featurization.py` file to save the `CountVectorizer` and the `TfidfTransformer` with MLEM.

```py
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

Update the `src/train.py` file to save the model with its artifacts with MLEM.

```py
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
x = matrix[:, 2:].toarray()

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
    # Remove the `.toarray()` when the following PR is merged: https://github.com/iterative/mlem/pull/538
    preprocess=lambda x: tfidf(vectorizer(x)).toarray(),
    sample_data=["This is a sample text."]
)
```

{% callout type="note" %}
Did you pay attention to the last lines? The `preprocess` lambda loads the `TfidfTransformer` with the `CountVectorizer`. These will be saved along the model for future predictions. The `sample_data` will be used to generate the right input for when the model is deployed (seen later on). MLEM will store the model's metadata in the `models/rf.mlem` file.
{% /callout %}

Update the `src/evaluate.py` file to load the model from MLEM.

```py
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
x = matrix[:, 2:].toarray()

predictions_by_class = model.predict_proba(x)
predictions = predictions_by_class[:, 1]

with Live("evaluation") as live:

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

{% callout type="note" %}
When a MLEM model is loaded with `mlem.api.load`, it will automatically load the artifacts as well. In this case, `mlem.api.load("models/rf")` will automatically load the `preprocess` lambda described earlier.
{% /callout %}

### Update the DVC pipeline

Update the DVC pipeline to include the new files.

```sh
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
  -d src/evaluate.py -d models/rf -d data/features \
  -O evaluation/plots/metrics \
  --metrics-no-cache evaluation/metrics.json \
  --plots-no-cache evaluation/plots/prc.json \
  --plots-no-cache evaluation/plots/sklearn/roc.json \
  --plots-no-cache evaluation/plots/sklearn/confusion_matrix.json \
  --plots evaluation/plots/importance.png \
  python src/evaluate.py models/rf data/features
```

Run the experiment.

```sh
# Run the experiment. DVC will automatically run all required steps
dvc repro
```

The experiment now uses MLEM to save and load the model. DVC stores the model and its metadata.

### Install additional dependencies

Install the additional MLEM dependencies to serve.

```sh
# Install MLEM
pip install "mlem[fastapi]==0.4.1"
```

Update the `src/requirements.txt` file to include the added packages.

```
dvc==2.37.0
dvc[gs]==2.37.0
dvclive==1.0.0
pandas==1.5.1
pyaml==21.10.1
scikit-learn==1.1.3
scipy==1.9.3
matplotlib==3.6.2
mlem==0.4.1
mlem[fastapi]==0.4.1
```

### Serve the model with FastAPI

Now that the model has been saved with MLEM, we will serve it with [FastAPI](https://fastapi.tiangolo.com/).

FastAPI will generate a REST API with [FastAPI](https://fastapi.tiangolo.com/) that we can use to get predictions from our model.

{% callout type="note" %}
FastAPI is only one of the available backends that MLEM can use to serve the model. Check out their official documentation for more options. 
{% /callout %}

Serve the model with FastAPI.

```sh
# Serve the model with FastAPI
mlem serve fastapi --model models/rf
```

MLEM will load the model, create the FastAPI app and start it. You can then access the auto-generated model documentation on <http://0.0.0.0:8080/docs>.

{% callout type="note" %}
Remember the `sample_data` variable discussed above? This will be used by MLEM to generate the FastAPI endpoints with the right OpenAPI/Swagger specifications.
{% /callout %}

The following endpoints have been created:

- `predict`: Get a string as the input and display the prediction of the input as true (1) if it is related to the R programming language or as false (0) if it is is not related to the R programming language.
- `predict_proba`: Get a string as the input and display the probability of the input as a array of two numbers. The first number is the probability from 0 to 1 of the input as not related to the R programming language. The second number is the probability from 0 to 1 of the input as related to the R programming language.

You can try out predictions by inputing some sentences to the model through the REST API!

Here are some request bodies you can use as examples.

{% callout type="warning" %}
Please be aware the model is a very simple model. Some inputs may be incorrectly predicted.
{% /callout %}

**Request body**

```json
{
  "data": [
    "Is this related to the R programming language?"
  ]
}
```

**Prediction output**

This output means that the input is related to the R programming language.

```json
[
  1
]
```

**Probablities output**

This output means a 55% probability that the input is related to the R programming language.

```json
[
  [
    0.45,
    0.55
  ]
]
```

**Request body**

```json
{
  "data": [
    "This should not be related as I talk about dogs"
  ]
}
```

**Prediction output**

This output means that the input is not related to the R programming language.

```json
[
  0
]
```

**Probablities output**

This output means a 0% probability that the input is related to the R programming language.

```json
[
  [
    1,
    0
  ]
]
```

**Request body**

```json
{
  "data": [
    "My favorite programming language is Python!"
  ]
}
```

**Prediction output**

This output means that the input is not related to the R programming language.

```json
[
  0
]
```

**Probablities output**

This output means a 33% probability that the input is related to the R programming language.

```json
[
  [
    0.6616666666666666,
    0.33833333333333326
  ]
]
```

### Push the changes to DVC and Git

Push the changes to DVC and Git.

```sh
# Upload the experiment data and cache to the remote bucket
dvc push

# Add all the files
git add .

# Commit the changes
git commit -m "MLEM can save, load and serve the model"

# Push the changes
git push
```

Congrats! You now have a model served over a REST API! You could serve this model from anywhere. Additional services could submit predictions to your model. The usage of FastAPI creates endpoints that are automatically documented to interact with the model. Check the next step of this guide concluding your journey for the next things you could do with your model.

## Check the results

Want to see what the result of this step should look like? Have a look at the Git repository directory here: [step-8-serve-the-model-with-mlem](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/step-8-serve-the-model-with-mlem).

## State of the MLOps process

- ✅ The codebase can be shared among the developers. The codebase can be improved collaboratively;
- ✅ The dataset can be shared among the developers and is placed in the right directory in order to run the experiment;
- ✅ The steps used to create the model are documented and can be re-executed;
- ✅ The experiment can be executed on a clean machine with the help of the CI/CD pipeline;
- ✅ The changes done to a model can be visualized with parameters, metrics and plots to identify differences between iterations with the help of the CI/CD pipeline;
- ✅ The model can be saved and loaded with all have required artifacts for future usage. The model can be served outside of the experiment context.

## Next & Previous steps

- **Previous**: [Step 7: Track model evolutions in the CI/CD pipeline with CML](/the-guide/step-7-track-model-evolutions-in-the-cicd-pipeline-with-cml)
- **Next**: [Conclusion](/the-guide/conclusion)
