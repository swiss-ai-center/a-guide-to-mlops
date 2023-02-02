---
title: "Chapter 4: Reproduce the experiment with DVC"
---

# {% $markdoc.frontmatter.title %}

## Introduction

A key component of DVC is the concept of "stages". Stages are essentially
commands that produce a result, whether that be a file or directory. The beauty
of DVC is that these stages are executed only when the dependencies they rely on
have changed. This way, we don't have to waste time re-running unnecessary
steps.

By using DVC stages to create a pipeline, we can execute all of our experiment's
steps in a streamlined manner by simply running the `dvc repro` command. As a result, DVC
makes it easy to reproduce the experiment and track the effects of changes.

In this chapter, you will learn how to:

1. Remove custom rules from the gitignore file;
2. Set up four DVC pipeline stages:
  - `prepare`,
  - `featurize`,
  - `train`,
  - `evaluate`;
1. Visualize the pipeline;
2. Execute the pipeline;
3. Push the changes to DVC and Git.

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

Let's get started!

## Steps

### Remove custom rules from the gitignore file

As seen in the previous chapter, DVC can update `.gitignore` files.

As you will define the entire experiment pipeline with DVC, you can safely
remove all the custom rules from the main `.gitignore` file so DVC can manage
them for you. At the end of this chapter, DVC should have updated all the
`.gitignore` files.

Update the `.gitignore` file to remove your experiment data. The required files
to be ignored will then be added by DVC.

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

The output should be similar to this:

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

A DVC pipeline is a set of stages that are executed in a specific order based on the
dependencies between the stages (deps and outs). The `dvc repro` command
executes the pipeline to reproduce the experiment.

In the following sections, each step of the experiment will be converted into a stage of a DVC pipeline.
The `dvc stage add` command creates a new stage in the pipeline. 
This stage will be added to the `dvc.yaml` file that describes the pipeline.
This file can also be edited manually.

The `dvc stage add` accepts some options:
- `-n` specifies the name of the stage;
- `-p` specifies the parameters of the stage (referenced in the `params.yaml` file);
- `-d` specifies the dependencies of the stage;
- `-o` specifies the outputs of the stage;
- `--metrics-no-cache` specifies the metrics of the stage (not cached by DVC);
- `--plots-no-cache` specifies the plots of the stage (not cached by DVC).

As parameters are an important part of the experiment, they are versioned in a `params.yaml` file.
DVC keeps track of these parameters and of the corresponding results.

Dependencies and outputs are files or directories that are used or produced by the stage.
If any of these files change, DVC will re-run the command of the stage when using `dvc repro`.

#### `prepare` stage

Run the following command to add a new stage called _prepare_ that prepares the dataset.

```sh
dvc stage add -n prepare \
  -p prepare.seed,prepare.split \
  -d src/prepare.py -d data/data.xml \
  -o data/prepared \
  python src/prepare.py data/data.xml
```

The values of the parameters `prepare.seed` and `prepare.split` are referenced in the `params.yaml` file.

This stage has the `src/prepare.py` and `data/data.xml` files as dependencies.
If any of these files change, DVC will run the command 
`python src/prepare.py data/data.xml` when using `dvc repro`.

The output of this command is stored in the `data/prepared` directory.

Take some time to explore the `dvc.yaml` file and to understand how the pipeline is updated.

#### `featurize` stage

Run the following command to create a new stage called _featurize_ that performs the features extraction.

```sh
dvc stage add -n featurize \
  -p featurize.max_features,featurize.ngrams \
  -d src/featurization.py -d data/prepared \
  -o data/features/test.pkl -o data/features/train.pkl \
  python src/featurization.py data/prepared data/features
```

The values of the parameters `featurize.max_features` and `featurize.ngrams` are referenced in the `params.yaml` file.

This stage has the `src/featurization.py` file and `data/prepared` directory as dependencies.
If any of these files change, DVC will run the command 
`python src/featurization.py data/prepared data/features` 
when using `dvc repro`.

The outputs of this command are stored in the `data/features/test.pkl` and
`data/features/train.pkl` files.

Explore the `dvc.yaml` file to understand how the pipeline is updated.

#### `train` stage

Run the following command to create a new stage called _train_ that trains the model.

```sh
dvc stage add -n train \
  -p train.seed,train.n_est,train.min_split \
  -d src/train.py -d data/features \
  -o model.pkl \
  python src/train.py data/features model.pkl
```

The values of the parameters `train.seed`, `train.n_est` and `train.min_split` are referenced in the `params.yaml` file.

This stage has the `src/train.py` and `data/features` files as dependencies.
If any of these files change, DVC will run the command 
`python src/train.py data/features model.pkl` when using `dvc repro`.

The output of this command is stored in the `model.pkl` file.

Explore the `dvc.yaml` file to understand how the pipeline is updated.

#### `evaluate` stage


Run the following command to create a new stage called _evaluate_ that evaluates the model.

```sh
dvc stage add -n evaluate \
  -d src/evaluate.py -d model.pkl \
  -O evaluation/plots/metrics \
  --metrics-no-cache evaluation/metrics.json \
  --plots-no-cache evaluation/plots/prc.json \
  --plots-no-cache evaluation/plots/sklearn/roc.json \
  --plots-no-cache evaluation/plots/sklearn/confusion_matrix.json \
  --plots-no-cache evaluation/plots/importance.png \
  python src/evaluate.py model.pkl data/features
```

This stage has the `src/evaluate.py` file and `model.pkl` file, and the `data/features` directory as dependencies.
If any of these files change, DVC will run the command 
`python src/evaluate.py model.pkl data/features` when using `dvc repro`.

This command writes the model's metrics to `evaluation/metrics.json`. It writes
the `confusion_matrix` to `evaluation/plots/sklearn/confusion_matrix.json`, the
`precision_recall_curve` to `evaluation/plots/prc.json ` and the `roc_curve` to
`evaluation/plots/sklearn/roc.json` that will be used to create plots.
Here, `no-cache` prevents DVC from caching the metrics and plots.


DVC has the ability to generate images for the plots.
The following command are used to tune the axes of the plots.

```sh
# Set the axes for the `precision_recall_curve`
dvc plots modify evaluation/plots/prc.json -x recall -y precision

# Set the axes for the `roc_curve`
dvc plots modify evaluation/plots/sklearn/roc.json -x fpr -y tpr

# Set the axes for the `confusion_matrix`
dvc plots modify evaluation/plots/sklearn/confusion_matrix.json -x actual -y predicted -t confusion
```

Explore the `dvc.yaml` file to understand how the pipeline is updated.

#### Summary of the DVC pipeline

The pipeline is now entirely defined. You can explore the `dvc.yaml` file to
see all the stages and their dependencies.

Notice that DVC also updated the main `.gitignore` file with the model, as it is an output of the
`train` stage.

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

Now that the pipeline has been defined, you can execute it and reproduce the experiment.

```sh
# Execute only the required pipeline stages
dvc repro
```

{% callout type="note" %} You can force the execution of the entire pipeline
with the command `dvc repro --force`. {% /callout %}

### Check the changes

Check the changes with Git to ensure all wanted files are here.

```sh
# Add all the files
git add .

# Check the changes
git status
```

The output of the `git status` command should be similar to this.

```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   .gitignore
        modified:   data/.gitignore
        new file:   data/features/.gitignore
        new file:   dvc.lock
        new file:   dvc.yaml
        modified:   evaluation/report.html
```

### Push the changes to DVC and Git

Push all the DVC changes to the remote storage and all the Git changes to the remote repository.

```sh
# Upload the experiment data and cache to the remote bucket
dvc push

# Commit the changes
git commit -m "My ML experiment commands are saved with DVC"

# Push the changes
git push
```

This chapter is done, you can check the summary.

## Summary

Congrats! You have defined a pipeline and know how to reproduce your experiment. 

In this chapter, you have successfully:

1. Removed custom rules from the gitignore file;
2. Set up four DVC pipeline stages;
  - `prepare`,
  - `featurize`,
  - `train`,
  - `evaluate`;
1. Visualized the pipeline;
2. Executed the pipeline;
3. Pushed the changes to DVC and Git.

You did fix some of the previous issues:

- ✅ The steps used to create the model are documented and can be reproduced.

With the help of DVC, another member of your team can now easily reproduce your
experiment and, thanks to caching, only the required steps will be executed.

```sh
# Execute the pipeline
dvc repro
```

However, you might have identified the following areas for improvement:

- ❌ How can I ensure my changes helps to improve the model?
- ❌ How can I ensure my model still can be run on someone's computer?

In the next chapters, you will enhance the workflow to fix these issues.

You can now safely continue to the next chapter.

## State of the MLOps process

- ✅ The codebase can be shared and improved by multiple developers;
- ✅ The dataset can be shared among the developers and is placed in the right
  directory in order to run the experiment;
- ✅ The steps used to create the model are documented and can be re-executed;
- ❌ Changes to model are not easily visualized;
- ❌ Experiment may not be reproducible on other machines;
- ❌ Model may have required artifacts that are forgotten or omitted in
  saved/loaded state. There is no easy way to use the model outside of the
  experiment context.

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by the [_Get Started: Data Pipelines_ -
dvc.org](https://dvc.org/doc/start/data-management/pipelines) guide.

Want to see what the result at the end of this chapter should look like? Have a
look at the Git repository directory here:
[chapter-4-reproduce-the-experiment-with-dvc](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/chapter-4-reproduce-the-experiment-with-dvc).

## Next & Previous chapters

- **Previous**: [Chapter 3: Share your ML experiment data with
  DVC](/the-guide/chapter-3-share-your-ml-experiment-data-with-dvc)
- **Next**: [Chapter 5: Track model evolutions with
  DVC](/the-guide/chapter-5-track-model-evolutions-with-dvc)
