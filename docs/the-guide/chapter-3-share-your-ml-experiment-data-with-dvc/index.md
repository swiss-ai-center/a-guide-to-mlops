# Chapter 3: Share your ML experiment data with DVC

## Introduction

At this point, the codebase is made available to team members using Git, but the
experiment data is not.

The goal of this chapter is to store the data of the experiment in a version control system.
Git is not suitable for this purpose because of its size limitations.
Git LFS is a solution to this problem, but it is not as efficient as other version control systems.

[DVC](../../get-started/the-tools-used-in-this-guide#dvc) is a version control system for data.
It uses chunking to store large files efficiently and track their changes.
Similar to Git, DVC allows you to store the dataset in a remote storage, typically a cloud storage provider, and track its changes.

In this guide, a Google Storage Bucket will be used to store the dataset.
Although, DVC is compatible with many other cloud storage providers as well.

!!! info

	Want to self-host your storage? Check out the [Deploy
	MinIO](../../advanced-concepts/deploy-minio) guide!

In this chapter, you will learn how to:

1. Create a new project on Google Cloud
2. Install Google Cloud CLI
3. Create the Google Storage Bucket
4. Install DVC
5. Initialize and configure DVC
6. Update the `.gitignore` file and add the experiment data to DVC
7. Push the data files to DVC
8. Push the metadata files to Git

Let's get started!

## Steps

### Create a Google Cloud Project

Create a Google Cloud Project by going to the [Google Cloud
console](https://console.cloud.google.com/), select **Select a project** in the
upper left corner of the screen and select **New project**.

Name your project and select **Create** to create the project.

A new page opens. Note the ID of your project, it will be used later.

!!! warning

	Always make sure you're in the right project by selecting your project with **Select a project** in the upper left corner of the screen.

### Install Google Cloud CLI

To install `gcloud`, follow the official documentation: [_Install the Google
Cloud CLI_ - cloud.google.com](https://cloud.google.com/sdk/docs/install-sdk)

### Initialize and configure Google Cloud CLI 

The following process will authenticate to Google Cloud using the Google Cloud
CLI. It will open a browser window to log you in and create a credentials file
in `~/.config/gcloud/application_default_credentials.json`. This file must not
be shared.

DVC will then automatically use these credentials to authenticate to the cloud
storage provider.

Alternatively, you can set the `GOOGLE_APPLICATION_CREDENTIALS` environment
variable to the path of the credentials file.

Replace `<id of your gcp project>` with your own project ID.

```sh title="Execute the following command(s) in a terminal"
# Initialize and login to Google Cloud
gcloud init

# List all available projects
gcloud projects list

# Select your Google Cloud project
gcloud config set project <id of your gcp project>
```

Then run the following command to authenticate to Google Cloud with the Application Default.

```sh title="Execute the following command(s) in a terminal"
# Set authentication for our ML experiment
# https://dvc.org/doc/command-reference/remote/add#google-cloud-storage
# https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login
gcloud auth application-default login
```

### Create the Google Storage Bucket

To be able to create the bucket, the project must be linked to an active billing account. You can set up the billing account from the main Google Cloud console menu on the top left.

Create the Google Storage Bucket to store the data with the Google Cloud CLI. You should ideally select a location close to where most of the expected traffic will come from. You can view the available regions at [Cloud locations](https://cloud.google.com/about/locations).

Change the `<my bucket name>` to your own bucket name (ex: `mlopsdemo`).

!!! warning

	The bucket name must be unique accross all Google Cloud projects and users.

```sh title="Execute the following command(s) in a terminal"
gcloud storage buckets create gs://<my bucket name> \
	--location=EUROPE-WEST6 \
	--uniform-bucket-level-access \
	--public-access-prevention
```

You now have everything needed for DVC.

### Install DVC

Update the `src/requirements.txt` file to include some additional packages.

Here, the `dvc[gs]` package enables support for Google Cloud Storage.

``` title="src/requirements.txt" hl_lines="1"
dvc[gs]==2.37.0
dvclive==1.0.0
pandas==1.5.1
pyaml==21.10.1
scikit-learn==1.1.3
scipy==1.10.1
matplotlib==3.6.2
```

Check the differences with Git to validate the changes.

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff src/requirements.txt
```

The output should be similar to this.

```diff
diff --git a/src/requirements.txt b/src/requirements.txt
index c8fa80f..ff173a7 100644
--- a/src/requirements.txt
+++ b/src/requirements.txt
@@ -1,3 +1,4 @@
+dvc[gs]==2.37.0
 dvclive==1.0.0
 pandas==1.5.1
 pyaml==21.10.1
```

You can now install the required packages from the `src/requirements.txt` file.

```sh title="Execute the following command(s) in a terminal"
# Install the requirements
pip install --requirement src/requirements.txt
```

### Initialize and configure DVC

Initialize DVC with a Google Storage remote bucket. Replace `<my bucket name>` with your own bucket name. The `dvcstore` is a user-defined path on the bucket. You can change it if needed.

```sh title="Execute the following command(s) in a terminal"
# Initialize DVC in the working directory
dvc init

# Add the Google Storage remote bucket
dvc remote add -d data gs://<my bucket name>/dvcstore
```

The effect of the `dvc init` command is to create a `.dvc` directory in the
working directory. This directory contains the configuration of DVC.

### Update the .gitignore file and add the experiment data to DVC

Now that DVC has been setup, you can add files to DVC.

Try to add the experiment data. Warning, it will fail.

```sh title="Execute the following command(s) in a terminal"
# Try to add the experiment data to DVC
dvc add data/data.xml
```

When executing this command, the following output occurs.

```sh
ERROR: bad DVC file name 'data/data.xml.dvc' is git-ignored.
```

You will have to update the `.gitignore` file so that DVC can create files in
the `data` directory. However, you still don't want the directories
`data/features` and `data/prepared` to be added to Git.

Update the `.gitignore` file by changing `data` to `data/features` and
`data/prepared`.

```sh title="Execute the following command(s) in a terminal" hl_lines="2-3"
# Data used to train the models
data/features
data/prepared

# The models
*.pkl

## Python

# Environments
.venv

# Byte-compiled / optimized / DLL files
__pycache__/
```

Check the differences with Git to validate the changes.

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff .gitignore
```

The output should be similar to this.

```diff
diff --git a/.gitignore b/.gitignore
index f1cbfa9..2b092ce 100644
--- a/.gitignore
+++ b/.gitignore
@@ -1,5 +1,6 @@
 # Data used to train the models
-data
+data/features
+data/prepared
 
 # The models
 *.pkl
```

You can now add the experiment data to DVC without complain!

```sh title="Execute the following command(s) in a terminal"
# Add the experiment data to DVC
dvc add data/data.xml
```

The effect of the `dvc add` command is to create a `data/data.xml.dvc` file and
a `data/.gitignore`. The `.dvc` file contains the metadata of the file that is
used by DVC to download and check the integrity of the files. The `.gitignore`
file is created to add the `data.xml` file to be ignored by Git. The `.dvc`
files must be added to Git.

Various DVC commands will automatically try to update the `.gitignore` files. If a
`.gitignore` file is already present, it will be updated to include the newly
ignored files. You might need to update existing `.gitignore` files accordingly.

### Push the data files to DVC

DVC works as Git. Once you want to share the data, you can use `dvc push` to
upload the data and its cache to the storage provider.

```sh title="Execute the following command(s) in a terminal"
# Upload the experiment data and cache to the remote bucket
dvc push
```

### Check the changes

Check the changes with Git to ensure all wanted files are here.

```sh title="Execute the following command(s) in a terminal"
# Add all the files
git add .

# Check the changes
git status
```

The output of the `git status` command should be similar to this.

```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   .dvc/.gitignore
        new file:   .dvc/config
        new file:   .dvcignore
        modified:   .gitignore
        new file:   data/.gitignore
        new file:   data/README.md
        new file:   data/data.xml.dvc
        modified:   src/requirements.txt
```

### Push the changes to Git

You can now push the changes to Git so all team members can get the data from
DVC as well.

```sh title="Execute the following command(s) in a terminal"
# Commit the changes
git commit -m "My ML experiment data is saved with DVC"

# Push the changes
git push
```

This chapter is done, you can check the summary.

## Summary

Congrats! You now have a dataset that can be used and shared among the team.

In this chapter, you have successfully:

1. Created a new project on Google Cloud
2. Installed Google Cloud CLI
3. Created the Google Storage Bucket
4. Installed DVC
5. Initialized and configuring DVC
6. Updated the `.gitignore` file and adding the experiment data to DVC
7. Pushed the data files to DVC
8. Pushed the metadata files to Git

You fixed some of the previous issues:

- ✅ Data no longer needs manual download and is placed in the right directory.

When used by another member of the team, they can easily get a copy of the
experiment data from DVC with the following command.

```sh title="Execute the following command(s) in a terminal"
# Download experiment data from DVC
dvc pull
```

You can now safely continue to the next chapter.

## State of the MLOps process

- ✅ The codebase can be shared and improved by multiple developers
- ✅ The dataset can be shared among the developers and is placed in the right
  directory in order to run the experiment
- ❌ Model steps rely on verbal communication and may be undocumented
- ❌ Changes to model are not easily visualized
- ❌ Experiment may not be reproducible on other machines
- ❌ Model may have required artifacts that are forgotten or omitted in
  saved/loaded state and there is no easy way to use the model outside of the
  experiment context

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by the [_Get Started_ - dvc.org](https://dvc.org/doc/start),
[_Supported storage types_ - dvc.org
](https://dvc.org/doc/command-reference/remote/add#supported-storage-types)
[_Get Started: Data Versioning_ -
dvc.org](https://dvc.org/doc/start/data-management), [_Install the Google Cloud
CLI_ - cloud.google.com](https://cloud.google.com/sdk/docs/install-sdk),
[_Create storage buckets_ -
cloud.google.com](https://cloud.google.com/storage/docs/creating-buckets) and [_gcloud storage buckets create_ - cloud.google.com](https://cloud.google.com/sdk/gcloud/reference/storage/buckets/create)
guides.

Want to see what the result at the end of this chapter should look like? Have a
look at the Git repository directory here:
[chapter-3-share-your-ml-experiment-data-with-dvc](https://github.com/csia-pme/a-guide-to-mlops/tree/main/docs/the-guide/chapter-3-share-your-ml-experiment-data-with-dvc).
