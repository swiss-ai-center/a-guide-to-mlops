---
title: "Chapter 1: Run a simple ML experiment"
---

# {% $markdoc.frontmatter.title %}

## Summary

Let's imagine you recently arrived in a new ML team. They have a very nice ML experiment that you have to take on. This experiment is quite simple:

- It uses 10K posts from StackOverflow
    - The posts that are related to the R programming language are marked with `1`, the others with `0`
- It splits all of them into training/testing datasets
- It makes bags of words matrixes from the title and the description of all posts
- It trains the model to classify the R posts vs. the non-R posts from the training dataset
- It evaluates the performance of the model using the testing dataset with the following metrics:
    - Measure the Precision-Recall of the R posts vs. the non-R posts
    - Measure the Receiver operating characteristic of the R posts vs. the non-R posts
    - Measure the most important words characterising the R posts vs. the non-R posts

Your job is to set up MLOps tools to improve the team efficiency, help the documentation of the workflow, track changes made to a model and easily serve the model to the rest of the world.

In this chapter, you will:

1. Set up the working directory
2. Download the codebase
3. Download the dataset
4. Set up a Python environment to run the experiment
5. Run the experiment locally for the first time

Let's start!

## Steps

{% callout type="warning" %}
This guide has been written with macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use [GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

### Set up the working directory

{% callout type="note" %}
If it's the first time you follow this guide, we recommend you to check the [Introduction - Requirements](/the-guide/introduction#requirements).
{% /callout %}

As you started as a new collaborator, create a directory on your computer that you will use for the this new awesome ML experiment. This directory will be your working directory for the rest of the guide.

### Download and set up the codebase

One of your colleague has given you their codebase on a USB stick so you don't start everything from scratch (how nice of them). It's still an old way to share files with colleagues but you weren't hired for nothing right?

Their work has to be copied in your working directory.

_To simulate the USB stick, you can download the source code for this simple ML experiment from GitHub with the following commands._

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

Explore the codebase and try to understand the content of the files. You have a summary for each file below.

Your working directory should look like this.

```
.
├── src
│   ├── evaluate.py
│   ├── featurization.py
│   ├── prepare.py
│   ├── requirements.txt
│   └── train.py
└── params.yaml
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

The same colleague that gave you the codebase told you that you can get the dataset from the company's NAS. This is where all data is stored and you can get a copy of it there.

They told you that the data must be saved as `data/data.xml` in your working directory. Otherwise, the experiment cannot be run.

_To simulate the download of the dataset from the NAS, you can download the dataset for this simple ML experiment from GitHub with the following commands._

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

Explore the dataset and try to understand the content of the file.

Your working directory should now look like this.

```
.
├── data
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

Great! You now have everything you need to run the experiment: the codebase is set up, the dataset is in the right place and you can finally try the experiment for the first time.

Generate the virtual environment and install the dependencies in your working directory with the following commands.

```sh
# Generate the virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the requirements
pip install --requirement src/requirements.txt
```

The same nice colleague knows by heart how to run the experiment. They give you the steps.

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

### Check the results

Congrats! You have now a running experiment on your machine. Thanks to your dear colleague, you were able to run the experiment. Without their advice, you wouldn't know how to run the experiment on your machine.

Explore the outputs and try to understand the content of the files.

Your working directory should now look like this.

```
.
├── data
│   ├── features
│   │   ├── test.pkl
│   │   └── train.pkl
│   ├── prepared
│   │   ├── test.tsv
│   │   └── train.tsv
│   └── data.xml
├── evaluation
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
├── model.pkl
└── params.yaml
```

This chapter is done, you can check the summary.

## Summary

In this chapter, you were able to:

1. Set up the working directory
2. Download the codebase
3. Download the dataset
4. Set up a Python environment to run the experiment
5. Run the experiment locally for the first time

You have spotted the following issues:

- ❌ The codebase still needs to be downloaded and set up locally in order to run the experiment;
- ❌ The dataset still needs to be downloaded and placed in the right directory in order to run the experiment;
- ❌ Someone had to tell you the steps used to create the model.

You will improve the workflow for better efficiency and teamwork in the next steps. You can now safely continue the guide.

## State of the MLOps process

- ❌ The codebase still needs to be downloaded and set up locally in order to run the experiment;
- ❌ The dataset still needs to be downloaded and placed in the right directory in order to run the experiment;
- ❌ Someone has to tell you the steps used to create the model and they can be forgotten/undocumented;
- ❌ The changes done to a model cannot be visualized and improvements and/or deteriorations are hard to identify;
- ❌ There is no guarantee that the experiment can be executed on another machine;
- ❌ The model might have required artifacts that can be forgotten or omitted when saving/loading the model for future usage. There is no easy way to use the model outside of the experiment context.

## Sources

Highly inspired by the [_Get Started: Data Pipelines_ - dvc.org](https://dvc.org/doc/start/data-management/pipelines) guide.

Want to see what the result of this step should look like? Have a look at the Git repository directory here: [chapter-1-run-a-simple-ml-experiment](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/chapter-1-run-a-simple-ml-experiment).

## Next & Previous steps

- **Previous**: [Introduction](/the-guide/introduction)
- **Next**: [Step 2: Share your ML experiment code with Git](/the-guide/step-2-share-your-ml-experiment-code-with-git)
