# Chapter 17 - Train the model on a Kubernetes pod

## Introduction

!!! warning

    This chapter is a work in progress. It focuses for now solely on :simple-github:
    GitHub.

    Please check back later for updates specific to using :simple-gitlab: GitLab.
    Thank you!

Some experiments can require specific hardware to run. For example, you may need
a GPU to train a deep learning model.

Training these experiments locally can be challenging. You may not have the
required hardware, or you may not want to use your local machine for training.
In this case, you can use a specialized Kubernetes pod to train your model.

In this chapter, you will learn how to:

1. Create a self-hosted runner Docker container image
2. Publish the containerized runner image to the container registry
3. Configure the CI/CD to start the containerized runner on Kubernetes
4. Start the training of the model from your CI/CD pipeline on the Kubernetes
   cluster

The following diagram illustrates the control flow of the experiment at the end
of this chapter:

```mermaid
graph TB
    dot_dvc[(.dvc)] <-->|dvc pull
                         dvc push| s3_storage[(S3 Storage)]
    dot_git[(.git)] <-->|git pull
                         git push| repository[(Repository)]
    workspaceGraph <-....-> dot_git
    base_runner_artifact <-->|docker push| registry_docker[(GH Container
                                                    registry)]
    data[data/raw]
    subgraph cacheGraph[CACHE]
        dot_dvc
        dot_git
        base_runner_artifact[(Containerized
                        base runner)]
    end

    subgraph workspaceGraph[WORKSPACE]
        subgraph runnerBase[base runner]
            direction TB
            Dockerfile <--> startup.sh
        end
        runnerBase --> |docker build| base_runner_artifact
        data --> code[*.py]
        subgraph dvcGraph["dvc.yaml"]
            code
        end
        params[params.yaml] -.- code
        code <--> bento_model[classifier.bentomodel]
        subgraph bentoGraph[bentofile.yaml]
            bento_model
            serve[serve.py] <--> bento_model
        end
        bento_model <-.-> dot_dvc
    end

    subgraph remoteGraph[REMOTE]
        registry_docker[(GH Container
                  registry)]
        s3_storage
        subgraph gitGraph[Git Remote]
            repository --> action[Action]
        end
        registry[(Container
                  registry)]
        action --> |bentoml build
                    bentoml containerize
                    docker push|registry
        s3_storage --> |...|repository
        subgraph clusterGraph[Kubernetes]
            subgraph clusterPodGraph[Kubernetes Pod]
                pod_runner[Runner] -->|dvc pull
                                       dvc repro| pod_train[Train stage]
                k8s_gpu[GPUs] -.-> pod_train
            end
            bento_service_cluster[classifier.bentomodel] --> k8s_fastapi[FastAPI]
        end
        action --> |runner|pod_runner
        pod_train -->|dvc push| s3_storage
        registry --> bento_service_cluster
        action --> |kubectl apply|bento_service_cluster
    end

    subgraph browserGraph[BROWSER]
        k8s_fastapi <--> publicURL["public URL"]
    end

    style workspaceGraph opacity:0.4,color:#7f7f7f80
    style dvcGraph opacity:0.4,color:#7f7f7f80
    style cacheGraph opacity:0.4,color:#7f7f7f80
    style data opacity:0.4,color:#7f7f7f80
    style dot_git opacity:0.4,color:#7f7f7f80
    style dot_dvc opacity:0.4,color:#7f7f7f80
    style code opacity:0.4,color:#7f7f7f80
    style bentoGraph opacity:0.4,color:#7f7f7f80
    style serve opacity:0.4,color:#7f7f7f80
    style bento_model opacity:0.4,color:#7f7f7f80
    style params opacity:0.4,color:#7f7f7f80
    style remoteGraph opacity:0.4,color:#7f7f7f80
    style gitGraph opacity:0.4,color:#7f7f7f80
    style repository opacity:0.4,color:#7f7f7f80
    style bento_service_cluster opacity:0.4,color:#7f7f7f80
    style registry opacity:0.4,color:#7f7f7f80
    style clusterGraph opacity:0.4,color:#7f7f7f80
    style k8s_fastapi opacity:0.4,color:#7f7f7f80
    style browserGraph opacity:0.4,color:#7f7f7f80
    style publicURL opacity:0.4,color:#7f7f7f80
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
    linkStyle 13 opacity:0.4,color:#7f7f7f80
    linkStyle 16 opacity:0.4,color:#7f7f7f80
    linkStyle 17 opacity:0.4,color:#7f7f7f80
    linkStyle 18 opacity:0.4,color:#7f7f7f80
```

## Steps

### Configure hardened security

Jobs in a CI/CD workflow are executed on applications known as runners. These
can be physical servers, virtual machines, or container images, and may operate
on a public cloud, like the runner used for our workflow so far, or on-premises
within your own infrastructure.

We will create a custom container image for a self-hosted runner and deploy it
on our Kubernetes cluster.

It is important to understand that using a self-hosted runner allows other users
to execute code on your infrastructure. Specifically, forks of your public
repository will trigger the workflow when a pull request is created.

Consequently, other users can potentially run malicious code on your self-hosted
runner machine by executing a workflow.

While our self-hosted runner will be set up in a containerized, isolated
environment that limits the impact of any malicious code, unwanted pull requests
in forks could still exhaust the computational resources for which you are
responsible.

To mitigate these risks, it is advisable to secure your runner by disabling
workflow triggers by forks.

In the repository, go to **Settings > Actions > General**. In the
**Fork pull request workflows** section, disable
**Run workflows from fork pull requests** and click on **Save**.

!!! danger

    Creating a self-hosted runner allows other users to execute code on your
    infrastructure. Make sure to secure your runner and restrict access to the
    repository. For more information, see
    [Self-hosted runner security](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners#self-hosted-runner-security).

    More generally, it is recommended that you only use self-hosted runners with
    private repositories.

    If not already done, you can change the repository visibility in
    **Settings > General**. In the **Danger Zone** section, choose
    **Change visibility** and set the repository to **private**.

### Create a self-hosted runner container image

We will create a custom container image for a self-hosted runner and deploy it
on our Kubernetes cluster. This base runner listens for jobs from GitHub
Actions. When asked to, it creates specialized GPU runner pods on the Kubernetes
cluster to execute the jobs. This specialized runner will then be destroyed.

!!! note

    For our small experiment, there is actually no need to have a GPU to train the
    model. This is done solely for demonstration purposes. In a real-life production
    setup with a larger machine learning experiment, however, training with a GPU is
    likely to be a strong requirement due to the increased computational demands and
    the need for faster processing times.

This approach can also be easily adapted to run on a on-premises Kubernetes
cluster.

#### Create the base runner files

The runner uses a custom Docker image that includes the necessary dependencies
to run the workflows.

At the root level of your Git repository, create a `docker` folder.

The following table describes the files that you will create in this folder:

| **File**          | **Description**                                    | *Role**                                       |
| ----------------- | -------------------------------------------------- | --------------------------------------------- |
| `Dockerfile`      | Instructions for building a Docker container image | Package runner files and dependencies         |
| `startup.sh`      | The entrypoint for the Docker image                | Initialize the docker container when launched |

The `Dockerfile` provides the instructions needed to create a custom Docker
container image that incorporates the
[GitHub Actions runner](https://github.com/actions/runner) along with the
workflow files and all its necessary dependencies.

Replace `<my_repository_url>` with your own repository name.

```yaml title="docker/Dockerfile"
FROM ubuntu:24.04

ENV RUNNER_VERSION=2.319.1

LABEL RunnerVersion=${RUNNER_VERSION}
LABEL org.opencontainers.image.source="<my_repository_url>"

# Install dependencies
RUN apt-get update -y && \
    apt-get install -y build-essential lsb-release python3 python3-pip \
    curl jq vim gpg wget git unzip tar gettext-base

# Add a non-root user
RUN useradd -m runner

WORKDIR /home/actions-runner

# Install GitHub Actions Runner
RUN curl -o actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz -L https://github.com/actions/runner/releases/download/v${RUNNER_VERSION}/actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz
RUN tar xzf ./actions-runner-linux-x64-${RUNNER_VERSION}.tar.gz

# Install extra dependencies for the runner
RUN ./bin/installdependencies.sh

COPY startup.sh .

RUN chmod +x startup.sh

USER runner

ENTRYPOINT ["./startup.sh"]
```

This `startup.sh` script will act as an entrypoint for the Docker image. It will
be used to initialize our Docker container when launched from the image we are
creating. The primary purpose of this script is to register a new self-hosted
GitHub runner instance for our repository, each time a new container is started
from the image.

Replace `<my_username>` and `<my_repository_name>` with your own username and
repository name.

```yaml title="docker/startup.sh"
#!/bin/bash

set -e  # Exit on error

REPOSITORY_OWNER=<my_username>
REPOSITORY_NAME=<my_repository_name>

# Set the runner token (expires after 1 hour)
set_token() {
    REG_TOKEN=$(curl -s -X POST -H "Accept: application/vnd.github.v3+json" -H "Authorization: token ${GITHUB_RUNNER_PAT}" https://api.github.com/repos/${REPOSITORY_OWNER}/${REPOSITORY_NAME}/actions/runners/registration-token | jq -r .token)
}

# Configure the runner
set_token
./config.sh --unattended \
    --url https://github.com/${REPOSITORY_OWNER}/${REPOSITORY_NAME} \
    --replace --labels ${GITHUB_RUNNER_LABELS} --token ${REG_TOKEN}

# Cleanup the runner
cleanup() {
    echo "Removing runner..."
    set_token
    ./config.sh remove --unattended --token ${REG_TOKEN}
}

trap 'cleanup; exit 130' INT
trap 'cleanup; exit 143' TERM

# Start the runner
./run.sh > run.log 2>&1 & wait $!
```

@todo: `GITHUB_RUNNER_LABELS` @todo: `GITHUB_RUNNER_PAT` @todo: define these
variables

#### Create a Personal access token

Before proceeding, you will need to create a personal access token. This token
will be used to authenticate you on the GitHub Container Registry, allowing you
to push the image there.

!!! note

    We opted to use the GitHub Container Registry for our self-hosted Docker image
    because of its close integration with our existing GitHub environment. This
    decision enables us to restrict our CI/CD processes to the GitHub infrastructure
    while also demonstrating its capabilities. However, we could have also utilized
    our existing Google Cloud Container Registry.

Follow the
[_Managing Personal Access Token_ - GitHub docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
guide to create a personal access token (classic) named `GHCR_PAT` with the
`write:package` scope.

Export your token in as a variable. Replace`<my_container_repository_token>`
with your own token.

```sh title="Execute the following command(s) in a terminal"
GHCR_PAT=<my_container_repository_token>
```

#### Build and push the image to the container regsitry

With the entrypoint script ready, we can now build the Docker image. The Docker
image is built and pushed to the Container Registry.

Build the docker image. Make sure to update the tag of the Docker image to match
your username and repository.

```sh title="Execute the following command(s) in a terminal"
docker build -t ghcr.io/<my_username>/<my_repository_name>/github-runner:latest .
```

The output should be similar to this:

```
[+] Building 57.3s (14/14) FINISHED                                                                      docker:default
 => [internal] load build definition from Dockerfile                                                               0.1s
 => => transferring dockerfile: 920B                                                                               0.0s
 => [internal] load metadata for docker.io/library/ubuntu:24.04                                                    1.8s
 => [internal] load .dockerignore                                                                                  0.0s
 => => transferring context: 2B                                                                                    0.0s
 => [1/9] FROM docker.io/library/ubuntu:24.04@sha256:8a37d68f4f73ebf3d4efafbcf66379bf3728902a8038616808f04e34a9ab  2.5s
 => => resolve docker.io/library/ubuntu:24.04@sha256:8a37d68f4f73ebf3d4efafbcf66379bf3728902a8038616808f04e34a9ab  0.0s
 => => sha256:8a37d68f4f73ebf3d4efafbcf66379bf3728902a8038616808f04e34a9ab63ee 1.34kB / 1.34kB                     0.0s
 => => sha256:d35dfc2fe3ef66bcc085ca00d3152b482e6cafb23cdda1864154caf3b19094ba 424B / 424B                         0.0s
 => => sha256:edbfe74c41f8a3501ce542e137cf28ea04dd03e6df8c9d66519b6ad761c2598a 2.30kB / 2.30kB                     0.0s
 => => sha256:31e907dcc94a592a57796786399eb004dcbba714389fa615f5efa05a91316356 29.71MB / 29.71MB                   1.1s
 => => extracting sha256:31e907dcc94a592a57796786399eb004dcbba714389fa615f5efa05a91316356                          1.2s
 => [internal] load build context                                                                                  0.0s
 => => transferring context: 862B                                                                                  0.0s
 => [2/9] RUN apt-get update -y && apt-get install -y     build-essential lsb-release     python3 python3-pip     26.6s
 => [3/9] RUN useradd -m runner                                                                                    0.3s
 => [4/9] WORKDIR /home/actions-runner                                                                             0.1s
 => [5/9] RUN curl -o actions-runner-linux-x64-2.319.1.tar.gz -L https://github.com/actions/runner/releases/downl  7.3s
 => [6/9] RUN tar xzf ./actions-runner-linux-x64-2.319.1.tar.gz                                                    4.2s
 => [7/9] RUN ./bin/installdependencies.sh                                                                        12.3s
 => [8/9] COPY startup.sh .                                                                                        0.2s
 => [9/9] RUN chmod +x startup.sh                                                                                  0.3s
 => exporting to image                                                                                             1.5s
 => => exporting layers                                                                                            1.4s
 => => writing image sha256:91b6c9cbfd267d995f2701bcbc45181b78413b8b3d580f9ac6333f25ca2903c4                       0.0s
 => => naming to ghcr.io/username/a-guide-to-mlops/github-runner:latest                                            0.0s
```

Authenticate to the Container Registry:

```sh title="Execute the following command(s) in a terminal"
echo $GHCR_PAT | docker login -u <my_username> ghcr.io --password-stdin
```

Lastly, push the docker image to the GitHub Container Registry:

```sh title="Execute the following command(s) in a terminal"
docker push ghcr.io/<my_username>/<my_repository_name>/github-runner:latest
```

#### Adjust image visibility

Make sure to set the image visibility to `Public` in the GitHub Container
Registry settings.

In your repository page, click on *Packages* * on the right hand side, then on
your **github-runner** package. In **Package settings** in the **Danger Zone**
section,choose **Change package visibility** and set the package to **public**.

### Deploy the self-hosted runner

We will now deploy our self-hosted GitHub runner to our Kubernetes cluster with
the help of a YAML configuration file. As a reminder, the runner is used to
execute the GitHub Action workflows defined in the repository.

The runner will use the custom Docker image that we pushed to the GitHub
Container Registry. It is identified by a `base-runner` label.

Create a new file called `runner.yaml` in the `kubernetes` directory with the
following content. Replace `<my_username>` and `<my_repository_name>` with your
own username and repository name.

```txt title="kubernetes/runner.yaml"
apiVersion: v1
kind: Pod
metadata:
  name: github-runner
  labels:
    app: github-runner
spec:
  containers:
    - name: github-runner
      image: ghcr.io/<my_username>/<my_repository_name>/github-runner:latest
      env:
        - name: GITHUB_RUNNER_LABELS
          value: "base-runner"
        - name: GITHUB_RUNNER_PAT
          valueFrom:
            secretKeyRef:
              name: github-runner-pat
              key: token
      securityContext:
        runAsUser: 1000
      resources:
        limits:
          cpu: "4"
          memory: "2Gi"
        requests:
          cpu: "4"
          memory: "2Gi"
```



### Prepare Kubeconfig secret

You will need to create another personal access token. This token will be used
to authenticate you on the GitHub repository, allowing you to register the
self-hosted runner.

Follow the
[_Managing Personal Access Token_ - GitHub docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
guide to create a personal access token (classic) named `GH_RUNNER_PAT` with the
`repo` scope.

Export your token in as a variable. Replace `<my_repository_token>` with your
own token.

```
GH_RUNNER_PAT=<my_repository_token>
```

Run the following command to create the secret:

```sh title="Execute the following command(s) in a terminal"
printf "Enter your GitHub runner PAT: " && read GH_RUNNER_PAT \
   && kubectl create secret generic github-runner-pat --from-literal=token=$GH_RUNNER_PAT
```

### Install the base runner

To deploy the base runner to the Kubernetes cluster, navigate to `kubernetes`
folder and run the following command:

```sh title="Execute the following command(s) in a terminal"
kubectl apply -f runner.yaml
```

This will deploy a GitHub runner pod named `github-runner` in your current
Kubernetes namespace. The runner will automatically register itself to the
repository. See startup.sh for more information.

You can check the runner logs by connecting to the pod:

```sh title="Execute the following command(s) in a terminal"
kubectl exec -it github-runner -- bash
tail -f run.log
```

!!! note

    To remove the runner from the Kubernetes cluster, run the following command:

    ```sh title="Execute the following command(s) in a terminal"
    kubectl delete -f kubernetes/runner.yaml
    ```

    The runner will also automatically be removed from the repository.

### Self-hosted GPU runner

We also create a similar configuration file for the GPU runner, which is used
exclusively during the `train-report-publish-and-deploy` step of the workflow to
create a self-hosted GPU runner specifically for executing this step. This
approach optimizes resource usage by ensuring that GPU resources are only
utilized when necessary.

It also uses the same custom Docker image as the base runner. It is identified
by a `gpu-runner` label.

Create a new file called `runner-gpu.yaml` in the `kubernetes` directory with
the following content. Replace `<my_username>` and `<my_repository_name>` with
your own username and repository name.

```txt title="kubernetes/runner-gpu.yaml"
apiVersion: v1
kind: Pod
metadata:
  name: github-runner-gpu-${GITHUB_RUN_ID}
  labels:
    app: github-runner-gpu-${GITHUB_RUN_ID}
spec:
  volumes:
    - name: dshm
      emptyDir:
        medium: Memory
        sizeLimit: 16Gi
  containers:
    - name: github-runner-gpu-${GITHUB_RUN_ID}
      image: ghcr.io/<my_username>/<my_repository_name>/github-runner:latest
      # We mount a shared memory volume for training with PyTorch
      volumeMounts:
        - name: dshm
          mountPath: /dev/shm
      env:
        - name: GITHUB_RUNNER_LABELS
          value: "gpu-runner"
        - name: GITHUB_RUNNER_PAT
          valueFrom:
            secretKeyRef:
              name: github-runner-pat
              key: token
      securityContext:
        runAsUser: 1000
      resources:
        limits:
          cpu: "16"
          memory: "64Gi"
          nvidia.com/gpu: "1"
        requests:
          cpu: "16"
          memory: "64Gi"
          nvidia.com/gpu: "1"
```

@todo: explain dependencies of gpu-runner.

!!! tip

    The python dependencies for the GPU runner are listed in the
    requirements-freeze.txt file. The dependencies are installed in the Docker image
    used by the runner. This speeds up the workflow execution by avoiding dependency
    resolution and makes the workflow more reproducible.

    To update the dependencies, run the following command:

    pip freeze > requirements-freeze.txt

### Update the CI/CD configuration file

You'll now update the CI/CD configuration file to start a runner on the
Kubernetes cluster. Using the labels defined previously, you'll be able to start
the training of the model on the node with the GPU.

=== ":simple-github: GitHub"

    Update the `.github/workflows/mlops.yaml` file.

    Take some time to understand the new steps:

    ```yaml title=".github/workflows/mlops.yaml" hl_lines="15-18 21-49 52-54 71-77 169-186"
    name: MLOps

    on:
      # Runs on pushes targeting main branch
      push:
        branches:
          - main

      # Runs on pull requests
      pull_request:

      # Allows you to run this workflow manually from the Actions tab
      workflow_dispatch:

    # Allow the creation and usage of self-hosted runners
    permissions:
      contents: read
      id-token: write

    jobs:
      setup-runner:
        runs-on: [self-hosted, base-runner]
        steps:
          - name: Checkout repository
            uses: actions/checkout@v4
          - name: Login to Google Cloud
            uses: google-github-actions/auth@v2
            with:
              credentials_json: '${{ secrets.GOOGLE_SERVICE_ACCOUNT_KEY }}'
          - name: Get Google Cloud's Kubernetes credentials
            uses: 'google-github-actions/get-gke-credentials@v2'
            with:
              cluster_name: ${{ secrets.GCP_K8S_CLUSTER_NAME }}
              location: ${{ secrets.GCP_K8S_CLUSTER_ZONE }}
          - name: Setup kubectl
            uses: azure/setup-kubectl@v3
          - name: Initialize runner on Kubernetes
            env:
              KUBECONFIG_DATA: ${{ secrets.KUBECONFIG }}
            # We use envsubst to replace variables in runner-gpu.yaml
            # in order to create a unique runner name with the
            # GitHub run ID. This prevents conflicts when multiple
            # runners are created at the same time.
            run: |
              echo "$KUBECONFIG_DATA" > kubeconfig
              export KUBECONFIG=kubeconfig
              # We use run_id to make the runner name unique
              export GITHUB_RUN_ID="${{ github.run_id }}"
              envsubst < kubernetes/github-runner-gpu.yaml | kubectl apply -f -

      train-report-publish-and-deploy:
        permissions: write-all
        needs: setup-runner
        runs-on: [self-hosted, gpu-runner]
        steps:
          - name: Checkout repository
            uses: actions/checkout@v4
          - name: Setup Python
            uses: actions/setup-python@v5
            with:
              python-version: '3.11'
              cache: pip
          - name: Install dependencies
            run: pip install --requirement requirements-freeze.txt
          - name: Login to Google Cloud
            uses: google-github-actions/auth@v2
            with:
              credentials_json: '${{ secrets.GOOGLE_SERVICE_ACCOUNT_KEY }}'
          - name: Train model
            run: dvc repro --pull
          - name: Push the outcomes to DVC remote storage
            run: dvc push
          - name: Commit changes in dvc.lock
            uses: stefanzweifel/git-auto-commit-action@v5
            with:
              commit_message: Commit changes in dvc.lock
              file_pattern: dvc.lock
          - name: Setup CML
            if: github.event_name == 'pull_request'
            uses: iterative/setup-cml@v2
            with:
              version: '0.20.0'
          - name: Create CML report
            if: github.event_name == 'pull_request'
            env:
              REPO_TOKEN: ${{ secrets.GITHUB_TOKEN }}
            run: |
              # Fetch all other Git branches
              git fetch --depth=1 origin main:main

              # Add title to the report
              echo "# Experiment Report (${{ github.sha }})" >> report.md

              # Compare parameters to main branch
              echo "## Params workflow vs. main" >> report.md
              dvc params diff main --md >> report.md

              # Compare metrics to main branch
              echo "## Metrics workflow vs. main" >> report.md
              dvc metrics diff main --md >> report.md

              # Compare plots (images) to main branch
              dvc plots diff main

              # Create plots
              echo "## Plots" >> report.md

              # Create training history plot
              echo "### Training History" >> report.md
              echo "#### main" >> report.md
              echo '![](./dvc_plots/static/main_evaluation_plots_training_history.png "Training History")' >> report.md
              echo "#### workspace" >> report.md
              echo '![](./dvc_plots/static/workspace_evaluation_plots_training_history.png "Training History")' >> report.md

              # Create predictions preview
              echo "### Predictions Preview" >> report.md
              echo "#### main" >> report.md
              echo '![](./dvc_plots/static/main_evaluation_plots_pred_preview.png "Predictions Preview")' >> report.md
              echo "#### workspace" >> report.md
              echo '![](./dvc_plots/static/workspace_evaluation_plots_pred_preview.png "Predictions Preview")' >> report.md

              # Create confusion matrix
              echo "### Confusion Matrix" >> report.md
              echo "#### main" >> report.md
              echo '![](./dvc_plots/static/main_evaluation_plots_confusion_matrix.png "Confusion Matrix")' >> report.md
              echo "#### workspace" >> report.md
              echo '![](./dvc_plots/static/workspace_evaluation_plots_confusion_matrix.png "Confusion Matrix")' >> report.md

              # Publish the CML report
              cml comment update --target=pr --publish report.md
          - name: Log in to the Container registry
            uses: docker/login-action@v3
            with:
              registry: ${{ secrets.GCP_CONTAINER_REGISTRY_HOST }}
              username: _json_key
              password: ${{ secrets.GOOGLE_SERVICE_ACCOUNT_KEY }}
          - name: Import the BentoML model
            if: github.ref == 'refs/heads/main'
            run: bentoml models import model/celestial_bodies_classifier_model.bentomodel
          - name: Build the BentoML model artifact
            if: github.ref == 'refs/heads/main'
            run: bentoml build src
          - name: Containerize and publish the BentoML model artifact Docker image
            if: github.ref == 'refs/heads/main'
            run: |
              # Containerize the Bento
              bentoml containerize celestial_bodies_classifier:latest \
                --image-tag ${{ secrets.GCP_CONTAINER_REGISTRY_HOST }}/celestial-bodies-classifier:latest \
                --image-tag ${{ secrets.GCP_CONTAINER_REGISTRY_HOST }}/celestial-bodies-classifier:${{ github.sha }}
              # Push the container to the Container Registry
              docker push --all-tags ${{ secrets.GCP_CONTAINER_REGISTRY_HOST }}/celestial-bodies-classifier
          - name: Get Google Cloud's Kubernetes credentials
            if: github.ref == 'refs/heads/main'
            uses: google-github-actions/get-gke-credentials@v2
            with:
              cluster_name: ${{ secrets.GCP_K8S_CLUSTER_NAME }}
              location: ${{ secrets.GCP_K8S_CLUSTER_ZONE }}
          - name: Update the Kubernetes deployment
            if: github.ref == 'refs/heads/main'
            run: |
              yq -i '.spec.template.spec.containers[0].image = "${{ secrets.GCP_CONTAINER_REGISTRY_HOST }}/celestial-bodies-classifier:${{ github.sha }}"' kubernetes/deployment.yaml
          - name: Deploy the model on Kubernetes
            if: github.ref == 'refs/heads/main'
            run: |
              kubectl apply \
                -f kubernetes/deployment.yaml \
                -f kubernetes/service.yaml

    cleanup-runner:
        needs: train-report-publish-and-deploy
        runs-on: [self-hosted, base-runner]
        # Always run this job even if the previous jobs fail
        if: always()
        steps:
          - name: Checkout repository
            uses: actions/checkout@v4
          - name: Setup kubectl
            uses: azure/setup-kubectl@v3
          - name: Cleanup runner on Kubernetes
            env:
              KUBECONFIG_DATA: ${{ secrets.KUBECONFIG }}
            run: |
              echo "$KUBECONFIG_DATA" > kubeconfig
              export KUBECONFIG=kubeconfig
              export GITHUB_RUN_ID="${{ github.run_id }}"
              envsubst < kubernetes/github-runner-gpu.yaml | kubectl delete --wait=false -f -
    ```

    Here, the following should be noted:

    * the `setup-runner` job creates a self-hosted GPU runner.
    * the `train-report-publish-and-deploy` job run the DVC pipeline and reports the
      results back to the pull request.
    * the `cleanup-runner` job deletes the self-hosted GPU runner.

    Check the differences with Git to validate the changes.

    ```sh title="Execute the following command(s) in a terminal"
    # Show the differences with Git
    git diff .github/workflows/mlops.yaml
    ```

    The output should be similar to this:

    ```diff
    diff --git a/.github/workflows/mlops.yaml b/.github/workflows/mlops.yaml
    index 30bbce8..5d4a6dd 100644
    --- a/.github/workflows/mlops.yaml
    +++ b/.github/workflows/mlops.yaml
    @@ -12,10 +12,48 @@ on:
       # Allows you to run this workflow manually from the Actions tab
       workflow_dispatch:

    +# Allow the creation and usage of self-hosted runners
    +permissions:
    +  contents: read
    +  id-token: write
    +
     jobs:
    +  setup-runner:
    +    runs-on: ubuntu-latest
    +    steps:
    +      - name: Checkout repository
    +        uses: actions/checkout@v3
    +      - name: Login to Google Cloud
    +        uses: 'google-github-actions/auth@v1'
    +        with:
    +          credentials_json: '${{ secrets.CML_GCP_SERVICE_ACCOUNT_KEY }}'
    +      - name: Get Google Cloud's Kubernetes credentials
    +        uses: 'google-github-actions/get-gke-credentials@v1'
    +        with:
    +          cluster_name: '<my_cluster_name>'
    +          location: '<my_cluster_zone>'
    +      - uses: iterative/setup-cml@v1
    +        with:
    +          version: '0.19.1'
    +      - name: Initialize runner on Kubernetes
    +        env:
    +          REPO_TOKEN: ${{ secrets.CML_PAT }}
    +        run: |
    +          export KUBERNETES_CONFIGURATION=$(cat $KUBECONFIG)
    +          # https://cml.dev/doc/ref/runner
    +          # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resources/task#machine-type
    +          # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resources/task#{cpu}-{memory}
    +          cml runner \
    +            --labels="cml-runner" \
    +            --cloud="kubernetes" \
    +            --cloud-type="1-2000" \
    +            --cloud-kubernetes-node-selector="gpu=true" \
    +            --single
    +
       train-and-report:
         permissions: write-all
    -    runs-on: ubuntu-latest
    +    needs: setup-runner
    +    runs-on: [self-hosted, cml-runner]
         steps:
           - name: Checkout repository
             uses: actions/checkout@v3
    ```

    Take some time to understand the changes made to the file.

=== ":simple-gitlab: GitLab"

    !!! warning "This is a work in progress"

        This part is a work in progress. Please check back later for updates. Thank you!

    Update the `.gitlab-ci.yml` file.

    Check the differences with Git to validate the changes.

    The output should be similar to this:

    Take some time to understand the changes made to the file.

### Push the CI/CD pipeline configuration file to Git

=== ":simple-github: GitHub"

    Push the CI/CD pipeline configuration file to Git.

    ```sh title="Execute the following command(s) in a terminal"
    # Add the configuration files
    git add .

    # Commit the changes
    git commit -m "A pipeline will run my experiment on Kubernetes on each push"

    # Push the changes
    git push
    ```

=== ":simple-gitlab: GitLab"

    Push the CI/CD pipeline configuration file to Git.

    ```sh title="Execute the following command(s) in a terminal"
    # Add the configuration file
    git add .gitlab-ci.yml

    # Commit the changes
    git commit -m "A pipeline will run my experiment on Kubernetes on each push"

    # Push the changes
    git push
    ```

### Check the results

On GitHub, you can see the pipeline running on the **Actions** page.

On GitLab, you can see the pipeline running on the **CI/CD > Pipelines** page.

The pod should be created on the Kubernetes Cluster.

=== ":simple-googlecloud: Google Cloud"

    On Google Cloud Console, you can see the pod that has been created on the
    **Kubernetes Engine > Workloads** page. Open the pod and go to the **YAML** tab
    to see the configuration of the pod. You should notice that the pod has been
    created with the node selector `gpu=true` and that it has been created on the
    right node.

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

This chapter is done, you can check the summary.

## Summary

Congratulations! You now can train your model on on a custom infrastructure with
custom hardware for specific use-cases.

In this chapter, you have successfully:

1. Created a Kubernetes cluster on Google Cloud
2. Configured the CI/CD to start a runner on Kubernetes
3. Trained the model on the Kubernetes cluster

### Destroy the Kubernetes cluster

When you are done with the chapter, you can destroy the Kubernetes cluster.

```sh title="Execute the following command(s) in a terminal"
# Destroy the Kubernetes cluster
gcloud container clusters delete --zone europe-west6-a mlops-kubernetes
```

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
- [x] Model publication to the artifact registry is automated
- [x] Model can be accessed from a Kubernetes cluster
- [x] Model is continuously deployed with the CI/CD
- [x] Model can be trained on a custom infrastructure with custom hardware for
      specific use-cases

You can now safely continue to the next chapter of this guide concluding your
journey and the next things you could do with your model.

## Sources

Highly inspired by:

- [_About self-hosted runners_ - GitHub docs](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)
- [_GitHub Actions self-hosted runners on Google Cloud_ - github.blog](https://github.blog/news-insights/product-news/github-actions-self-hosted-runners-on-google-cloud/)
- [_Working with the Container registry_ - GitHub docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [_Create a Docker based Self Hosted GitHub runner Linux container_ - dev.to](https://dev.to/pwd9000/create-a-docker-based-self-hosted-github-runner-linux-container-48dh)
- [_Self-hosted runner security_ - GitHubdocs](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners#self-hosted-runner-security)
- [_Security for self-managed runners_ - GitLab docs](https://docs.gitlab.com/runner/security/)
- [_Install kubectl and configure cluster access_ - cloud.google.com](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl)
- [_gcloud container clusters create_ - cloud.google.com](https://cloud.google.com/sdk/gcloud/reference/container/clusters/create)
- [_Install Tools_ - kubernetes.io](https://kubernetes.io/docs/tasks/tools/)
- [_Assigning Pods to Nodes_ - kubernetes.io](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector)
- [_Assign Pods to Nodes_ - kubernetes.io](https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes/)
