---
title: "Chapter 1: Run a simple ML experiment"
---

# {% $markdoc.frontmatter.title %}

## Introduction

You've just joined a new ML team with a promising ML experiment in hand. The experiment is straightforward using 10,000 StackOverflow posts:

- Mark the R-related posts posts as `1` and the others as `0`.
- Split the posts into training/testing datasets.
- Create bag-of-words matrices from the post titles and descriptions.
- Train a model to classify R vs. non-R posts using the training dataset.
- Evaluate the model's performance using the following metrics: precision-recall, Receiver operating characteristic (ROC), and key words.

Your goal is to streamline the team's workflow by setting up MLOps tools, documenting the process, tracking changes, and making the model accessible to others.

In this chapter, you will:

1. Set up the project directory
2. Acquire the codebase
3. Obtain the dataset
4. Create a Python environment to run the experiment
5. Launch the experiment locally for the first time.

Let's get started!

## Steps

{% callout type="warning" %}
This guide has been written with macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use [GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

### Set up the project directory

{% callout type="note" %}
If it's the first time you follow this guide, we recommend you to check the [Introduction - Requirements](/the-guide/introduction#requirements).
{% /callout %}

As a new team member, set up a project directory on your computer for this exciting ML experiment. This directory will serve as your working directory for the duration of the guide.

### Download and set up the codebase

Your colleague has generously provided you with their codebase on a USB stick. Although this may be an outdated method of sharing files, you're ready to tackle the task.

Copy the codebase into your working directory.

_As an alternative to the USB stick, you can also download the source code for this simple ML experiment from GitHub using these commands._

```sh
# Download the archive containing the code
wget https://github.com/csia-pme/a-guide-to-mlops/archive/refs/heads/code.zip -O code.zip

# Extract the code
unzip code.zip

# Move the subdirectory files to the working directory
mv a-guide-to-mlops-code/src ./src
mv a-guide-to-mlops-code/params.yaml ./params.yaml

# Remove the archive directory
rm -rf a-guide-to-mlops-code

# Remove the archive
rm -f code.zip
```

### Explore the codebase

Take some time to familiarize yourself with the codebase by examining its contents. The following is a summary of each file.

This is what your working directory should look like.

```
.
├── src <- this is new
│   ├── evaluate.py
│   ├── featurization.py
│   ├── prepare.py
│   ├── requirements.txt
│   └── train.py
└── params.yaml  <- this is new
```

| **File**              | **Description**                                   | **Input**                             | **Output**                                                        |
|-----------------------|---------------------------------------------------|---------------------------------------|-------------------------------------------------------------------|
| `requirements.txt`    | The Python dependencies to run the ML experiment  | -                                     | -                                                                 |
| `params.yaml`         | The parameters to run the ML experiment           | -                                     | -                                                                 |
| `prepare.py`          | Prepare the dataset to run the ML experiment      | The dataset to prepare as an XML file | The prepared data in `data/prepared` directory                    |
| `featurization.py`    | Extract the features from the dataset             | The prepared dataset                  | The extracted features in `data/features` directory               |
| `train.py`            | Train the ML model                                | The extracted features                | The model trained with the dataset                                |
| `evaluate.py`         | Evaluate the ML model using DVC                   | The model to evaluate                 | The results of the model evaluation in `evaluation` directory     |

### Download and set up the dataset

Your colleague informed you that you can obtain the dataset from the company's Network Attached Storage (NAS). This is the centralized location for all data and you can easily retrieve a copy from there.

They told you the dataset must be saved as `data/data.xml` in your working directory for the experiment to run correctly.

_As an alternative to accessing the NAS, you can download the dataset for this simple ML experiment from GitHub using these commands._

```sh
# Download the archive containing the dataset
wget https://github.com/csia-pme/a-guide-to-mlops/archive/refs/heads/data.zip -O data.zip

# Extract the dataset
unzip data.zip

# Create the data directory
mkdir data

# Move the `data.xml` file to the working directory
mv a-guide-to-mlops-data/data.xml data/data.xml

# Remove the archive directory
rm -rf a-guide-to-mlops-data

# Remove the archive
rm -f data.zip
```

### Explore the dataset

Examine the dataset to get a better understanding of its contents.

Your working directory should now look like this

```
.
├── data <- this is new
│   └── data.xml
├── src
│   ├── evaluate.py
│   ├── featurization.py
│   ├── prepare.py
│   ├── requirements.txt
│   └── train.py
└── params.yaml
```

### Run the experiment

Awesome! You have everything you need to run the experiment: the codebase is ready, the dataset is in place, and you're ready to run the experiment for the first time.

Create the virtual environment and install necessary dependencies in your working directory using these commands.

```sh
# Create the virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the requirements
pip install --requirement src/requirements.txt
```

Your helpful colleague provided you with the steps to run the experiment.

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

{% callout type="note" %}
The `evaluate.py` Python script might display a warning regarding DVC. You can safely ignore it for now.
{% /callout %}

Examine the experiment results to gain insights into the output files.

### Check the results

Congratulations! You've successfully run the experiment on your machine, with guidance from your colleague. Your working directory should now appear as follows.

```
.
├── .venv <- this is new
│   └── ...
├── data
│   ├── features <- this is new
│   │   ├── test.pkl
│   │   └── train.pkl
│   ├── prepared <- this is new
│   │   ├── test.tsv
│   │   └── train.tsv
│   └── data.xml
├── evaluation <- this is new
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
├── model.pkl <- this is new
└── params.yaml
```

This chapter is done, you can check the summary.

## Summary

In this chapter, you have successfully:

1. Created the working directory
2. Acquired the codebase
3. Obtained the dataset
4. Set up a Python environment to run the experiment
5. Executed the experiment locally for the first time

However, you have identified the following areas for improvement:

- ❌ Codebase still needs manual download
- ❌ Dataset still needs manual download and placement
- ❌ Steps to run the experiment were not documented

In the next chapters, you will enhance the workflow for better efficiency and teamwork.

You can safely continue to the next chapter.

## State of the MLOps process

- ❌ Codebase requires manual download and setup;
- ❌ Dataset requires manual download and placement;
- ❌ Model steps rely on verbal communication and may be undocumented;
- ❌ Changes to model are not easily visualized;
- ❌ Experiment may not be reproducible on other machines;
- ❌ Model may have required artifacts that are forgotten or omitted in saved/loaded state. There is no easy way to use the model outside of the experiment context.

You will address these issues in the next chapters for improved efficiency and collaboration. Continue the guide to learn how.

## Sources

Highly inspired by the [_Get Started: Data Pipelines_ - dvc.org](https://dvc.org/doc/start/data-management/pipelines) guide.

Want to see what the result at the end of this chapter should look like? Have a look at the Git repository directory here: [chapter-1-run-a-simple-ml-experiment](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/chapter-1-run-a-simple-ml-experiment).

## Next & Previous chapters

- **Previous**: [Introduction](/the-guide/introduction)
- **Next**: [Chapter 2: Share your ML experiment code with Git](/the-guide/chapter-2-share-your-ml-experiment-code-with-git)
