---
title: "Chapter 4: Reproduce the experiment with DVC"
---

# {% $markdoc.frontmatter.title %}

## Summary

{% callout type="note" %}
Highly inspired by the [_Get Started: Data Pipelines_ - dvc.org](https://dvc.org/doc/start/data-management/pipelines) guide.
{% /callout %}

Now that both our code and our data can be shared and manipulated by our team, it's time to procedurize our experiment's steps using DVC to make them easily reproductible and standardized.

We will be using DVC stages to create a pipeline that will be executed by `dvc repro`. A stage in DVC is a command that is executed to produce a result. The result of a stage is a file or a directory. The command of a stage is executed only if the stage's dependencies have changed.

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

We will split these steps into 3 stages :
- prepare
- featurize
- train


## Instructions

{% callout type="warning" %}
This guide has been written with macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use [GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

#### Update the `.gitignore` file. 

Various DVC commands will automatically include the files and directories that should be ignored by Git. We need to take care of files and folders that are outside of the DVC scope. 

Please update the `.gitignore` file with the following content:


```sh
## Custom experiment

# The models evaluations
evaluation

## Python

# Environments
.venv

# Byte-compiled / optimized / DLL files
__pycache__/

## DVC
/model.pkl
```

#### Setup the DVC pipeline

Each step of the experiment will be stored as a DVC stage.  

A pipeline is a set of stages that are executed in a specific order based on the dependencies between the stages (deps and outs).

The pipeline will be executed by `dvc repro` to reproduce the experiment. 

Each `dvc stage add` command will create a new stage in the `dvc.yaml` file. 

`dvc.yaml` file can also be edited manually.

Store the command to prepare the dataset in DVC.

###### Prepare stage

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

###### Featurize stage

Store the command to perform the features extraction in DVC.

```sh
dvc stage add -n featurize \
  -p featurize.max_features,featurize.ngrams \
  -d src/featurization.py -d data/prepared \
  -o data/features/test.pkl -o data/features/train.pkl \
  python src/featurization.py data/prepared data/features
```

This command adds a new stage called _featurize_ that has the `src/featurization.py` and `data/prepared` files as a dependency.

If any of these files change, DVC will run the command `python src/featurization.py data/prepared data/features` when using `dvc repro`.

The outputs of this command are `data/features/test.pkl` and `data/features/train.pkl` files.

{% callout type="note" %}
The parameters `featurize.max_features` and `featurize.ngrams` will be discussed later.
{% /callout %}

###### Train stage

Store the command to train the model in DVC.

```sh
dvc stage add -n train \
  -p train.seed,train.n_est,train.min_split \
  -d src/train.py -d data/features \
  -o model.pkl \
  python src/train.py data/features model.pkl
```

This command adds a new stage called _train_ that has the `src/train.py` and `data/features` files as a dependency of the DVC pipeline.

If any of these files change, DVC will run the command `python src/train.py data/features model.pkl` when using `dvc repro`.

The output of this command is `model.pkl`.

{% callout type="note" %}
The parameters `train.seed`, `train.n_est` and `train.min_split` will be discussed later.
{% /callout %}

###### Execute the pipeline.

```sh
# Execute only the required pipeline stages (if files or parameters changed)
dvc repro
```

{% callout type="note" %}
You can force the execution of the entire pipeline with the command `dvc repro --force`.
{% /callout %}

###### Visualize the pipeline.

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
```

###### Push the changes to DVC and Git.

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

The parameters discussed before - defined in the `params.yaml` file - can be edited to re-run the experiment. DVC will track all these parameters and store the outputs' results in its cache so it will not re-run the experiment if not needed.

Congrats! You now have a defined and common way to reproduce the pipeline to create a model. The stages will be ran only if files or parameters change.

## Check the results

Want to see what the result at the end of this chapter should look like? Have a look at the Git repository directory here: [chapter-4-reproduce-the-experiment-with-dvc](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/chapter-4-reproduce-the-experiment-with-dvc).

## State of the MLOps process

- ✅ The codebase can be shared among the developers. The codebase can be improved collaboratively;
- ✅ The dataset can be shared among the developers and is placed in the right directory in order to run the experiment;
- ✅ The steps used to create the model are documented and can be re-executed;
- ❌ The changes done to a model cannot be visualized and improvements and/or deteriorations are hard to identify;
- ❌ There is no guarantee that the experiment can be executed on another machine;
- ❌ The model might have required artifacts that can be forgotten or omitted when saving/loading the model for future usage. There is no easy way to use the model outside of the experiment context.

## Next & Previous Chapter

- **Previous**: [Chapter 3: Share your ML experiment data with DVC](/the-guide/chapter-3-share-your-ml-experiment-data-with-dvc)
- **Next**: [Chapter 5: Track model evolutions with DVC](/the-guide/chapter-5-track-model-evolutions-with-dvc)
