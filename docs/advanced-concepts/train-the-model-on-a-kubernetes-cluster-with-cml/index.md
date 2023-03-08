# Train the model on a Kubernetes cluster with CML

!!! warning

	This is a work in progress.

## Introduction

The purpose of this guide is to improve the results obtained at the end of [The guide](../../the-guide/introduction/index.md) to allow the training of the model on a Kubernetes cluster with the help of CML.

Carrying out the guide is necessary to follow this guide.

In this chapter, you will learn how to:

1. Create a Kubernetes cluster on Google Cloud
2. Configure CML to start a runner on Kubernetes
3. Start the training of the model from your CI/CD pipeline on the Kubernetes cluster

## Steps

### Enable the Google Kubernetes Engine API

You must enable the Google Kubernetes Engine API to create Kubernetes clusters on Google Cloud.

[Enable Google Kubernetes Engine API :octicons-arrow-up-right-16:](https://console.cloud.google.com/flows/enableapi?apiid=container.googleapis.com){ .md-button .md-button--primary }

### Create the Kubernetes cluster

Create the Google Kubernetes cluster with the Google Cloud CLI.

```sh title="Execute the following command(s) in a terminal"
gcloud container clusters create \
	--machine-type=e2-standard-2 \
	--num-nodes=2 \
	--zone=europe-west6-a \
	mlops-kubernetes
```

### Install kubectl

Install the Kubernetes CLI using the Google Cloud CLI to interact with Kubernetes clusters.

```sh title="Execute the following command(s) in a terminal"
# Install kubectl with gcloud
gcloud components install kubectl
```

### Validate kubectl can access the cluster

Validate kubectl can access the cluster using Google Cloud credentials.

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

### Generate a universal kubeconfig file

The kubeconfig file allows to authenticate to a Kubernetes cluster. This file will be used in the CI/CD pipeline to create runners.

In order to obtain a kubeconfig file that can be used without the need of the Google Cloud CLI (gcloud), a number of steps are required. This is done to demonstrate the usage of Kubernetes and CML without being coupled to a specific authentication provider such as gcloud.

Create a file `my-service-account.yml`. It will allow to create a user on the Google Kubernetes Cluster we'll use later to authenticate to the cluster.

```yaml title="my-service-account.yaml"
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-user
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: my-user-role
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "watch", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: my-user-role-binding
subjects:
  - kind: ServiceAccount
    name: my-user
roleRef:
  kind: Role
  name: my-user-role
  apiGroup: rbac.authorization.k8s.io
```

Create the resources on the Google Kubernetes cluster.

```sh title="Execute the following command(s) in a terminal"
kubectl apply -f my-service-account.yml
```


```sh title="Execute the following command(s) in a terminal"
export USE_GKE_GCLOUD_AUTH_PLUGIN=True

gcloud container clusters get-credentials mlops-kubernetes \
	--zone=europe-west6-a
```

### Check the Kubernetes access with kubectl

```sh title="Execute the following command(s) in a terminal"
./kubectl get namespaces
```

### Display the kubectl config

=== ":simple-github: GitHub"

	Display the configuration of kubectl.

	```sh title="Execute the following command(s) in a terminal"
	# Display the kubectl configuration
	./kubectl config view
	```

=== ":simple-gitlab: GitLab"

	Encode and display the configuration of kubectl as `base64`. It allows to hide the secret in GitLab CI logs as a
	security measure.

	!!! tip

		If on Linux, you can use the command `kubectl config view | base64 -w 0 -i -`.

	```sh title="Execute the following command(s) in a terminal"
	# Encode the kubectl configuration to base64
	./kubectl config view | base64 -i -
	```

### Store the content of the kubeconfig file as a CI/CD variable 

=== ":simple-github: GitHub"

	Store the output as a CI/CD variable by going to the **Settings** section from
	the top header of your GitHub repository.

	Select **Secrets > Actions** and select **New repository secret**.

	Create a new variable named `GCP_KUBECONFIG` with the output value of
	the Google Service Account key file as its value. Save the variable by selecting
	**Add secret**.

=== ":simple-gitlab: GitLab"

	Store the output as a CI/CD Variable by going to **Settings > CI/CD** from the
	left sidebar of your GitLab project.

	Select **Variables** and select **Add variable**.

	Create a new variable named `GCP_KUBECONFIG` with
	the Google Service Account key file encoded in `base64` as its value.

	- **Protect variable**: _Unchecked_
	- **Mask variable**: _Checked_
	- **Expand variable reference**: _Unchecked_

	Save the variable by clicking **Add variable**.

### Update the CI/CD configuration file

=== ":simple-github: GitHub"

	In order to allow CML to create a self-hosted runner, a Personal Access Token (PAT) must be
	created.

	Follow the [_Personal Access Token_ - cml.dev](https://cml.dev/doc/self-hosted-runners?tab=GitHub#personal-access-token) guide to create a personal access token named `CML_PAT` with the `repo` scope.

	Store the Personal Access Token as a CI/CD variable by going to the **Settings** section from
	the top header of your GitHub repository.

	Select **Secrets > Actions** and select **New repository secret**.

	Create a new variable named `CML_PAT` with the value of
	the Personal Access Token as its value. Save the variable by selecting
	**Add secret**.

	Update the `.github/workflows/mlops.yml` file.

	```yaml  title=".github/workflows/mlops.yml" hl_lines="9-10 42-133"
	TODO
	```

	Check the differences with Git to validate the changes.

	```sh title="Execute the following command(s) in a terminal"
	# Show the differences with Git
	git diff .github/workflows/mlops.yml
	```

	The output should be similar to this:

	```diff
	diff --git a/.github/workflows/mlops.yml b/.github/workflows/mlops.yml
	index 0ca4d29..10afa49 100644
	--- a/.github/workflows/mlops.yml
	+++ b/.github/workflows/mlops.yml
	TODO
	```

	Take some time to understand the changes made to the file.

=== ":simple-gitlab: GitLab"

	Update the `.gitlab-ci.yml` file.

	```yaml title=".gitlab-ci.yml" hl_lines="2 19-38 43-47"
	stages:
	  - setup runner
	  - train
	  - report
	
	variables:
	  # Change pip's cache directory to be inside the project directory since we can
	  # only cache local items.
	  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
	  # https://dvc.org/doc/user-guide/troubleshooting?tab=GitLab-CI-CD#git-shallow
	  GIT_DEPTH: '0'
	
	# Pip's cache doesn't store the python packages
	# https://pip.pypa.io/en/stable/reference/pip_install/#caching
	cache:
	  paths:
	    - .cache/pip
	
	setup-runner:
	  stage: setup runner
	  image: iterativeai/cml:0-dvc2-base1
	  before_script:
	    # Install Kubernetes
	    - export KUBERNETES_VERSION=$(curl -L -s https://dl.k8s.io/release/stable.txt)
	    - curl -LO -s "https://dl.k8s.io/release/${KUBERNETES_VERSION}/bin/linux/amd64/kubectl"
	    - curl -LO -s "https://dl.k8s.io/${KUBERNETES_VERSION}/bin/linux/amd64/kubectl.sha256"
	    - echo "$(cat kubectl.sha256) kubectl" | sha256sum --check
	    - sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
	    # https://cml.dev/doc/self-hosted-runners?tab=Kubernetes#cloud-compute-resource-credentials
	    - export KUBERNETES_CONFIGURATION=$(cat $GCP_KUBECONFIG)
	  script:
	    # https://cml.dev/doc/ref/runner#--cloud-type
	    # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resources/task#machine-type
	    # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resources/task#{cpu}-{memory}+{accelerator}*{count}
	    - cml runner
	        --labels="cml-runner"
	        --cloud="kubernetes"
	        --cloud-type="64-256000+nvidia-tesla-k80*1"
	
	train:
	  stage: train
	  image: iterativeai/cml:0-dvc2-base1
	  needs:
	    - setup-runner
	  tags:
	    # Uses the runner set up by CML
	    - cml-runner
	  rules:
	    - if: $CI_COMMIT_BRANCH == "main"
	    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
	  variables:
	    # Set the path to Google Service Account key for DVC - https://dvc.org/doc/command-reference/remote/add#google-cloud-storage
	    GOOGLE_APPLICATION_CREDENTIALS: "${CI_PROJECT_DIR}/google-service-account-key.json"
	  before_script:
	    # Set the Google Service Account key
	    - echo "${GCP_SERVICE_ACCOUNT_KEY}" | base64 -d > $GOOGLE_APPLICATION_CREDENTIALS
	    # Install dependencies
	    - pip install --requirement src/requirements.txt
	  script:
	    # Pull data from DVC
	    - dvc pull
	    # Run the experiment
	    - dvc repro
	  artifacts:
	    expire_in: 1 week
	    paths:
	      - "evaluation"
	
	report:
	  stage: report
	  image: iterativeai/cml:0-dvc2-base1
	  needs:
	    - job: train
	      artifacts: true
	  rules:
	    - if: $CI_COMMIT_BRANCH == "main"
	    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
	  variables:
	    REPO_TOKEN: $CML_PAT
	  script:
	    - |
	      # Compare parameters to main branch
	      echo "# Params workflow vs. main" >> report.md
	      echo >> report.md
	      dvc params diff main --show-md >> report.md
	      echo >> report.md
	
	      # Compare metrics to main branch
	      echo "# Metrics workflow vs. main" >> report.md
	      echo >> report.md
	      dvc metrics diff main --show-md >> report.md
	      echo >> report.md
	
	      # Create plots
	      echo "# Plots" >> report.md
	      echo >> report.md
	
	      echo "## Precision recall curve" >> report.md
	      echo >> report.md
	      dvc plots diff \
	        --target evaluation/plots/prc.json \
	        -x recall \
	        -y precision \
	        --show-vega main > vega.json
	      vl2png vega.json > prc.png
	      echo '![](./prc.png "Precision recall curve")' >> report.md
	      echo >> report.md
	
	      echo "## Roc curve" >> report.md
	      echo >> report.md
	      dvc plots diff \
	        --target evaluation/plots/sklearn/roc.json \
	        -x fpr \
	        -y tpr \
	        --show-vega main > vega.json
	      vl2png vega.json > roc.png
	      echo '![](./roc.png "Roc curve")' >> report.md
	      echo >> report.md
	
	      echo "## Confusion matrix" >> report.md
	      echo >> report.md
	      dvc plots diff \
	        --target evaluation/plots/sklearn/confusion_matrix.json \
	        --template confusion \
	        -x actual \
	        -y predicted \
	        --show-vega main > vega.json
	      vl2png vega.json > confusion_matrix.png
	      echo '![](./confusion_matrix.png "Confusion Matrix")' >> report.md
	      echo >> report.md
	
	      # Publish the CML report
	      cml comment create --target=pr --publish report.md
	```

	Check the differences with Git to validate the changes.

	```sh title="Execute the following command(s) in a terminal"
	# Show the differences with Git
	git diff .gitlab-ci.yml
	```

	The output should be similar to this:

	```diff
	diff --git a/.gitlab-ci.yml b/.gitlab-ci.yml
	index 561d04f..fad1002 100644
	--- a/.gitlab-ci.yml
	+++ b/.gitlab-ci.yml
	@@ -15,9 +15,35 @@ cache:
	   paths:
	     - .cache/pip

	+setup-runner:
	+  stage: setup runner
	+  image: iterativeai/cml:0-dvc2-base1
	+  before_script:
	+    # Install Kubernetes
	+    - export KUBERNETES_VERSION=$(curl -L -s https://dl.k8s.io/release/stable.txt)
	+    - curl -LO -s "https://dl.k8s.io/release/${KUBERNETES_VERSION}/bin/linux/amd64/kubectl"
	+    - curl -LO -s "https://dl.k8s.io/${KUBERNETES_VERSION}/bin/linux/amd64/kubectl.sha256"
	+    - echo "$(cat kubectl.sha256) kubectl" | sha256sum --check
	+    - sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
	+    # https://cml.dev/doc/self-hosted-runners?tab=Kubernetes#cloud-compute-resource-credentials
	+    - export KUBERNETES_CONFIGURATION=$(cat $GCP_KUBECONFIG)
	+  script:
	+    # https://cml.dev/doc/ref/runner#--cloud-type
	+    # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resources/task#machine-type
	+    # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resources/task#{cpu}-{memory}+{accelerator}*{count}
	+    - cml runner
	+        --labels="cml-runner"
	+        --cloud="kubernetes"
	+        --cloud-type="64-256000+nvidia-tesla-k80*1"
	+
	 train:
	   stage: train
	   image: iterativeai/cml:0-dvc2-base1
	+  needs:
	+    - setup-runner
	+  tags:
	+    # Uses the runner set up by CML
	+    - cml-runner
	   rules:
	     - if: $CI_COMMIT_BRANCH == "main"
	     - if: $CI_PIPELINE_SOURCE == "merge_request_event"
	```

	Take some time to understand the changes made to the file.

### Push the CI/CD pipeline configuration file to Git

=== ":simple-github: GitHub"

	Push the CI/CD pipeline configuration file to Git.

	```sh title="Execute the following command(s) in a terminal"
	# Add the configuration file
	git add .github/workflows/mlops.yml

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

On GitLab, you can see the pipeline running on the **CI/CD > Pipelines** page.

On GitHub, you can see the pipeline running on the **Actions** page.

TODO

This chapter is done, you can check the summary.

## Summary

Congrats! You now can train your model on on a custom infrastructure with custom hardware for specific use-cases.

In this chapter, you have successfully:

1. Created a Kubernetes cluster on Google Cloud
2. Configured CML to start a runner on Kubernetes
3. Trained the model on the Kubernetes cluster

## State of the MLOps process

- ✅ The training of the model can be done on a custom infrastructure with custom hardware for specific use-cases.

## Sources

Highly inspired by the [_Self-hosted (On-premise or Cloud) Runners_ - cml.dev](https://cml.dev/doc/self-hosted-runners), [_Install kubectl and configure cluster access_ - cloud.google.com](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl), [_gcloud container clusters create_ - cloud.google.com](https://cloud.google.com/sdk/gcloud/reference/container/clusters/create) and the [_Install Tools_ - kubernetes.io](https://kubernetes.io/docs/tasks/tools/) guides.

Want to see what the result at the end of this chapter should look like? Have a
look at the Git repository directory here:
[train-the-model-on-a-kubernetes-cluster-with-cml](https://github.com/csia-pme/a-guide-to-mlops/tree/main/docs/advanced-concepts/train-the-model-on-a-kubernetes-cluster-with-cml).
