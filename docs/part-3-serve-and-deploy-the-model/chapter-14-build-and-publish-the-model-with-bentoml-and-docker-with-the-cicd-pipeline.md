# Chapter 14 - Build and publish the model with BentoML and Docker in the CI/CD pipeline

## Introduction

Serving the model locally is great for testing purposes, but it is not
sufficient for production. In this chapter, you will learn how to build and
publish the model with [BentoML](../tools.md) and [Docker](../tools.md).

This will allow to share the model with others and deploy it on a Kubernetes in
a later chapter.

In this chapter, you will learn how to:

1. Create a container registry that will serve as your model registry
2. Publish the containerized model artifact Docker image to the container
   registry


The following diagram illustrates control flow of the experiment at the end of
this chapter:

```mermaid
flowchart TB
    dot_dvc[(.dvc)] <-->|dvc pull\ndvc push| s3_storage[(S3 Storage)]
    dot_git[(.git)] <-->|git pull\ngit push| gitGraph[Git Remote]
    workspaceGraph <-....-> dot_git
    data[data/raw]
    subgraph cacheGraph[CACHE]
        dot_dvc
        dot_git
        bento_artifact[(Containerized\nartifact)]
    end
    subgraph remoteGraph[REMOTE]
        s3_storage
        subgraph gitGraph[Git Remote]
            repository[(Repository)] --> action[Action]
            action[Action] --> |...|request[PR]
            request --> repository[(Repository)]
        end
        registry[(Container\nregistry)]
    end
    subgraph workspaceGraph[WORKSPACE]
        data --> code[*.py]
        subgraph dvcGraph["dvc.yaml"]
            code
        end
        params[params.yaml] -.- code
        code <--> bento_model[classifier.bentomodel]
        subgraph bentoGraph[bentofile.yaml]
            bento_model
            serve[serve.py] <--> bento_model
            fastapi[FastAPI] <--> |bento serve|serve
        end

        bentoGraph -->|bento build\nbento containerize| bento_artifact
        bento_model <-.-> dot_dvc
        bento_artifact -->|docker push| registry
    end

    style workspaceGraph opacity:0.4,color:#7f7f7f80
    style dvcGraph opacity:0.4,color:#7f7f7f80
    style cacheGraph opacity:0.4,color:#7f7f7f80
    style data opacity:0.4,color:#7f7f7f80
    style dot_git opacity:0.4,color:#7f7f7f80
    style dot_dvc opacity:0.4,color:#7f7f7f80
    style code opacity:0.4,color:#7f7f7f80
    style serve opacity:0.4,color:#7f7f7f80
    style bento_model opacity:0.4,color:#7f7f7f80
    style fastapi opacity:0.4,color:#7f7f7f80
    style params opacity:0.4,color:#7f7f7f80
    style s3_storage opacity:0.4,color:#7f7f7f80
    style repository opacity:0.4,color:#7f7f7f80
    style action opacity:0.4,color:#7f7f7f80
    style request opacity:0.4,color:#7f7f7f80
    style remoteGraph opacity:0.4,color:#7f7f7f80
    style gitGraph opacity:0.4,color:#7f7f7f80
    linkStyle 0 opacity:0.4,color:#7f7f7f80
    linkStyle 1 opacity:0.4,color:#7f7f7f80
    linkStyle 2 opacity:0.4,color:#7f7f7f80
    linkStyle 3 opacity:0.4,color:#7f7f7f80
    linkStyle 4 opacity:0.4,color:#7f7f7f80
    linkStyle 5 opacity:0.4,color:#7f7f7f80
    linkStyle 6 opacity:0.4,color:#7f7f7f80
    linkStyle 7 opacity:0.4,color:#7f7f7f80
    linkStyle 8 opacity:0.4,color:#7f7f7f80
    linkStyle 9 opacity:0.4,color:#7f7f7f80
    linkStyle 10 opacity:0.4,color:#7f7f7f80
    linkStyle 12 opacity:0.4,color:#7f7f7f80
```


## Steps

### Create a container registry

A container registry is a crucial component that provides a centralized system
to manage Docker images. It serves as a repository for storing, versioning, and
tracking Docker models built with BentoML, as each version comes with essential
metadata, including training data, hyperparameters, and performance metrics.

This comprehensive information ensures reproducibility by preserving historical
model versions, which aids in debugging and auditing. Additionally, it promotes
transparency and simplifies model comparison and selection for deployment,
allowing for seamless integration into production environments.

The model registry also facilitates collaboration among team members, enabling
standardized model formats and easy sharing of access. Its support for automated
deployment pipelines ensures consistent and reliable model deployment, allowing
for an efficient models management.

=== ":simple-googlecloud: Google Cloud"

    To improve the deployment process on the Kubernetes server, you will use Google
    Artifact Registry as the ML model registry to publish and pull Docker images.

    **Enable the Google Artifact Registry API**

    You must enable the Google Artifact Registry API to create a container registry
    on Google Cloud with the following command:

    !!! tip

        You can display the available services in your project with the following
        command:

        ```sh title="Execute the following command(s) in a terminal"
        # List the services
        gcloud services list
        ```

    ```sh title="Execute the following command(s) in a terminal"
    # Enable the Google Artifact Registry API
    gcloud services enable artifactregistry.googleapis.com
    ```

    **Create the Google Container Registry**

    Export the repository name as an environment variable. Replace
    `<my repository name>` with a registy name of your choice. It has to be
    lowercase and words separated by hyphens. For example, use `mlops-registry` for
    the registry name:

    !!! warning

        The container registry name must be unique across all Google Cloud projects and
        users. Change the container registry name if the command fails.

    ```sh title="Execute the following command(s) in a terminal"
    export GCP_CONTAINER_REGISTRY_NAME=<my repository name>
    ```

    Export the repository location as an environment variable. You can view the
    available locations at
    [Cloud locations](https://cloud.google.com/about/locations). You should ideally
    select a location close to where most of the expected traffic will come from.
    Replace `<my repository location>` with your own zone. For example, use
    `europe-west6` for Switzerland (Zurich):

    ```sh title="Execute the following command(s) in a terminal"
    export GCP_CONTAINER_REGISTRY_LOCATION=<my repository location>
    ```

    Lastly, when creating the repository, remember to specify the repository format
    as `docker`.

    ```sh title="Execute the following command(s) in a terminal"
    # Create the Google Container Registry
    gcloud artifacts repositories create $GCP_CONTAINER_REGISTRY_NAME \
        --repository-format=docker \
        --location=$GCP_CONTAINER_REGISTRY_LOCATION
    ```

    The output should be similar to this:

    ```text
    Create request issued for: [mlops-registry]
    Waiting for operation [projects/mlops-code-395207/locations/europe-west6/operations/be8b09fa-279c-468
    5-b451-1f3c900d4a36] to complete...done.
    Created repository [mlops-registry].
    ```

=== ":material-cloud: Using another cloud provider? Read this!"

    This guide has been written with Google Cloud in mind. We are open to
    contributions to add support for other cloud providers such as
    [:simple-amazonaws: Amazon Web Services](https://aws.amazon.com),
    [:simple-exoscale: Exoscale](https://www.exoscale.com),
    [:simple-microsoftazure: Microsoft Azure](https://azure.microsoft.com) or
    [:simple-kubernetes: Self-hosted Kubernetes](https://kubernetes.io) but we might
    not officially support them.

    If you want to contribute, please open an issue or a pull request on the
    [GitHub repository](https://github.com/csia-pme/csia-pme). Your help is greatly
    appreciated!

### Login to the remote Container Registry

=== ":simple-googlecloud: Google Cloud"

    **Authenticate with the Google Container Registry**

    Configure gcloud to use the Google Container Registry as a Docker credential
    helper.

    ```sh title="Execute the following command(s) in a terminal"
    # Authenticate with the Google Container Registry
    gcloud auth configure-docker ${GCP_CONTAINER_REGISTRY_LOCATION}-docker.pkg.dev
    ```

    Press ++y++ to validate the changes.

    Export the container registry host:

    ```sh title="Execute the following command(s) in a terminal"
    export GCP_CONTAINER_REGISTRY_HOST=${GCP_CONTAINER_REGISTRY_LOCATION}-docker.pkg.dev/${GCP_PROJECT_ID}/${GCP_CONTAINER_REGISTRY_NAME}
    ```

    !!! tip

        To get the ID of your project, you can use the Google Cloud CLI.

        ```sh title="Execute the following command(s) in a terminal"
        # List the projects
        gcloud projects list
        ```

        The output should be similar to this:

        ```text
        PROJECT_ID             NAME            PROJECT_NUMBER
        mlops-workshop-396007  mlops-workshop  475307267926
        ```

        Copy the PROJECT_ID and export it as an environment variable. Replace
        `<id of your gcp project>` with your own project ID:

        ```sh title="Execute the following command(s) in a terminal"
        export GCP_PROJECT_ID=<id of your gcp project>
        ```

=== ":material-cloud: Using another cloud provider? Read this!"

    This guide has been written with Google Cloud in mind. We are open to
    contributions to add support for other cloud providers such as
    [:simple-amazonaws: Amazon Web Services](https://aws.amazon.com),
    [:simple-exoscale: Exoscale](https://www.exoscale.com),
    [:simple-microsoftazure: Microsoft Azure](https://azure.microsoft.com) or
    [:simple-kubernetes: Self-hosted Kubernetes](https://kubernetes.io) but we might
    not officially support them.

    If you want to contribute, please open an issue or a pull request on the
    [GitHub repository](https://github.com/csia-pme/csia-pme). Your help is greatly
    appreciated!

### Publish the BentoML model artifact Docker image to the container registry

The BentoML model artifact Docker image can be published to the container
registry with the following commands:

```sh title="Execute the following command(s) in a terminal"
# Tag the local BentoML model artifact Docker image with the remote container registry host
docker tag celestial-bodies-classifier:latest $GCP_CONTAINER_REGISTRY_HOST/celestial-bodies-classifier:latest

# Push the BentoML model artifact Docker image to the container registry
docker push $GCP_CONTAINER_REGISTRY_HOST/celestial-bodies-classifier:latest
```

The image is now available in the container registry. You can use it from
anywhere using Docker or Kubernetes.

### Check the changes

Check the changes with Git to ensure that all the necessary files are tracked:

```sh title="Execute the following command(s) in a terminal"
# Add all the files
git add .

# Check the changes
git status
```

The output should look similar to this:

```text
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
(use "git restore --staged <file>..." to unstage)
    new file:   src/bentofile.yaml
```

### Commit the changes to Git

Commit the changes to Git.

```sh title="Execute the following command(s) in a terminal"
# Commit the changes
git commit -m "BentoML can be used to containerize the model artifact"

# Push the changes
git push
```

## Summary

Congratulations! You have successfully prepared the model for deployment in a
production environment.

In this chapter, you have successfully:

1. Created and containerized a BentoML model artifact
2. Published the BentoML model artifact Docker image to the container registry

## State of the MLOps process

- [x] Notebook has been transformed into scripts for production
- [x] Codebase and dataset are versioned
- [x] Steps used to create the model are documented and can be re-executed
- [x] Changes done to a model can be visualized with parameters, metrics and
      plots to identify differences between iterations
- [x] Codebase can be shared and improved by multiple developers
- [x] Dataset can be shared among the developers and is placed in the right
      directory in order to run the experiment
- [x] Experiment can be executed on a clean machine with the help of a CI/CD
      pipeline
- [x] CI/CD pipeline is triggered on pull requests and reports the results of
      the experiment
- [x] Changes to model can be thoroughly reviewed and discussed before
      integrating them into the codebase
- [x] Model can be saved and loaded with all required artifacts for future usage
- [x] Model can be easily used outside of the experiment context
- [ ] Model is accessible from the Internet and can be used anywhere
- [ ] Model requires manual deployment on the cluster
- [ ] Model cannot be trained on hardware other than the local machine

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by:

- [_Connecting a repository to a package_ - docs.github.com](https://docs.github.com/en/packages/learn-github-packages/connecting-a-repository-to-a-package)
- [_Working with the Container registry_ - docs.github.com](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [_Containerization_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/guides/containerization.html)
- [_Build options_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/guides/build-options.html)
