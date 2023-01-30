---
title: "Step 3: Share your ML experiment data with DVC"
---

# {% $markdoc.frontmatter.title %}

## Summary

{% callout type="note" %}
Highly inspired by the [_Get Started_ - dvc.org](https://dvc.org/doc/start), [_Supported storage types_ - dvc.org
](https://dvc.org/doc/command-reference/remote/add#supported-storage-types) [_Get Started: Data Versioning_ - dvc.org](https://dvc.org/doc/start/data-management), [_Install the Google Cloud CLI_ - cloud.google.com](https://cloud.google.com/sdk/docs/install-sdk) and [_Create storage buckets_ - cloud.google.com](https://cloud.google.com/storage/docs/creating-buckets) guides.
{% /callout %}


The objective of this step is to distribute the experiment data with the team using [DVC](https://dvc.org/). DVC is a version control system for your data. Dataset files are generally too large to be stored in Git. DVC allows you to store the dataset in a remote storage and to version it. DVC also allows you to track the changes done to the dataset and to the codebase.

At this point, the codebase is distrobuted to team members using Git. The point of this step is to distribute the dataset to the team members using DVC.

This will be done in the following steps:

1. Create a Google Storage Bucket to hold the data.
2. Install and configure DVC as a tool to push and pull the data on our newly created bucket.
3. Adapt the .gitignore file to exclude the data from our codebase.


## Requirements

It is required to have a cloud storage for DVC to store the dataset. DVC is compatible with many cloud storage providers.

For this demo, a Google Storage Bucket will be used to store the dataset. The [Google Cloud CLI (`gcloud`)](https://cloud.google.com/sdk/docs/install-sdk) must be installed.

{% callout type="note" %}
Want to self-host your storage? Check out the [Deploy MinIO](/advanced-concepts/deploy-minio) guide!
{% /callout %}

## Instructions

{% callout type="warning" %}
This guide has been written for macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use [GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

#### Create a Google Cloud Project

Create a Google Cloud Project by going to the [Google Cloud console](https://console.cloud.google.com/), select **Select a project** in the upper right corner of the screen and select **New project**.

Name your project (_mlopsdemo_ - The name is unique for all projects on Google Cloud, you might need to choose another one while following this guide) and select **Create**.

#### Setup the Google Cloud CLI

Locally, login to Google Cloud using gcloud and select the project.

```sh
# Initialize and login to Google Cloud
gcloud init

# Set authentication for our ML experiment
# https://dvc.org/doc/command-reference/remote/add#google-cloud-storage
# https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login
gcloud auth application-default login

# List all available projects
gcloud projects list

# Select the `mlopsdemo` project
gcloud config set project <id of the gcp project>
```

#### Create the Google Storage Bucket

Create the Google Storage Bucket by going to **Cloud Storage** on the left sidebar. Select **Create a Bucket**.

- **Bucket Name** : _mlopsdemo_
- **Location type** : _europe-west6 (Zurich)_
- **Default storage class** : _Standard_
- **Enforce public access prevention on this bucket** : _Checked_
- **Access control** : _Uniform_
- **Projection tools** : _None_

Select **Create**.

#### Update the gitignore file

Update the `.gitignore` file to ignore the data files. As previously mentioned, the data files are too large to be stored in Git. 


// TODO ajouter des "steps" pour mieux délimiter les étapes et pouvoir spécifier le but et la cause de chacune
### update gitignore <why>

Update the `.gitignore` file by changing 'data' to 'data/features' and 'data/prepared.

```sh
## Custom experiment

# Data used to train the models
data/features
data/prepared

# The models
*.pkl

# The models evaluations
evaluation

## Python

# Environments
.venv

# Byte-compiled / optimized / DLL files
__pycache__/
```

#### Install DVC.

Update the `src/requirements.txt` file to include the DVC and DVC Google Cloud Storage dependencies.

```
dvc==2.37.0
dvc[gs]==2.37.0
dvclive==1.0.0
pandas==1.5.1
pyaml==21.10.1
scikit-learn==1.1.3
scipy==1.9.3
matplotlib==3.6.2
```

```sh
# Install the new requirements

pip install -r src/requirements.txt
```

#### Initialize and configure DVC.

```sh
# Initialize DVC in the working directory
dvc init

# Add the Google remote storage bucket
dvc remote add -d data gs://mlopsdemo/dvcstore

# Optional: You can enable auto stage DVC files to Git
dvc config core.autostage true
```

DVC logs into Google Cloud using the Google Cloud CLI credentials.

Move the experiment data to DVC.

```sh
# Add the experiment data to DVC
dvc add data/data.xml

# Upload the experiment data and cache to the remote bucket
dvc push
```

DVC automatically adds files to be ignored, such as the ones described in the `data/.gitignore` file.

Push the changes to Git.

```sh
# Add all the files
git add .

# Commit the changes
git commit -m "My ML experiment data is saved with DVC"

# Push the changes
git push
```

Congrats! You now have a dataset that can be used and shared among the team.

When used by another member of the team, they can easily pull the experiment data from DVC.

```sh
# Pull the data from DVC
dvc pull
```

## Check the results

Want to see what the result of this step should look like? Have a look at the Git repository directory here: [step-3-share-your-ml-experiment-data-with-dvc](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/step-3-share-your-ml-experiment-data-with-dvc).

## State of the MLOps process

- ✅ The codebase can be shared among the developers. The codebase can be improved collaboratively;
- ✅ The dataset can be shared among the developers and is placed in the right directory in order to run the experiment;
- ❌ The steps used to create the model can be forgotten;
- ❌ The changes done to a model cannot be visualized and improvements and/or deteriorations are hard to identify;
- ❌ There is no guarantee that the experiment can be executed on another machine;
- ❌ The model might have required artifacts that can be forgotten or omitted when saving/loading the model for future usage. There is no easy way to use the model outside of the experiment context.

## Next & Previous steps

- **Previous**: [Step 2: Share your ML experiment code with Git](/the-guide/step-2-share-your-ml-experiment-code-with-git)
- **Next**: [Step 4: Reproduce the experiment with DVC](/the-guide/step-4-reproduce-the-experiment-with-dvc)
