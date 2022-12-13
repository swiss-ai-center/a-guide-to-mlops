---
title: "Step 3: Share your ML experiment data with DVC"
---

# {% $markdoc.frontmatter.title %}

## Summary

{% callout type="note" %}
Highly inspired by the [_Get Started_ - dvc.org](https://dvc.org/doc/start), [_Supported storage types_ - dvc.org
](https://dvc.org/doc/command-reference/remote/add#supported-storage-types) [_Get Started: Data Versioning_ - dvc.org](https://dvc.org/doc/start/data-management), [_Using service accounts_ - dvc.org](https://dvc.org/doc/user-guide/setup-google-drive-remote#using-service-accounts), [_Install the Google Cloud CLI_ - cloud.google.com](https://cloud.google.com/sdk/docs/install-sdk) and [_Create storage buckets_ - cloud.google.com](https://cloud.google.com/storage/docs/creating-buckets) guides.
{% /callout %}

The purpose of this step is to share the data of the simple ML experiment with the rest of the team using DVC.

## Prerequisites

For this demo, a Google Storage Bucket will be used to store the dataset. The [Google Cloud CLI (`gcloud`)](https://cloud.google.com/sdk/docs/install-sdk) must be installed.

{% callout type="note" %}
Want to self-host your storage? Check out the [Deploy MinIO](/advanced-concepts/deploy-minio) guide!
{% /callout %}

## Instructions

{% callout type="warning" %}
This guide has been written for macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use a decent terminal ([GitBash](https://gitforwindows.org/) for instance) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

Create a Google Cloud Project by going to the [Google Cloud console](https://console.cloud.google.com/), select **Select a project** in the upper right corner of the screen and select **New project**.

Name your project (_mlopsdemo_ - The name is unique for all projects on Google Cloud, you might need to choose another one while following this guide) and select **Create**. Save the project ID, it will be used later.

Create a Google Service Account by going to **IAM & Admin > Service Accounts**  on the left sidebar.

Select **Create Service Account**, name the Service Account Key (_mlopsdemo_) select **Create and continue**, select the _Viewer_ Role, select **Continue** and select **Done**.

Select the newly created service account, select **Keys** and add a new key (JSON format). Save the key under the name `google-service-account-key.json`, it will be used later.

Locally, login to Google Cloud using gcloud and select the project.

```sh
# Initialize and login to Google Cloud
gcloud init

# List all available projects
gcloud projects list

# Select the `mlopsdemo` project
gcloud config set project <id of the gcp project>
```

Create the Google Storage Bucket by going to **Cloud Storage** on the left sidebar. Select **Create a Bucket**.

Name the bucket (_mlopsdemo_), select _europe-west6 (Zurich)_ for the **Location type**, select _Standard_ for the **Default storage class**, check the _Enforce public access prevention on this bucket_ option and select _Uniform_ for the **Access control**, select _None_ for the **Projection tools** and select **Create**.

Update the `.gitignore` file.

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

Install DVC.

```sh
# Install DVC
pip install dvc==2.37.0

# If using Google Cloud Storage, install DVC with Google Cloud Storage support
pip install dvc-gs==2.20.0
```

Initialize and configure DVC.

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

{% callout type="note" %}
Want to see what the result of this step should look like? Have a look at the Git repository directory here: [step-3-share-your-ml-experiment-data-with-dvc](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/step-3-share-your-ml-experiment-data-with-dvc)
{% /callout %}

## State of the MLOps process

- The codebase can be shared among the developers. The codebase can be improved collaboratively.
- The dataset can be shared among the developers and is placed in the right directory in order to run the experiment.
- The steps used to create the model can be forgotten.

## Next & Previous steps

- **Previous**: [Step 2: Share your ML experiment code with Git](/the-guide/step-2-share-your-ml-experiment-code-with-git)
- **Next**: [Step 4: Reproduce the experiment with DVC](/the-guide/step-4-reproduce-the-experiment-with-dvc)
