# Chapter 3.3 - Build and publish the model with BentoML and Docker locally

## Introduction

Serving the model locally is great for testing purposes, but it is not
sufficient for production. In this chapter, you will learn how to build and
publish the model with [BentoML](../tools.md) and [Docker](../tools.md).

This will allow to share the model with others and deploy it on a Kubernetes in
a later chapter.

In this chapter, you will learn how to:

1. Create a BentoML model artifact
2. Containerize the model artifact with BentoML and Docker
3. Test the containerized model artifact by serving it locally with Docker
4. Create a container registry that will serve as your model registry
5. Publish the containerized model artifact Docker image to the container
   registry

The following diagram illustrates the control flow of the experiment at the end
of this chapter:

```mermaid
flowchart TB
    dot_dvc[(.dvc)] <-->|dvc pull
                         dvc push| s3_storage[(S3 Storage)]
    dot_git[(.git)] <-->|git pull
                         git push| gitGraph[Git Remote]
    workspaceGraph <-....-> dot_git
    data[data/raw]
    subgraph cacheGraph[CACHE]
        dot_dvc
        dot_git
        bento_artifact[(Containerized
                        artifact)]
    end
    subgraph remoteGraph[REMOTE]
        s3_storage
        subgraph gitGraph[Git Remote]
            action[Action] <--> |...|repository[(Repository)]
        end
        registry[(Container
                  registry)]
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

        bentoGraph -->|bento build
                       bento containerize| bento_artifact
        bento_model <-.-> dot_dvc
        bento_artifact -->|docker tag
                           docker push| registry
    end
    subgraph browserGraph[BROWSER]
        localhost <--> |docker run|bento_artifact
        localhost <--> |bento serve| fastapi
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

    linkStyle 10 opacity:0.4,color:#7f7f7f80
```

## Steps

### Create a BentoML model artifact

A BentoML model artifact (called "Bento" in the documentation) packages your
model, code, and environment dependencies into a single file. It is the standard
format for saving and sharing ML models.

The BentoML model artifact is described in a `bentofile.yaml` file. It contains
the following information:

- The service filename and class name
- The Python packages required to run the service
- The Docker configuration, such as the Python version to use

Create a new `bentofile.yaml` file in the `src` directory with the following
content:

```yaml title="src/bentofile.yaml"
service: 'serve:CelestialBodiesClassifierService'
include:
  - serve.py
python:
  packages:
    - "tensorflow==2.17.1"
    - "matplotlib==3.9.3"
    - "pillow==11.0.0"
docker:
    python_version: "3.12"
```

Do not forget to include the `serve.py` file in the BentoML model artifact. This
file contains the code to serve the model with FastAPI as you have seen in the
previous chapter.

The `python` section contains the Python packages required to run the service.
It does not contain DVC and other packages to build the model, as they are not
required to run the service.

The `docker` section contains the Python version to use. It is important to
specify the Python version to ensure the service runs correctly.

Now that the `bentofile.yaml` file is created, you can serve the model with the
following command:

```sh title="Execute the following command(s) in a terminal"
# Serve the model
bentoml serve --working-dir src
```

### Build the BentoML model artifact

Before containerizing the BentoML model artifact with Docker, you need to build
it.

A BentoML model artifact can be built with the following command:

```sh title="Execute the following command(s) in a terminal"
# Build the BentoML model artifact
bentoml build src
```

The output should be similar to this:

```text
INFO: Adding current BentoML version to requirements.txt: bentoml==1.3.15
INFO: Locking PyPI package versions.

██████╗ ███████╗███╗   ██╗████████╗ ██████╗ ███╗   ███╗██╗
██╔══██╗██╔════╝████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║██║
██████╔╝█████╗  ██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║██║
██╔══██╗██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║██║
██████╔╝███████╗██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║███████╗
╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚══════╝

Successfully built Bento(tag="celestial_bodies_classifier:v5rlmavw4kahqaav").

Next steps:

* Deploy to BentoCloud:
    $ bentoml deploy celestial_bodies_classifier:v5rlmavw4kahqaav -n ${DEPLOYMENT_NAME}

* Update an existing deployment on BentoCloud:
    $ bentoml deployment update --bento celestial_bodies_classifier:v5rlmavw4kahqaav ${DEPLOYMENT_NAME}

* Containerize your Bento with `bentoml containerize`:
    $ bentoml containerize celestial_bodies_classifier:v5rlmavw4kahqaav

* Push to BentoCloud with `bentoml push`:
    $ bentoml push celestial_bodies_classifier:v5rlmavw4kahqaav
```

All Bentos can be listed with the following command:

```sh title="Execute the following command(s) in a terminal"
# List all BentoML model artifacts
bentoml list
```

The output should be similar to this:

```text
 Tag                                           Size       Model Size  Creation Time
 celestial_bodies_classifier:v5rlmavw4kahqaav  18.88 KiB  9.43 MiB    2024-12-10 11:37:00
```

### Containerize the BentoML model artifact with Docker

Now that the BentoML model artifact is built, you can containerize it with the
following command:

```sh title="Execute the following command(s) in a terminal"
# Containerize the BentoML model artifact with Docker
bentoml containerize celestial_bodies_classifier:latest --image-tag celestial-bodies-classifier:latest
```

The first `:latest` is the tag of the BentoML model artifact. It is a symlink to
the latest version of the BentoML model artifact.

The output should be similar to this:

```text
INFO: Building OCI-compliant image for celestial_bodies_classifier:v5rlmavw4kahqaav with docker

[+] Building 57.1s (17/17) FINISHED                                                                      docker:default
 => [internal] load build definition from Dockerfile                                                               0.1s
 => => transferring dockerfile: 1.92kB                                                                             0.0s
 => [internal] load metadata for docker.io/library/python:3.12-slim                                                2.3s
 => [internal] load .dockerignore                                                                                  0.0s
 => => transferring context: 2B                                                                                    0.0s
 => [base-container  1/12] FROM docker.io/library/python:3.12-slim@sha256:2b0079146a74e23bf4ae8f6a28e1b484c6292f6  3.6s
 => => resolve docker.io/library/python:3.12-slim@sha256:2b0079146a74e23bf4ae8f6a28e1b484c6292f6fb904cbb51825b4a1  0.0s
 => => sha256:bc0965b23a04fe7f2d9fb20f597008fcf89891de1c705ffc1c80483a1f098e4f 28.23MB / 28.23MB                   1.2s
 => => sha256:9b871d410cbf35a95adbe8c061f6d60e2e129bd2fd9b60485a8dd397ee3fcf61 3.32MB / 3.32MB                     1.1s
 => => sha256:8bfa778b5b231c44fb4d35b4783fe69f55f2b3f59dad4c8205661c3f752494a6 13.65MB / 13.65MB                   1.6s
 => => sha256:2b0079146a74e23bf4ae8f6a28e1b484c6292f6fb904cbb51825b4a19812fcd8 9.12kB / 9.12kB                     0.0s
 => => sha256:027e90762c20461da8dc5f530b0ca8604b38c382dadacb4471ea47377c7cf951 1.75kB / 1.75kB                     0.0s
 => => sha256:3ebf71e888419589c6cda9e15384dc2bff81338fb591f54af96ca5529df597c2 5.17kB / 5.17kB                     0.0s
 => => sha256:258b25b9265525eaafd659e18f862525eea9e6379dce2ef29defd91ba0b8868c 249B / 249B                         1.4s
 => => extracting sha256:bc0965b23a04fe7f2d9fb20f597008fcf89891de1c705ffc1c80483a1f098e4f                          1.3s
 => => extracting sha256:9b871d410cbf35a95adbe8c061f6d60e2e129bd2fd9b60485a8dd397ee3fcf61                          0.1s
 => => extracting sha256:8bfa778b5b231c44fb4d35b4783fe69f55f2b3f59dad4c8205661c3f752494a6                          0.6s
 => => extracting sha256:258b25b9265525eaafd659e18f862525eea9e6379dce2ef29defd91ba0b8868c                          0.0s
 => [internal] load build context                                                                                  0.1s
 => => transferring context: 9.91MB                                                                                0.0s
 => [base-container  2/12] RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Pa  0.5s
 => [base-container  3/12] RUN --mount=type=cache,target=/var/lib/apt --mount=type=cache,target=/var/cache/apt s  11.6s
 => [base-container  4/12] RUN curl -LO https://astral.sh/uv/install.sh &&     sh install.sh && rm install.sh &&   2.8s
 => [base-container  5/12] RUN groupadd -g 1034 -o bentoml && useradd -m -u 1034 -g 1034 -o -r bentoml             0.5s
 => [base-container  6/12] RUN mkdir /home/bentoml/bento && chown bentoml:bentoml /home/bentoml/bento -R           0.5s
 => [base-container  7/12] WORKDIR /home/bentoml/bento                                                             0.1s
 => [base-container  8/12] COPY --chown=bentoml:bentoml ./env/python ./env/python/                                 0.2s
 => [base-container  9/12] RUN --mount=type=cache,target=/root/.cache/uv bash -euxo pipefail /home/bentoml/bento  29.7s
 => [base-container 10/12] COPY --chown=bentoml:bentoml . ./                                                       0.1s
 => [base-container 11/12] RUN rm -rf /var/lib/{apt,cache,log}                                                     0.2s
 => [base-container 12/12] RUN chmod +x /home/bentoml/bento/env/docker/entrypoint.sh                               0.7s
 => exporting to image                                                                                             4.1s
 => => exporting layers                                                                                            4.1s
 => => writing image sha256:09a34e0dd539e44331537b8ddb316e8b02e0a2c01d1d760ac225bed9ee1af6b0                       0.0s
 => => naming to docker.io/library/celestial-bodies-classifier:latest                                              0.0s

 1 warning found (use docker --debug to expand):
 - FromAsCasing: 'as' and 'FROM' keywords' casing do not match (line 6)
Successfully built Bento container for "celestial_bodies_classifier:latest" with tag(s)
"celestial-bodies-classifier:latest"
To run your newly built Bento container, run:
    docker run --rm -p 3000:3000 celestial-bodies-classifier:latest
```

### Test the containerized BentoML model artifact locally

The BentoML model artifact is now containerized. To verify its behavior, serve
the model artifact locally by running the Docker image:

```sh title="Execute the following command(s) in a terminal"
# Run the Docker image
docker run --rm -p 3000:3000 celestial-bodies-classifier:latest
```

Congrats! You have successfully containerized the BentoML model artifact using
Docker. You have also tested the container by running it locally. The model is
now ready to be shared on a container registry.

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
    `<my_repository_name>` with a registy name of your choice. It has to be
    lowercase and words separated by hyphens.

    !!! warning

        The container registry name must be **unique** across all Google Cloud projects
        and users. For example, use `mlops-<surname>-registry`, where `surname` is based
        on your name. Change the container registry name if the command fails.

    ```sh title="Execute the following command(s) in a terminal"
    export GCP_CONTAINER_REGISTRY_NAME=<my_repository_name>
    ```

    Export the repository location as an environment variable. You can view the
    available locations at
    [Cloud locations](https://cloud.google.com/about/locations). You should ideally
    select a location close to where most of the expected traffic will come from.
    Replace `<my_repository_location>` with your own zone. For example, use
    `europe-west6` for Switzerland (Zurich):

    ```sh title="Execute the following command(s) in a terminal"
    export GCP_CONTAINER_REGISTRY_LOCATION=<my_repository_location>
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
    Create request issued for: [mlops-surname-registry]
    Waiting for operation [projects/mlops-surname-project/locations/europe-west6/operations/be8b09fa-279c-468
    5-b451-1f3c900d4a36] to complete...done.
    Created repository [mlops-surname-registry].
    ```

=== ":material-cloud: Using another cloud provider? Read this!"

    This guide has been written with Google Cloud in mind. We are open to
    contributions to add support for other cloud providers such as
    [:simple-amazonwebservices: Amazon Web Services](https://aws.amazon.com),
    [:simple-exoscale: Exoscale](https://www.exoscale.com),
    [:material-microsoft-azure: Microsoft Azure](https://azure.microsoft.com) or
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
        PROJECT_ID             NAME                   PROJECT_NUMBER
        mlops-surname-project  mlops-surname-project  123456789012
        ```

        Copy the `PROJECT_ID` and export it as an environment variable. Replace
        `<my_project_id>` with your own project ID:

        ```sh title="Execute the following command(s) in a terminal"
        export GCP_PROJECT_ID=<my_project_id>
        ```

=== ":material-cloud: Using another cloud provider? Read this!"

    This guide has been written with Google Cloud in mind. We are open to
    contributions to add support for other cloud providers such as
    [:simple-amazonwebservices: Amazon Web Services](https://aws.amazon.com),
    [:simple-exoscale: Exoscale](https://www.exoscale.com),
    [:material-microsoft-azure: Microsoft Azure](https://azure.microsoft.com) or
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

Open the container registry interface on the cloud provider and check that the
artifact files have been uploaded.

=== ":simple-googlecloud: Google Cloud"

    Open the [Artifact Registry](https://console.cloud.google.com/artifacts) on the
    Google cloud interface and click on your registry to access the details.

=== ":material-cloud: Using another cloud provider? Read this!"

    This guide has been written with Google Cloud in mind. We are open to
    contributions to add support for other cloud providers such as
    [:simple-amazonwebservices: Amazon Web Services](https://aws.amazon.com),
    [:simple-exoscale: Exoscale](https://www.exoscale.com),
    [:material-microsoft-azure: Microsoft Azure](https://azure.microsoft.com) or
    [:simple-kubernetes: Self-hosted Kubernetes](https://kubernetes.io) but we might
    not officially support them.

    If you want to contribute, please open an issue or a pull request on the
    [GitHub repository](https://github.com/swiss-ai-center/a-guide-to-mlops). Your
    help is greatly appreciated!

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
- [ ] Model requires manual publication to the artifact registry
- [ ] Model is accessible from the Internet and can be used anywhere
- [ ] Model requires manual deployment on the cluster
- [ ] Model cannot be trained on hardware other than the local machine
- [ ] Model cannot be trained on custom hardware for specific use-cases

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by:

- [_Connecting a repository to a package_ - docs.github.com](https://docs.github.com/en/packages/learn-github-packages/connecting-a-repository-to-a-package)
- [_Working with the Container registry_ - docs.github.com](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [_Containerization_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/guides/containerization.html)
- [_Build options_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/guides/build-options.html)
