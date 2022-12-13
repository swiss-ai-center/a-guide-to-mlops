---
title: "Step 4: Reproduce the experiment with DVC"
---

# {% $markdoc.frontmatter.title %}

## Summary

{% callout type="note" %}
Highly inspired by the [_Get Started: Data Pipelines_ - dvc.org](https://dvc.org/doc/start/data-management/pipelines) guide.
{% /callout %}

The purpose of this step is to store the commands to execute the simple ML experiment in DVC to easily reproduce the experiment in its entirety.

As a reminder, the steps to run the experiment is as follow:

```sh
# Prepare the dataset
python src/prepare.py data/data.xml

# Perform feature extraction
python src/featurization.py data/prepared data/features

# Train the model with the extracted features and save it
python src/train.py data/features model.pkl

# Evaluate the model performances
python src/evaluate.py model.pkl data/features
```

## Instructions

Update the `.gitignore` file. DVC will automatically add new lines at the end of the file.

```sh
## Custom experiment

# The models evaluations
evaluation/importance.png

## Python

# Environments
.venv

# Byte-compiled / optimized / DLL files
__pycache__/

## DVC
/model.pkl
```

Store the command to prepare the dataset in DVC.

```sh
dvc stage add -n prepare \
  -p prepare.seed,prepare.split \
  -d src/prepare.py -d data/data.xml \
  -o data/prepared \
  python src/prepare.py data/data.xml
```

This command adds a new stage called _prepare_ that has the `src/prepare.py` and `data/data.xml` files as a dependency.

If any of these files change, DVC will run the command `python src/prepare.py data/data.xml` when using `dvc repro`.

The output of this command is `data/prepared`.

{% callout type="note" %}
The parameters `prepare.seed` and `prepare.split` will be discussed later.
{% /callout %}

Store the command to perform the features extraction in DVC.

```sh
dvc stage add -n featurize \
  -p featurize.max_features,featurize.ngrams \
  -d src/featurization.py -d data/prepared \
  -o data/features \
  python src/featurization.py data/prepared data/features
```

This command adds a new stage called _featurize_ that has the `src/featurization.py` and `data/prepared` files as a dependency.

If any of these files change, DVC will run the command `python src/featurization.py data/prepared data/features` when using `dvc repro`.

The output of this command is `data/features`.

{% callout type="note" %}
The parameters `featurize.max_features` and `featurize.ngrams` will be discussed later.
{% /callout %}

Store the command to train the model in DVC.

```sh
dvc stage add -n train \
  -p train.seed,train.n_est,train.min_split \
  -d src/train.py -d data/features \
  -o model.pkl \
  python src/train.py data/features model.pkl
```

This command adds a new stage called _train_ that has the `src/train.py` and `data/features` files as a dependency.

If any of these files change, DVC will run the command `python src/train.py data/features model.pkl` when using `dvc repro`.

The output of this command is `model.pkl`.

{% callout type="note" %}
The parameters `train.seed`, `train.n_est` and `train.min_split` will be discussed later.
{% /callout %}

Store the command to evaluate the model in DVC.

```sh
dvc stage add -n evaluate \
  -d src/evaluate.py -d model.pkl -d data/features \
  --metrics-no-cache evaluation/plots/metrics/avg_prec.tsv \
  --metrics-no-cache evaluation/plots/metrics/roc_auc.tsv \
  --plots-no-cache evaluation/plots/sklearn/confusion_matrix.json \
  --plots-no-cache evaluation/plots/sklearn/precision_recall.json \
  --plots-no-cache evaluation/plots/sklearn/roc.json \
  python src/evaluate.py model.pkl data/features
```

This command adds a new stage called _evaluate_ that has the `src/evaluate.py`, `model.pkl` and `data/features` files as a dependency.

If any of these files change, DVC will run the command `python src/evaluate.py model.pkl data/features` when using `dvc repro`.

This command writes the model's average precision to `evaluation/plots/metrics/avg_prec.tsv` and ROC-AUC to `evaluation/plots/metrics/roc_auc.tsv` that are marked as metrics. It writes the `confusion_matrix` to `evaluation/plots/sklearn/confusion_matrix.json`, the `precision_recall_curve` to `evaluation/plots/sklearn/precision_recall.json` and the `roc_curve` to `evaluation/plots/sklearn/roc.json` that will be used to create plots.

Execute the pipeline.

```sh
# Execute only the required pipeline steps (if files or parameters changed)
dvc repro

# Force the execution of the entire pipeline
dvc repro --force
```

Visualize the pipeline.

```sh
# Display the Directed Acyclic Graph of the pipeline
dvc dag
```

```
    +-------------------+
    | data/data.xml.dvc |
    +-------------------+
              *
              *
              *
         +---------+
         | prepare |
         +---------+
              *
              *
              *
        +-----------+
        | featurize |
        +-----------+
         **        **
       **            *
      *               **
+-------+               *
| train |             **
+-------+            *
         **        **
           **    **
             *  *
        +----------+
        | evaluate |
        +----------+
```

Push the changes to DVC and git.

```sh
# Upload the experiment data and cache to the remote bucket
dvc push

# Add all the files
git add .

# Commit the changes
git commit -m "My ML experiment commands are saved with DVC"

# Push the changes
git push
```

The parameters discussed before, defined in the `params.yaml` file can be edited to re-run the experiment. DVC will track all these parameters and store the outputs' results in its cache so it will not re-run the experiment if not needed.

Congrats! You now have a defined and common way to reproduce the pipeline to create a model. The steps will be run only if files or parameters change.

{% callout type="note" %}
Want to see what the result of this step should look like? Have a look at the Git repository directory here: [step-4-reproduce-the-experiment-with-dvc](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/step-4-reproduce-the-experiment-with-dvc)
{% /callout %}

## State of the MLOps process

- The codebase can be shared among the developers. The codebase can be improved collaboratively.
- The dataset can be shared among the developers and is placed in the right directory in order to run the experiment.
- The steps used to create the model are documented and can be re-executed.

## Next & Previous steps

- **Previous**: [Step 3: Share your ML experiment data with DVC](/the-guide/step-3-share-your-ml-experiment-data-with-dvc)
- **Next**: [Step 5: Track model evolutions with DVC](/the-guide/step-5-track-model-evolutions-with-dvc)
