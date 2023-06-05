# Chapter 7: Move the ML experiment code to the cloud


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

### Export the Google Cloud Project ID

Export the Google Cloud Project ID as an environment variable. Replace `<id of your gcp project>` with your own project ID.

```sh title="Execute the following command(s) in a terminal"
export GCP_PROJECT_ID=<id of your gcp project>
```

### Install the Google Cloud CLI

To install `gcloud`, follow the official documentation: [_Install the Google
Cloud CLI_ - cloud.google.com](https://cloud.google.com/sdk/docs/install-sdk)

### Initialize and configure the Google Cloud CLI

The following process will authenticate to Google Cloud using the Google Cloud
CLI. It will open a browser window to log you in and create a credentials file
in `~/.config/gcloud/application_default_credentials.json`. This file must not
be shared.

DVC will then automatically use these credentials to authenticate to the cloud
storage provider.

Alternatively, you can set the `GOOGLE_APPLICATION_CREDENTIALS` environment
variable to the path of the credentials file.

```sh title="Execute the following command(s) in a terminal"
# Initialize and login to Google Cloud
gcloud init

# List all available projects
gcloud projects list

# Select your Google Cloud project
gcloud config set project $GCP_PROJECT_ID
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

Export the bucket name as an environment variable. Replace `<my bucket name>` with your own bucket name (ex: `mlopsdemo`).

!!! warning

    The bucket name must be unique across all Google Cloud projects and users. Change the `<my bucket name>` to your own bucket name.

```sh title="Execute the following command(s) in a terminal"
export GCP_BUCKET_NAME=<my bucket name>
```

Export the bucket region as an environment variable. Replace `<my bucket region>` with your own zone (ex: `EUROPE-WEST6` for Switzerland).

```sh title="Execute the following command(s) in a terminal"
export GCP_BUCKET_REGION=<my bucket region>
```

Create the bucket.

```sh title="Execute the following command(s) in a terminal"
gcloud storage buckets create gs://$GCP_BUCKET_NAME \
    --location=$GCP_BUCKET_REGION \
    --uniform-bucket-level-access \
    --public-access-prevention
```

You now have everything needed for DVC.

### Install DVC Google Storage plugin

Here, the `dvc[gs]` package enables support for Google Cloud Storage.

```sh title="Execute the following command(s) in a terminal"
poetry add "dvc[gs]==2.37.0"
```
Check the differences with Git to validate the changes.

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff pyproject.toml
```

The output should be similar to this.

```diff
diff --git a/pyproject.toml b/pyproject.toml
index 8a57399..ff11768 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -13,6 +13,7 @@ pyaml = "21.10.1"
scikit-learn = "1.1.3"
scipy = "1.10.1"
matplotlib = "3.6.2"
-dvc = {version = "2.37.0"}
+dvc = {version = "2.37.0", extras = ["gs"]}

[build-system]
requires = ["poetry-core"]
```

### Configure DVC

Configure DVC to use a Google Storage remote bucket. The `dvcstore` is a user-defined path on the bucket. You can change it if needed.

```sh title="Execute the following command(s) in a terminal"
# Add the Google Storage remote bucket
dvc remote add -d data gs://$GCP_BUCKET_NAME/dvcstore
```

#### Push the data files to DVC

DVC works as Git. Once you want to share the data, you can use `dvc push` to
upload the data and its cache to the storage provider.

```sh title="Execute the following command(s) in a terminal"
# Upload the experiment data and cache to the remote bucket
dvc push
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

## Summary

Congrats! You now have a dataset that can be used and shared among the team.

In this chapter, you have successfully:

1. Created a new project on Google Cloud
2. Installed Google Cloud CLI
3. Created the Google Storage Bucket
4. Installed DVC Google Storage plugin
5. Configuring DVC for Google Storage
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

!!! bug

    `[TBD]`
