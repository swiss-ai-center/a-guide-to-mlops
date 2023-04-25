# Chapter 1: Run a simple ML experiment

## Introduction

You have just joined a new ML team whose goal is to build a model that can
classify text into two categories: "related to R programming language" and "not
related to R programming language".

Their dataset consists of 10,000 posts from StackOverflow.

The training process is as follows:

- Mark the R-related posts posts as `1` and the others as `0`
- Split the posts into training/testing datasets
- Create bag-of-words matrices from the post titles and descriptions
- Train a model to classify R vs. non-R posts using the training dataset
- Evaluate the model's performance using a precision-recall (PR) curve and a
  receiver operating characteristic (ROC) curve

Your goal is to streamline the team's workflow by setting up MLOps tools,
documenting the process, tracking changes, and making the model accessible to
others.

In this chapter, you will learn how to:

1. Set up the project directory
2. Acquire the codebase
3. Obtain the dataset
4. Create a Python environment to run the experiment
5. Launch the experiment locally for the first time

Let's get started!

## Steps

### Set up the project directory

As a new team member, set up a project directory on your computer for this
ground breaking ML experiment. This directory will serve as your working
directory for the duration of the guide.

### Download and set up the codebase

Your colleague has generously provided you a ZIP file containing the source
code. Although this may be an outdated method for sharing files, you are ready to
tackle the task.

```sh title="Execute the following command(s) in a terminal"
# Download the archive containing the code
wget https://github.com/csia-pme/a-guide-to-mlops/archive/refs/heads/code.zip -O code.zip
```

Unzip the codebase into your working directory.

```sh title="Execute the following command(s) in a terminal"
# Extract the code
unzip code.zip

# Move the subdirectory files to the working directory
mv a-guide-to-mlops-code/* .

# Remove the archive and the directory
rm -r code.zip a-guide-to-mlops-code
```

### Explore the codebase

Take some time to get familiar with the codebase and examine its
contents. The following is a summary of each file.

This is what your working directory should look like.

```yaml hl_lines="2-10"
.
├── src # (1)!
│   ├── evaluate.py
│   ├── featurization.py
│   ├── prepare.py
│   └── train.py
├── params.yaml # (2)!
├── poetry.lock # (3)!
├── pyproject.toml # (4)!
└── README.md # (5)!
```

1. This, and all its sub-directory, is new.
2. This is new.
3. This is new.
4. This is new.
5. This is new.

The following table describes the files present in the codebase.

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

### Download and set up the dataset

Your colleague provided you the following URL to download an archive containing
the dataset for this machine learning experiment.

```sh title="Execute the following command(s) in a terminal"
# Download the archive containing the dataset
wget https://github.com/csia-pme/a-guide-to-mlops/archive/refs/heads/data.zip -O data.zip
```

This archive must be decompressed and its contents be moved in the
`data` directory in the working directory of the experiment.

```sh title="Execute the following command(s) in a terminal"
# Extract the dataset
unzip data.zip

# Move the `data.xml` file to the working directory
mv a-guide-to-mlops-data/ data/

# Remove the archive and the directory
rm data.zip
```

### Explore the dataset

Examine the dataset to get a better understanding of its contents.

Your working directory should now look like this:

```yaml hl_lines="2-4"
.
├── data # (1)!
│   ├── data.xml
│   └── README.md
├── src
│   ├── evaluate.py
│   ├── featurization.py
│   ├── prepare.py
│   └── train.py
├── params.yaml
├── pyproject.toml
├── poetry.lock
└── README.md
```

1. This, and all its sub-directory, is new.

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

Your helpful colleague provided you some steps to reproduce the experiment.

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

Congratulations! You have successfully reproduced the experiment on your machine.

In this chapter, you have:

1. Created the working directory
2. Acquired the codebase
3. Obtained the dataset
4. Set up a Python environment to run the experiment
5. Executed the experiment locally for the first time

However, you may have identified the following areas for improvement:

- ❌ Codebase still needs manual download
- ❌ Dataset still needs manual download and placement
- ❌ Steps to run the experiment were not documented

In the next chapters, you will enhance the workflow to fix those issues.

You can now safely continue to the next chapter.

## State of the MLOps process

- ❌ Codebase requires manual download and setup
- ❌ Dataset requires manual download and placement
- ❌ Model steps rely on verbal communication and may be undocumented
- ❌ Changes to model are not easily visualized
- ❌ Experiment may not be reproducible on other machines
- ❌ Model may have required artifacts that are forgotten or omitted in
  saved/loaded state and there is no easy way to use the model outside of the
  experiment context

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by the [_Get Started: Data Pipelines_ -
dvc.org](https://dvc.org/doc/start/data-management/data-pipelines) guide.

Want to see what the result at the end of this chapter should look like locally? Have a
look at the Git repository directory here:
[chapter-1-run-a-simple-ml-experiment](https://github.com/csia-pme/a-guide-to-mlops/tree/main/docs/the-guide/chapter-1-run-a-simple-ml-experiment).
