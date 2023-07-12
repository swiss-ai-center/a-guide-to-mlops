# Chapter 12: Deploy and access the model on Kubernetes with MLEM

??? info "You want to take over from this chapter? Collapse this section and follow the instructions below."

    _Work in progress._

    [//]: # "TODO"

## Introduction

## Steps

### Create the Kubernetes cluster

In order to deploy the model on Kubernetes, you will need a Kubernetes cluster.
Follow the steps below to create one.

=== ":simple-amazonaws: Amazon Web Services"

	TODO

=== ":simple-googlecloud: Google Cloud"

    **Create a Google Cloud Project**

    !!! info

        If you already have created a Google Cloud Project, you can skip this step.

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

    **Install the Google Cloud CLI**

    !!! info

        If you already have the Google Cloud CLI installed, you can skip this step.

    To install `gcloud`, follow the official documentation:
    [_Install the Google Cloud CLI_ - cloud.google.com](https://cloud.google.com/sdk/docs/install-sdk)

    **Initialize and configure the Google Cloud CLI**

    !!! info

        If you already have configured the Google Cloud CLI, you can skip this step.

    The following process will authenticate to Google Cloud using the Google Cloud
    CLI. It will open a browser window to log you in and create a credentials file
    in `~/.config/gcloud/application_default_credentials.json`. This file must not
    be shared.

    ```sh title="Execute the following command(s) in a terminal"
    # Initialize and login to Google Cloud
    gcloud init

    # List all available projects
    gcloud projects list

    # Select your Google Cloud project
    gcloud config set project $GCP_PROJECT_ID
    ```

    **Enable the Google Kubernetes Engine API**

    You must enable the Google Kubernetes Engine API to create Kubernetes clusters
    on Google Cloud.

    [Enable Google Kubernetes Engine API :octicons-arrow-up-right-16:](https://console.cloud.google.com/flows/  enableapi?apiid=container.googleapis.com){
    .md-button .md-button--primary }

    **Create the Kubernetes cluster**

    Create the Google Kubernetes cluster with the Google Cloud CLI. You should
    ideally select a location close to where most of the expected traffic will come
    from. You can view the available zones at
    [Regions and zones](https://cloud.google.com/compute/docs/regions-zones#available).
    You can view the available types of machine with the
    `gcloud compute machine-types list` command.

    Export the cluster name as an environment variable. Replace `<my cluster name>`
    with your own name (ex: `mlops-kubernetes`).

    ```sh title="Execute the following command(s) in a terminal"
    export GCP_CLUSTER_NAME=<my cluster name>
    ```

    Export the cluster zone as an environment variable. Replace `<my cluster zone>`
    with your own zone (ex: `europe-west6-a` for Switzerland Zurich).

    ```sh title="Execute the following command(s) in a terminal"
    export GCP_CLUSTER_ZONE=<my cluster zone>
    ```

    Create the Kubernetes cluster.

    ```sh title="Execute the following command(s) in a terminal"
    gcloud container clusters create \
    	--machine-type=e2-standard-2 \
    	--num-nodes=2 \
    	--zone=$GCP_CLUSTER_ZONE \
    	$GCP_CLUSTER_NAME
    ```

=== ":simple-microsoftazure: Microsoft Azure"

	TODO

=== ":simple-rancher: Self-hosted Rancher"

	TODO

Install the Kubernetes CLI (kubectl) on your machine.

=== ":simple-amazonaws: Amazon Web Services"

	TODO

=== ":simple-googlecloud: Google Cloud"

	Install kubectl with the Google Cloud CLI.

    ```sh title="Execute the following command(s) in a terminal"
    # Install kubectl with gcloud
    gcloud components install kubectl
    ```

=== ":simple-microsoftazure: Microsoft Azure"

	TODO

=== ":simple-rancher: Self-hosted Rancher"

	TODO

### Validate kubectl can access the Kubernetes cluster

Validate kubectl can access the Kubernetes cluster.

```sh title="Execute the following command(s) in a terminal"
kubectl get namespaces
```

The output should be similar to this.

```
NAME              STATUS   AGE
default           Active   25m
kube-node-lease   Active   25m
kube-public       Active   25m
kube-system       Active   25m
```

### Deploy the model on Kubernetes with MLEM

### Access the model

## Summary

## State of the MLOps process

- [x] Notebook has been transformed into scripts for production
- [x] Codebase and dataset are versioned
- [x] Steps used to create the model are documented and can be re-executed
- [x] Changes done to a model can be visualized with parameters, metrics and
      plots to identify differences between iterations
- [x] Dataset can be shared among the developers and is placed in the right
      directory in order to run the experiment
- [x] Codebase can be shared and improved by multiple developers
- [x] Experiment can be executed on a clean machine with the help of a CI/CD
      pipeline
- [x] Changes to model can be thoroughly reviewed and discussed before
      integrating them into the codebase
- [x] Model can be saved and loaded with all required artifacts for future usage
- [x] Model can be easily used outside of the experiment context
- [x] Model can be accessed from a Kubernetes cluster
- [ ] Model cannot be trained on hardware other than the local machine

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.
