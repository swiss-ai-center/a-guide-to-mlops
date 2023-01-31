---
title: "Chapter 4: Reproduce the experiment with DVC"
---

# {% $markdoc.frontmatter.title %}

## Introduction

A key component of DVC is the concept of "stages". Stages are essentially commands that produce a result, whether that be a file or directory. The beauty of DVC is that these stages are executed only when the dependencies they rely on have changed. This way, we don't have to waste time re-running unnecessary steps.

By using DVC stages to create a pipeline, we can execute all of our experiment's steps in a streamlined manner by simply running dvc repro. In this way, DVC helps us improve our team's efficiency and makes it easier for us to keep track of our experiment's progress.

In this chapter, you'll cover:

- Removing custom rules from the gitignore file
- Setting up four DVC pipeline stages
  - `prepare`
  - `featurize`
  - `train`
  - `evaluate`
- Visualizing the pipeline
- Executing the pipeline
- Pushing the changes to DVC and Git

As a reminder, the current steps to run the experiment are as follow:

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

## Steps

{% callout type="warning" %}
This guide has been written with macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use [GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

### Remove custom rules from the gitignore file

As seen in the previous chapter, DVC can update gitignore files.

As you will define the entire experiment pipeline with DVC, you can safely remove all the custom rules from the main `.gitignore` file so DVC can manage them for you. At the end of this chapter, DVC should have updated all the gitignore files if necessary.

Update the `.gitignore` file to keep Python elements with the following content. The rest will be added by DVC.

```sh
## Python

# Environments
.venv

# Byte-compiled / optimized / DLL files
__pycache__/

## DVC

# DVC will add new files after this line
```

Check the differences with Git to validate the changes.

```sh
# Show the differences with Git
git diff .gitignore
```

The output should be similar to this.

```diff
diff --git a/.gitignore b/.gitignore
index 6755ab0..be446de 100644
--- a/.gitignore
+++ b/.gitignore
@@ -1,10 +1,3 @@
-# Data used to train the models
-data/features
-data/prepared
-
-# The models
-*.pkl
-
 ## Python
 
 # Environments
@@ -12,3 +5,7 @@ data/prepared
 
 # Byte-compiled / optimized / DLL files
 __pycache__/
+
+## DVC
+
+# DVC will add new files after this line
```

### Setup the DVC pipeline stages

Each step of the experiment will be stored as a DVC stage.  

A pipeline is a set of stages that are executed in a specific order based on the dependencies between the stages (deps and outs).

The pipeline will be executed by `dvc repro` to reproduce the experiment. 

Each `dvc stage add` command will create a new stage in the `dvc.yaml` file. 

The `dvc.yaml` file can also be edited manually.

Store the command to prepare the dataset in DVC.

#### `prepare` stage

Store the command to prepare the experiment data in DVC.

```sh
dvc stage add -n prepare \
  -p prepare.seed,prepare.split \
  -d src/prepare.py -d data/data.xml \
  -o data/prepared \
  python src/prepare.py data/data.xml
```

Explore the `dvc.yaml` file to understand how the pipeline is updated.

This command adds a new stage called _prepare_ that has the `src/prepare.py` and `data/data.xml` files as a dependency.

If any of these files change, DVC will run the command `python src/prepare.py data/data.xml` when using `dvc repro`.

The output of this command is `data/prepared`.

{% callout type="note" %}
The parameters `prepare.seed` and `prepare.split` will be discussed later.
{% /callout %}

#### `featurize` stage

Store the command to perform the features extraction in DVC.

```sh
dvc stage add -n featurize \
  -p featurize.max_features,featurize.ngrams \
  -d src/featurization.py -d data/prepared \
  -o data/features/test.pkl -o data/features/train.pkl \
  python src/featurization.py data/prepared data/features
```

Explore the `dvc.yaml` file to understand how the pipeline is updated.

This command adds a new stage called _featurize_ that has the `src/featurization.py` and `data/prepared` files as a dependency.

If any of these files change, DVC will run the command `python src/featurization.py data/prepared data/features` when using `dvc repro`.

The outputs of this command are `data/features/test.pkl` and `data/features/train.pkl` files.

{% callout type="note" %}
The parameters `featurize.max_features` and `featurize.ngrams` will be discussed later.
{% /callout %}

#### `train` stage

Store the command to train the model in DVC.

```sh
dvc stage add -n train \
  -p train.seed,train.n_est,train.min_split \
  -d src/train.py -d data/features \
  -o model.pkl \
  python src/train.py data/features model.pkl
```

Explore the `dvc.yaml` file to understand how the pipeline is updated.

This command adds a new stage called _train_ that has the `src/train.py` and `data/features` files as a dependency of the DVC pipeline.

If any of these files change, DVC will run the command `python src/train.py data/features model.pkl` when using `dvc repro`.

The output of this command is `model.pkl`.

{% callout type="note" %}
The parameters `train.seed`, `train.n_est` and `train.min_split` will be discussed later.
{% /callout %}

#### `evaluate` stage

Store the command to evaluate the model in DVC.

```sh
dvc stage add -n evaluate \
  -d src/evaluate.py -d model.pkl \
  -O evaluation/plots/metrics \
  --metrics-no-cache evaluation/metrics.json \
  --plots-no-cache evaluation/plots/prc.json \
  --plots-no-cache evaluation/plots/sklearn/roc.json \
  --plots-no-cache evaluation/plots/sklearn/confusion_matrix.json \
  --plots evaluation/plots/importance.png \
  python src/evaluate.py model.pkl data/features
```

Explore the `dvc.yaml` file to understand how the pipeline is updated.

This command adds a new stage called _evaluate_ that has the `src/evaluate.py`, `model.pkl` and `data/features` files as a dependency.

If any of these files change, DVC will run the command `python src/evaluate.py model.pkl data/features` when using `dvc repro`.

This command writes the model's metrics to `evaluation/metrics.json`. It writes the `confusion_matrix` to `evaluation/plots/sklearn/confusion_matrix.json`, the `precision_recall_curve` to `evaluation/plots/prc.json ` and the `roc_curve` to `evaluation/plots/sklearn/roc.json` that will be used to create plots.

Update the plots to set the axes with the following commands.

```sh
# Set the axes for the `precision_recall_curve`
dvc plots modify evaluation/plots/prc.json -x recall -y precision

# Set the axes for the `roc_curve`
dvc plots modify evaluation/plots/sklearn/roc.json -x fpr -y tpr

# Set the axes for the `confusion_matrix`
dvc plots modify evaluation/plots/sklearn/confusion_matrix.json -x actual -y predicted -t confusion
```

#### Summary of the DVC pipeline

The pipeline is now entirely defined. You can explore the `dvc.yaml` file to understand how the pipeline is defined.

DVC updated the main `.gitignore` file with the model, as it is an output of the  `train` stage.

```sh
## Python

# Environments
.venv

# Byte-compiled / optimized / DLL files
__pycache__/

## DVC

# DVC will add new files after this line
/model.pkl
```

### Visualize the pipeline

You can visualize the pipeline to check the stages that will be performed.

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
          *
          *
          *
      +-------+
      | train |
      +-------+
          *
          *
          *
    +----------+
    | evaluate |
    +----------+
```

If any dependencies/outputs change, the affected stages will be reexecuted.

### Execute the pipeline

Now that the pipeline has been defined, you can reproduce it.

```sh
# Execute only the required pipeline stages
dvc repro
```

{% callout type="note" %}
You can force the execution of the entire pipeline with the command `dvc repro --force`.
{% /callout %}

The parameters discussed before - defined in the `params.yaml` file - can be edited to re-run the experiment. DVC will track all these parameters and store the outputs' results in its cache so it will not re-run the experiment if not needed.

### Push the changes to DVC and Git

Push all DVC and Git files to the remote.

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

### Check the results

Congrats! You now have a defined and common way to reproduce the pipeline to create a model. The stages will be ran only if files or parameters change.

This chapter is done, you can check the summary.

## Summary

In this chapter, you have successfully:

- Removed custom rules from the gitignore file
- Set up four DVC pipeline stages
  - `prepare`
  - `featurize`
  - `train`
  - `evaluate`
- Visualized the pipeline
- Executed the pipeline
- Pushed the changes to DVC and Git

You did fix some of the previous issues:

- ✅ The steps used to create the model are documented and can be re-executed

When used by another member of the team, they can easily reproduce your experiment with the help of DVC with the following commands.

```sh
# Execute the pipeline
dvc repro
```

It will only run the required stages thanks to DVC cache.

You can safely continue to the next chapter.

## State of the MLOps process

- ✅ Codebase can be shared and improved by multiple developers;
- ✅ The dataset can be shared among the developers and is placed in the right directory in order to run the experiment;
- ✅ The steps used to create the model are documented and can be re-executed;
- ❌ Changes to model are not easily visualized;
- ❌ Experiment may not be reproducible on other machines;
- ❌ Model may have required artifacts that are forgotten or omitted in saved/loaded state. There is no easy way to use the model outside of the experiment context.

## Sources

Highly inspired by the [_Get Started: Data Pipelines_ - dvc.org](https://dvc.org/doc/start/data-management/pipelines) guide.

Want to see what the result at the end of this chapter should look like? Have a look at the Git repository directory here: [chapter-4-reproduce-the-experiment-with-dvc](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/chapter-4-reproduce-the-experiment-with-dvc).

## Next & Previous chapters

- **Previous**: [Chapter 3: Share your ML experiment data with DVC](/the-guide/chapter-3-share-your-ml-experiment-data-with-dvc)
- **Next**: [Chapter 5: Track model evolutions with DVC](/the-guide/chapter-5-track-model-evolutions-with-dvc)
