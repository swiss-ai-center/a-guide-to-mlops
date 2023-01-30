---
title: "Chapter 1: Run a simple ML experiment"
---

# {% $markdoc.frontmatter.title %}

## Summary

Let's imagine you arrive in a new ML team. They have a very nice ML experiment that you have to take on. This experiment is quite simple:

- It uses 10K posts from StackOverflow
- It marks the posts that are related to the R programming language with `1`, the others with `0`
- It splits all of them into training/testing datasets
- It makes bags of words matrixes from the title and the description of all posts
- It trains the model to classify the R posts vs. the non-R posts from the training dataset
- It evaluates the performance of the model using the testing dataset with the following metrics:
    - Measure the Precision-Recall of the R posts vs. the non-R posts
    - Measure the Receiver operating characteristic of the R posts vs. the non-R posts
    - Measure the most important words characterising the R posts vs. the non-R posts

You job is to set up MLOps tools to inmprove the team efficiency, help the documentation of the workflow and track changes made to a model. When the team is happy with the model's performances, you can easily serve the model to the rest of the world.

In this chapter, you will:

1. Download the codebase
2. Download the dataset
3. Set up a Python environment to run the experiment
4. Run the experiment locally for the first time

## Steps

{% callout type="warning" %}
This guide has been written for macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use [GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

### Download and set up the codebase

In this team, one of your colleague might have given you their codebase on a USB stick to start the code so you don't start everything from scratch.

On your computer, create 

To simulate the USB stick, you can download the source code for this simple ML experiment from GitHub.

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

The working directory should look like this.

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

Explore the codebase and try to understand the content of the files. You have a summary of each file in the the directory.

| **File**              | **Description**                                   | **Input**                             | **Output**                                                        |
|-----------------------|---------------------------------------------------|---------------------------------------|-------------------------------------------------------------------|
| `requirements.txt`    | The Python dependencies to run the ML experiment  | -                                     | -                                                                 |
| `params.yaml`         | The parameters to run the ML experiment           | -                                     | -                                                                 |
| `prepare.py`          | Prepare the dataset to run the ML experiment      | The dataset to prepare as an XML file | The prepared data in `data/prepared` directory                    |
| `featurization.py`    | Extract the features from the dataset             | The prepared dataset                  | The extracted features in `data/features` directory               |
| `train.py`            | Train the ML model                                | The extracted features                | The model trained with the dataset                                |
| `evaluate.py`         | Evaluate the ML model using DVC                   | The model to evaluate                 | The results of the model evaluation in `evaluation` directory     |

### Download and set up the dataset

Download the dataset to run this simple ML experiment.

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

The working directory should look like this.

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

Generate the virtual environment and install the dependencies.

```sh
# Generate the virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the requirements
pip install --requirement src/requirements.txt
```

Run the experiment.

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

You have now a running experiment. Check the summary.

## Summary

Congrats! You have now a running experiment. 

Want to see what the result of this step should look like? Have a look at the Git repository directory here: [step-1-run-a-simple-ml-experiment](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/step-1-run-a-simple-ml-experiment).

## State of the MLOps process

- ❌ The codebase still needs to be downloaded and set up locally in order to run the experiment;
- ❌ The dataset still needs to be downloaded and placed in the right directory in order to run the experiment;
- ❌ The steps used to create the model can be forgotten;
- ❌ The changes done to a model cannot be visualized and improvements and/or deteriorations are hard to identify;
- ❌ There is no guarantee that the experiment can be executed on another machine;
- ❌ The model might have required artifacts that can be forgotten or omitted when saving/loading the model for future usage. There is no easy way to use the model outside of the experiment context.

## Sources

Highly inspired by the [_Get Started: Data Pipelines_ - dvc.org](https://dvc.org/doc/start/data-management/pipelines) guide.

## Next & Previous steps

- **Previous**: [Introduction](/the-guide/introduction)
- **Next**: [Step 2: Share your ML experiment code with Git](/the-guide/step-2-share-your-ml-experiment-code-with-git)
