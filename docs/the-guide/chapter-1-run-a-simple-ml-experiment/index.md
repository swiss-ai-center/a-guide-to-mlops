# Chapter 1: Run a simple ML experiment

## Introduction

You've just joined a new ML team whose goal is to build a model that can
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
code. Although this may be an outdated method for sharing files, you're ready to
tackle the task.

```sh
# Download the archive containing the code
wget https://github.com/csia-pme/a-guide-to-mlops/archive/refs/heads/code.zip -O code.zip
```

Unzip the codebase into your working directory.

```sh
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

```yaml hl_lines="2-9"
.
├── src # this is new
│   ├── evaluate.py
│   ├── featurization.py
│   ├── prepare.py
│   ├── requirements.txt
│   └── train.py
├── params.yaml # this is new
└── README.md # this is new
```

The following table describes the files present in the codebase.

| **File**               | **Description**                                  | **Input**                             | **Output**                                                    |
| ---------------------- | ------------------------------------------------ | ------------------------------------- | ------------------------------------------------------------- |
| `src/requirements.txt` | The Python dependencies to run the ML experiment | -                                     | -                                                             |
| `src/prepare.py`       | Prepare the dataset to run the ML experiment     | The dataset to prepare as an XML file | The prepared data in `data/prepared` directory                |
| `src/featurization.py` | Extract the features from the dataset            | The prepared dataset                  | The extracted features in `data/features` directory           |
| `src/train.py`         | Train the ML model                               | The extracted features                | The model trained with the dataset                            |
| `src/evaluate.py`      | Evaluate the ML model using DVC                  | The model to evaluate                 | The results of the model evaluation in `evaluation` directory |
| `params.yaml`          | The parameters to run the ML experiment          | -                                     | -                                                             |

### Download and set up the dataset

Your colleague provide you the following URL to download an archive containing
the dataset for this machine learning experiment.

```sh
# Download the archive containing the dataset
wget https://github.com/csia-pme/a-guide-to-mlops/archive/refs/heads/data.zip -O data.zip
```

This archive must decompresed and its contents must be moved in the
 `data` directory in the working directory of the experiment.

```sh
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
├── data # this is new
│   ├── data.xml
│   └── README.md
├── src
│   ├── evaluate.py
│   ├── featurization.py
│   ├── prepare.py
│   ├── requirements.txt
│   └── train.py
├── params.yaml
└── README.md
```

### Run the experiment

Awesome! You now have everything you need to run the experiment: the codebase and
the dataset are in place; and you're ready to run the experiment for the first
time.

Create the virtual environment and install necessary dependencies in your
working directory using these commands.

```sh
# Create the virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the requirements
pip install --requirement src/requirements.txt
```

Your helpful colleague provided you some steps to reproduce the experiment.

```sh
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

```yaml hl_lines="2-3 5-10 13-24 31"
.
├── .venv # this is new
│   └── ...
├── data
│   ├── features # this is new
│   │   ├── test.pkl
│   │   └── train.pkl
│   ├── prepared # this is new
│   │   ├── test.tsv
│   │   └── train.tsv
│   ├── data.xml
│   └── README.md
├── evaluation # this is new
│   ├── plots
│   │   ├── metrics
│   │   │   ├── avg_prec.tsv
│   │   │   └── roc_auc.tsv
│   │   ├── sklearn
│   │   │   ├── confusion_matrix.json
│   │   │   └── roc.json
│   │   ├── importance.png
│   │   └── prc.json
│   ├── metrics.json
│   └── report.html
├── src
│   ├── evaluate.py
│   ├── featurization.py
│   ├── prepare.py
│   ├── requirements.txt
│   └── train.py
├── model.pkl # this is new
└── params.yaml
└── README.md
```

Here, the following should be noted:
- the `prepare.py` script created the `data/prepared` directory and splitted the
  dataset into a training set and a test set
- the `featurization.py` script created the `data/features` directory and
  extracted the features from the training and test sets
- the `train.py` script created the `model.pkl` file and trained the model with
  the extracted features
- the `evaluate.py` script created the `evaluation` directory and generated some
  plots and metrics to evaluate the model

Take some time to get familiar with the scripts and the results.

## Summary

Congratulations! You've successfully reproduced the experiment on your machine. 

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
  saved/loadedstate and there is no easy way to use the model outside of the
  experiment context

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by the [_Get Started: Data Pipelines_ -
dvc.org](https://dvc.org/doc/start/data-management/pipelines) guide.

Want to see what the result at the end of this chapter should look like? Have a
look at the Git repository directory here:
[chapter-1-run-a-simple-ml-experiment](https://github.com/csia-pme/a-guide-to-mlops/tree/main/docs/the-guide/chapter-1-run-a-simple-ml-experiment).
