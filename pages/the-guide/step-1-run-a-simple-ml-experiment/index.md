---
title: "Step 1: Run a simple ML experiment"
---

# {% $markdoc.frontmatter.title %}

## Summary

{% callout type="note" %}
Highly inspired by the [Get Started: Data Pipelines](https://dvc.org/doc/start/data-management/pipelines) guide.
{% /callout %}

The purpose of this step is to run a simple ML experiment locally.

The purpose of this ML experiment is to:

- Use 10K posts from StackOverflow
- Mark those that are related to the R programming language with `1`, the others with `0`
- Split all of them into training/testing datasets
- Make bags of words matrixes from the title and the description of all posts
- Train the model to classify the R posts vs. the non-R posts from the training dataset
- Evaluate the performance of the model using the testing dataset
    - Measure the Precision-Recall of the R posts vs. the non-R posts
    - Measure the Receiver operating characteristic of the R posts vs. the non-R posts
    - Measure the most important words characterising the R posts vs. the non-R posts

## Instructions

{% callout type="warning" %}
This guide has been written for macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use a decent terminal ([GitBash](https://gitforwindows.org/) for instance) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

Download the source code for this simple ML experiment.

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
├── params.yaml
└── src
    ├── evaluate.py
    ├── featurization.py
    ├── prepare.py
    ├── requirements.txt
    └── train.py
```


| **File**              | **Description**                                   | **Input**                             | **Output**                                                        |
|-----------------------|---------------------------------------------------|---------------------------------------|-------------------------------------------------------------------|
| `requirements.txt`    | The Python dependencies to run the ML experiment  | -                                     | -                                                                 |
| `params.yaml`         | The parameters to run the ML experiment           | -                                     | -                                                                 |
| `prepare.py`          | Prepare the dataset to run the ML experiment      | The dataset to prepare as an XML file | The prepared data in `data/prepared` directory                    |
| `featurization.py`    | Extract the features from the dataset             | The prepared dataset                  | The extracted features in `data/features` directory               |
| `train.py`            | Train the ML model                                | The extracted features                | The model trained with the dataset                                |
| `evaluate.py`         | Evaluate the ML model                             | The model to evaluate                 | The results of the model evaluation in `evaluation` directory     |

Generate the virtual environment and install the dependencies.

```sh
# Generate the virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the requirements
pip install --requirement src/requirements.txt
```

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

Run the experiment.

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

Congrats! You have now a running experiment. This step is done.

{% callout type="note" %}
Want to see what the result of this step should look like? Have a look at the Git repository directory here: [step-1-run-a-simple-ml-experiment](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/step-1-run-a-simple-ml-experiment)
{% /callout %}

## State of the MLOps process

- The codebase still needs to be downloaded and set up locally in order to run the experiment.
- The dataset still needs to be downloaded and placed in the right directory in order to run the experiment.
- The steps used to create the model can be forgotten.

## Next & Previous steps

- **Previous**: [Introduction](/the-guide/introduction)
- **Next**: [Step 2: Share your ML experiment code with Git](/the-guide/step-2-share-your-ml-experiment-code-with-git)
