# Chapter 6: Move the ML experiment data to the cloud

??? info "You want to take over from this chapter? Collapse this section and follow the instructions below."

    _Work in progress._

    [//]: # "TODO"

## Introduction

Now that we have configured DVC and can reproduce the experiment, let's set up a
remote repository for sharing the data with the team.

Similarly to other version control system, DVC allows for storing the dataset in
a remote storage, typically a cloud storage provider, ensuring effective
tracking of modifications and smooth maintenance workflow.

This guide will demonstrate the use of a remote Storage Bucket for storing the
dataset.

In this chapter, you will learn how to:

1. Create a project on the chosen cloud provider
2. Create a storage bucket on the chosen cloud provider
3. Configure DVC for remote storage
4. Push the data files to DVC
5. Commit the metadata files to Git

The following diagram illustrates control flow of the experiment at the end of
this chapter:

```mermaid
flowchart LR
    dot_dvc[(.dvc)] -->|dvc push| s3_storage[(S3 Storage)]
    s3_storage -->|dvc pull| dot_dvc
    dot_git[(.git)]
    workspaceGraph <-....-> dot_git
    data[data/raw] <-.-> dot_dvc
    subgraph remoteGraph[REMOTE]
        s3_storage
    end
    subgraph cacheGraph[CACHE]
        dot_dvc
        dot_git
    end
    subgraph workspaceGraph[WORKSPACE]
        prepare[prepare.py] <-.-> dot_dvc
        train[train.py] <-.-> dot_dvc
        evaluate[evaluate.py] <-.-> dot_dvc
        data --> prepare
        subgraph dvcGraph["dvc.yaml (dvc repro)"]
            prepare --> train
            train --> evaluate
        end
        params[params.yaml] -.- prepare
        params -.- train
        params <-.-> dot_dvc
    end
    style workspaceGraph opacity:0.4,color:#7f7f7f80
    style dvcGraph opacity:0.4,color:#7f7f7f80
    style cacheGraph opacity:0.4,color:#7f7f7f80
    style dot_git opacity:0.4,color:#7f7f7f80
    style prepare opacity:0.4,color:#7f7f7f80
    style train opacity:0.4,color:#7f7f7f80
    style evaluate opacity:0.4,color:#7f7f7f80
    style params opacity:0.4,color:#7f7f7f80
    linkStyle 2 opacity:0.4,color:#7f7f7f80
    linkStyle 4 opacity:0.4,color:#7f7f7f80
    linkStyle 5 opacity:0.4,color:#7f7f7f80
    linkStyle 6 opacity:0.4,color:#7f7f7f80
    linkStyle 7 opacity:0.4,color:#7f7f7f80
    linkStyle 8 opacity:0.4,color:#7f7f7f80
    linkStyle 9 opacity:0.4,color:#7f7f7f80
    linkStyle 10 opacity:0.4,color:#7f7f7f80
    linkStyle 11 opacity:0.4,color:#7f7f7f80
    linkStyle 12 opacity:0.4,color:#7f7f7f80
```

Let's get started!

## Steps

### Create a project on a cloud provider

Create a project on a cloud provider to host the data.

=== ":simple-amazonaws: Amazon Web Services"

    _This is a work in progress._

=== ":simple-exoscale: Exoscale"

    _This is a work in progress._

=== ":simple-googlecloud: Google Cloud"

    Create a Google Cloud Project by going to the
    [Google Cloud console](https://console.cloud.google.com/), select
    **Select a project** in the upper left corner of the screen and select
    **New project**.

    Name your project and select **Create** to create the project.

    A new page opens. Note the ID of your project, it will be used later.

    !!! warning

        Always make sure you're in the right project by selecting your project with
        **Select a project** in the upper left corner of the screen.

    **Export the Google Cloud Project ID**

    Export the Google Cloud Project ID as an environment variable. Replace
    `<id of your gcp project>` with your own project ID.

    ```sh title="Execute the following command(s) in a terminal"
    export GCP_PROJECT_ID=<id of your gcp project>
    ```

=== ":simple-microsoftazure: Microsoft Azure"

    _This is a work in progress._

=== ":simple-kubernetes: Self-hosted Kubernetes"

    _This is a work in progress._

### Install and configure the cloud provider CLI

Install and configure the cloud provider CLI tool to manage the cloud resources.

=== ":simple-amazonaws: Amazon Web Services"

    _This is a work in progress._

=== ":simple-exoscale: Exoscale"

    _This is a work in progress._

=== ":simple-googlecloud: Google Cloud"

    To install `gcloud`, follow the official documentation:
    [_Install the Google Cloud CLI_ - cloud.google.com](https://cloud.google.com/sdk/docs/install-sdk)

    **Initialize and configure the Google Cloud CLI**

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

    Then run the following command to authenticate to Google Cloud with the
    Application Default.

    ```sh title="Execute the following command(s) in a terminal"
    # Set authentication for our ML experiment
    # https://dvc.org/doc/user-guide/data-management/remote-storage/google-cloud-storage
    # https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login
    gcloud auth application-default login
    ```

=== ":simple-microsoftazure: Microsoft Azure"

    _This is a work in progress._

=== ":simple-kubernetes: Self-hosted Kubernetes"

    _This is a work in progress._

### Create the Storage Bucket on the cloud provider

Create the Storage Bucket to store the data with the cloud provider CLI.

!!! info

    On most cloud providers, the project must be linked to an active billing account
    to be able to create the bucket. You must set up a valid billing account for
    your cloud provider.

=== ":simple-amazonaws: Amazon Web Services"

    _This is a work in progress._

=== ":simple-exoscale: Exoscale"

    _This is a work in progress._

=== ":simple-googlecloud: Google Cloud"

    Create the Google Storage Bucket to store the data with the Google Cloud CLI.
    You should ideally select a location close to where most of the expected traffic
    will come from. You can view the available regions at
    [Cloud locations](https://cloud.google.com/about/locations).

    Export the bucket name as an environment variable. Replace `<my bucket name>`
    with your own bucket name (ex: `mlopsdemo`).

    !!! warning

        The bucket name must be unique across all Google Cloud projects and users.
        Change the `<my bucket name>` to your own bucket name.

    ```sh title="Execute the following command(s) in a terminal"
    export GCP_BUCKET_NAME=<my bucket name>
    ```

    Export the bucket region as an environment variable. Replace
    `<my bucket region>` with your own zone. For example, use `EUROPE-WEST6` for
    Switzerland.

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

    ??? info "Getting an 'The billing account for the owning project is disabled in state absent' error? Read this!"

        In case you get a
        **HTTPError 403: The billing account for the owning project is disabled in state absent**
        error, ensure the
        [billing account](https://console.cloud.google.com/billing/linkedaccount) is
        correctly linked to the project.

        In the Google Cloud Interface, go to **Billing** in the main hamburger menu,
        then choose the **My Projects** tab. If billing is *disabled*, then select
        *Change billing* * in the **Actions** menu, and click the **Set Account**
        button.

    You now have everything you need for DVC.

=== ":simple-microsoftazure: Microsoft Azure"

    _This is a work in progress._

=== ":simple-kubernetes: Self-hosted Kubernetes"

    _This is a work in progress._

### Install the DVC Storage plugin

Install the DVC Storage plugin for the chosen cloud provider.

=== ":simple-amazonaws: Amazon Web Services"

    _This is a work in progress._

=== ":simple-exoscale: Exoscale"

    _This is a work in progress._

=== ":simple-googlecloud: Google Cloud"

    Here, the `dvc[gs]` package enables support for Google Cloud Storage. Update the
    `requirements.txt` file.

    ```txt title="requirements.txt" hl_lines="4"
    tensorflow==2.12.0
    matplotlib==3.7.1
    pyyaml==6.0
    dvc[gs]==3.2.2
    ```

    Check the differences with Git to validate the changes.

    ```sh title="Execute the following command(s) in a terminal"
    # Show the differences with Git
    git diff requirements.txt
    ```

    The output should be similar to this.

    ```diff
    diff --git a/requirements.txt b/requirements.txt
    index 193ebac..8ccc2df 100644
    --- a/requirements.txt
    +++ b/requirements.txt
    @@ -1,4 +1,4 @@
    tensorflow==2.12.0
    matplotlib==3.7.1
    pyyaml==6.0
    -dvc==3.2.2
    +dvc[gs]==3.2.2
    ```

    Install the dependencies and update the freeze file.

    !!! warning

        Prior to running any `pip` commands, it is crucial to ensure the virtual
        environment is activated to avoid potential conflicts with system-wide Python
        packages.

        To check its status, simply run `pip -V`. If the virtual environment is active,
        the output will show the path to the virtual environment's Python executable. If
        it is not, you can activate it with `source .venv/bin/activate`.

    ```sh title="Execute the following command(s) in a terminal"
    # Install the requirements
    pip install --requirement requirements.txt

    # Freeze the requirements
    pip freeze --local --all > requirements-freeze.txt
    ```

=== ":simple-microsoftazure: Microsoft Azure"

    _This is a work in progress._

=== ":simple-kubernetes: Self-hosted Kubernetes"

    _This is a work in progress._

### Configure DVC to use the Storage Bucket

Configure DVC to use the Storage Bucket on the chosen cloud provider.

=== ":simple-amazonaws: Amazon Web Services"

    _This is a work in progress._

=== ":simple-exoscale: Exoscale"

    _This is a work in progress._

=== ":simple-googlecloud: Google Cloud"

    Configure DVC to use a Google Storage remote bucket. The `dvcstore` is a
    user-defined path on the bucket. You can change it if needed.

    ```sh title="Execute the following command(s) in a terminal"
    # Add the Google Storage remote bucket
    dvc remote add -d data gs://$GCP_BUCKET_NAME/dvcstore
    ```

=== ":simple-microsoftazure: Microsoft Azure"

    _This is a work in progress._

=== ":simple-kubernetes: Self-hosted Kubernetes"

    _This is a work in progress._

### Check the changes

Check the changes with Git to ensure all wanted files are here.

```sh title="Execute the following command(s) in a terminal"
# Add all the available files
git add .

# Check the changes
git status
```

The output of the `git status` command should be similar to this.

```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
    modified:   .dvc/config
    modified:   requirements-freeze.txt
    modified:   requirements.txt
```

### Push the data files to DVC

DVC works as Git. Once you want to share the data, you can use `dvc push` to
upload the data and its cache to the storage provider.

```sh title="Execute the following command(s) in a terminal"
# Upload the experiment data and cache to the remote bucket
dvc push
```

### Commit the changes to Git

You can now push the changes to Git so all team members can get the data from
DVC as well.

```sh title="Execute the following command(s) in a terminal"
# Commit the changes
git commit -m "My ML experiment data is shared with DVC"
```

### Check the results

Open the Bucket Storage on the cloud provider and check that the data files have
been uploaded.

[//]: # "TODO: Add explanation on how to check the files on the cloud provider, the difference between the data and the cache, and how to download the data from the cloud provider."

## Summary

Congrats! You now have a dataset that can be used and shared among the team.

In this chapter, you have successfully:

1. Created a new project on a chosen cloud provider
2. Installed and configured the cloud provider CLI
3. Created the Storage Bucket on the cloud provider
4. Installed the DVC Storage plugin
5. Configured DVC to use the Storage Bucket
6. Updated the `.gitignore` file and adding the experiment data to DVC
7. Pushed the data files to DVC
8. Commit the changes to Git

You fixed some of the previous issues:

- [x] Data no longer needs manual download and is placed in the right directory.

When used by another member of the team, they can easily get a copy of the
experiment data from DVC with the following command.

```sh title="Execute the following command(s) in a terminal"
# Download experiment data from DVC
dvc pull
```

With the help of DVC, they can also easily reproduce your experiment and, thanks
to caching, only the required steps will be executed.

```sh title="Execute the following command(s) in a terminal"
# Execute the pipeline
dvc repro
```

You can now safely continue to the next chapter.

## State of the MLOps process

- [x] Notebook has been transformed into scripts for production
- [x] Codebase and dataset are versioned
- [x] Steps used to create the model are documented and can be re-executed
- [x] Changes done to a model can be visualized with parameters, metrics and
      plots to identify differences between iterations
- [x] Dataset can be shared among the developers and is placed in the right
      directory in order to run the experiment
- [ ] Codebase requires manual download and setup
- [ ] Experiment may not be reproducible on other machines
- [ ] CI/CD pipeline does not report the results of the experiment
- [ ] Changes to model are not thoroughly reviewed and discussed before
      integration
- [ ] Model may have required artifacts that are forgotten or omitted in
      saved/loaded state
- [ ] Model cannot be easily used from outside of the experiment context
- [ ] Model is not accessible on the Internet and cannot be used anywhere
- [ ] Model requires manual deployment on the cluster
- [ ] Model cannot be trained on hardware other than the local machine

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by:

* [_Supported storage types_ - dvc.org](https://dvc.org/doc/command-reference/remote/add#supported-storage-types)
* [_Install the Google Cloud CLI_ - cloud.google.com](https://cloud.google.com/sdk/docs/install-sdk)
* [_Create storage buckets_ - cloud.google.com](https://cloud.google.com/storage/docs/creating-buckets)
* [_gcloud storage buckets create_ - cloud.google.com](https://cloud.google.com/sdk/gcloud/reference/storage/buckets/create)
