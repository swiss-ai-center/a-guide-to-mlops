# Chapter 1 - Run a simple ML experiment with Jupyter Notebook

## Introduction

You have just joined a new ML team whose goal is to build a model that can
classify text into two categories: "related to R programming language" and "not
related to R programming language".

The data scientists of your team have been working with a Jupyter Notebook that
they promptly share with you. Their dataset consists of 10,000 posts from
StackOverflow.

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
2. Acquire the notebook
3. Obtain the dataset
4. Create a Python environment to run the experiment
5. Launch the experiment locally for the first time

Let's get started!

## Steps

### Set up the project directory

As a new team member, set up a project directory on your computer for this ground
breaking ML experiment. This directory will serve as your working directory for
the duration of the guide.

### Download the notebook

Your colleague provided you the following URL to download an archive containing the Jupyter Notebook for this machine learning experiment.

```sh title="Execute the following command(s) in a terminal"
# Download the archive containing the Jupyter Notebook
wget https://github.com/csia-pme/a-guide-to-mlops/archive/refs/heads/jupyter-notebook.zip -O jupyter-notebook.zip
```

Unzip the Jupyter Notebook into your working directory.

```sh title="Execute the following command(s) in a terminal"
# Extract the Jupyter Notebook
unzip jupyter-notebook.zip

# Move the subdirectory files to the working directory
mv a-guide-to-mlops-jupyter-notebook/* .

# Remove the archive and the directory
rm -r jupyter-notebook.zip a-guide-to-mlops-jupyter-notebook
```

### Download and set up the dataset

Your colleague provided you the following URL to download an archive containing
the dataset for this machine learning experiment.

TODO: Update the branch name once the branch is merged

```sh title="Execute the following command(s) in a terminal"
# Download the archive containing the dataset
wget https://github.com/csia-pme/a-guide-to-mlops/archive/refs/heads/59-data.zip -O data.zip
```

This archive must be decompressed and its contents be moved in the
`data` directory in the working directory of the experiment.

```sh title="Execute the following command(s) in a terminal"
# Extract the dataset
unzip data.zip

# Move the `data.xml` file to the working directory
mv a-guide-to-mlops-59-data/ data/

# Remove the archive and the directory
rm data.zip
```

### Explore the notebook and dataset

Examine the notebook and the dataset to get a better understanding of their contents.

Your working directory should now look like this:

TODO: Update the tree

```yaml hl_lines="2-4"
.
├── data # (1)!
│   ├── README.md
│   └── planet_habitability.csv
├── README.md
├── notebook.ipynb
└── requirements.txt
```

1. This, and all its sub-directory, is new.

### Create the virtual environment

Create the virtual environment and install necessary dependencies in your
working directory using these commands.

```sh
# Create the virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the requirements
pip install --requirement requirements.txt
```

### Run the experiment

Awesome! You now have everything you need to run the experiment: the notebook and
the dataset are in place, the virtual environment is ready; and you're ready to run the experiment for the first
time.

Launch the notebook with the following command.

```sh title="Execute the following command(s) in a terminal"
# Launch the experiment
jupyter-lab notebook.ipynb
```

A browser window should open with the Jupyter Notebook.

Execute each step of the notebook to train the model and evaluate its performance.

TODO: Improve this section

The notebook is useful for the following elements:

- Single file for the entire experiment
- Data visualization
- Presentation of the results

The notebook lacks the following elements:

- Difficult to share with others (no versioning)
- Difficult to reproduce
- Cluttered with previous outputs

Once done, you can close the notebook and shut down the Jupyter server by pressing `++Ctrl+C++` in the terminal.

Exit the virtual environment with the following command.

```sh title="Execute the following command(s) in a terminal"
# Exit the virtual environment
deactivate
```

## Summary

Congratulations! You have successfully reproduced the experiment on your machine.

In this chapter, you have:

1. Created the working directory
2. Acquired the codebase
3. Obtained the dataset
4. Set up a Python environment to run the experiment
5. Executed the experiment locally for the first time

However, you may have identified the following areas for improvement:

- ❌ Notebook still needs manual download
- ❌ Dataset still needs manual download and placement
- ❌ Steps to run the experiment were not documented

In the next chapters, you will enhance the workflow to fix those issues.

## State of the MLOps process

- ❌ Notebook can be run but is not adequate for production
- ❌ Codebase and dataset are not versioned
- ❌ Model steps rely on verbal communication and may be undocumented
- ❌ Changes to model are not easily visualized
- ❌ Dataset requires manual download and placement
- ❌ Codebase requires manual download and setup
- ❌ Experiment may not be reproducible on other machines
- ❌ Changes to model are not thoroughly reviewed and discussed before integration
- ❌ Model may have required artifacts that are forgotten or omitted in saved/loaded state
- ❌ Model cannot be easily used from outside of the experiment context

## Sources
