# Train the model on a Kubernetes cluster with CML

!!! warning

	This is a work in progress. CML does not support the Kubernetes arbitrary node selector at the moment. Check this issue for more information: <https://github.com/iterative/cml/issues/1365>.

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

### Display the nodes labels

Display the nodes labels with the following command.

```sh title="Execute the following command(s) in a terminal"
kubectl get nodes --show-labels
```

The output should be similar to this. As noticed, you have two nodes in your cluster.

```
NAME                                              STATUS   ROLES    AGE   VERSION            LABELS
gke-mlops-kubernetes-default-pool-d4f966ea-8rbn   Ready    <none>   49s   v1.24.9-gke.3200   beta.kubernetes.io/arch=amd64,[...]
gke-mlops-kubernetes-default-pool-d4f966ea-p7qm   Ready    <none>   50s   v1.24.9-gke.3200   beta.kubernetes.io/arch=amd64,[...]
```

### Labelize the nodes

Let's imagine one node has a GPU and the other one doesn't. You can labelize the nodes to be able to use the GPU node for the training of the model. For our expiriment, there is no need to have a GPU to train the model but it's for demonstration purposes.

```sh title="Execute the following command(s) in a terminal"
kubectl label nodes <your-node-1-name> gpu=true
kubectl label nodes <your-node-2-name> gpu=false
```

In the previous example, the nodes are named `gke-mlops-kubernetes-default-pool-d4f966ea-8rbn` and `gke-mlops-kubernetes-default-pool-d4f966ea-p7qm`. The command will be the following.

```sh title="Labelization example"
kubectl label nodes gke-mlops-kubernetes-default-pool-d4f966ea-8rbn gpu=true
kubectl label nodes gke-mlops-kubernetes-default-pool-d4f966ea-p7qm gpu=false
```

You can check the labels with the `kubectl get nodes --show-labels` command. You should see for both nodes the `gpu` label with the value `true` or `false`.

### Update the CI/CD configuration file

You'll now update the CI/CD configuration file to start a runner on the Kubernetes cluster with the help of CML. Using the labels defined previously, you'll be able to start the training of the model on the node with the GPU.

=== ":simple-github: GitHub"

	In order to allow CML to create a self-hosted runner, a Personal Access Token (PAT) must be
	created.

	Follow the [_Personal Access Token_ - cml.dev](https://cml.dev/doc/self-hosted-runners?tab=GitHub#personal-access-token) guide to create a personal access token named `CML_PAT` with the `repo` scope.

	Store the Personal Access Token as a CI/CD variable by going to the **Settings** section from
	the top header of your GitHub repository.

	Select **Secrets and variables > Actions** and select **New repository secret**.

	Create a new variable named `CML_PAT` with the value of
	the Personal Access Token as its value. Save the variable by selecting
	**Add secret**.

	Update the `.github/workflows/mlops.yml` file.

	```yaml  title=".github/workflows/mlops.yml" hl_lines="15-17 20-50 53-55"
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
	
	permissions:
	  contents: read
	  id-token: write
	
	jobs:
	  setup-runner:
	    runs-on: ubuntu-latest
	    steps:
	      - name: Checkout repository
	        uses: actions/checkout@v3
	      - name: Login to Google Cloud
	        uses: 'google-github-actions/auth@v1'
	        with:
	          credentials_json: '${{ secrets.GCP_SERVICE_ACCOUNT_KEY }}'
	      - name: Get Google Cloud's Kubernetes credentials
	        uses: 'google-github-actions/get-gke-credentials@v1'
	        with:
	          cluster_name: 'mlops-kubernetes'
	          location: 'europe-west6-a'
	      - name: Setup CML
	        uses: iterative/setup-cml@v1
	        with:
	          version: '0.18.17'
	      - name: Initialize runner on Kubernetes
	        env:
	          REPO_TOKEN: ${{ secrets.CML_PAT }}
	        run: |
	          export KUBERNETES_CONFIGURATION=$(cat $KUBECONFIG)
	          # https://cml.dev/doc/ref/runner#--cloud-type
	          # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resources/task#machine-type
	          # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resources/task#{cpu}-{memory}	+{accelerator}*{count}
	          cml runner \
	            --name="CML" \
	            --labels="cml-runner" \
	            --cloud="kubernetes" \
	            --reuse-idle
	
	  train:
	    needs: setup-runner
	    runs-on: [self-hosted, cml-runner]
	    timeout-minutes: 50400 # 35 days
	    steps:
	      - name: Checkout repository
	        uses: actions/checkout@v3
	      - name: Setup Python
	        uses: actions/setup-python@v4
	        with:
	          python-version: '3.10'
	          cache: 'pip'
	      - name: Setup DVC
	        uses: iterative/setup-dvc@v1
	        with:
	          version: '2.37.0'
	      - name: Login to Google Cloud
	        uses: 'google-github-actions/auth@v1'
	        with:
	          credentials_json: '${{ secrets.GCP_SERVICE_ACCOUNT_KEY }}'
	      - name: Train model
	        working-directory: docs/advanced-concepts/train-the-model-on-a-kubernetes-cluster-with-cml
	        run: |
	          # Install dependencies
	          pip install --requirement src/requirements.txt
	          # Pull data from DVC
	          dvc pull
	          # Run the experiment
	          dvc repro
	      - name: Upload evaluation results
	        uses: actions/upload-artifact@v3
	        with:
	          path: docs/advanced-concepts/train-the-model-on-a-kubernetes-cluster-with-cml/evaluation
	          retention-days: 5
	
	  report:
	    needs: train
	    if: github.event_name == 'pull_request'
	    runs-on: ubuntu-latest
	    steps:
	      - name: Checkout repository
	        uses: actions/checkout@v3
	        with:
	          ref: ${{ github.event.pull_request.head.sha }}
	      - name: Download evaluation results
	        uses: actions/download-artifact@v3
	      - name: Copy evaluation results
	        shell: bash
	        run: |
	          # Delete current evaluation results
	          rm -rf docs/advanced-concepts/train-the-model-on-a-kubernetes-cluster-with-cml/evaluation
	          # Replace with the new evaluation results
	          mv artifact docs/advanced-concepts/train-the-model-on-a-kubernetes-cluster-with-cml/evaluation
	      - name: Setup DVC
	        uses: iterative/setup-dvc@v1
	        with:
	          version: '2.37.0'
	      - name: Setup CML
	        uses: iterative/setup-cml@v1
	        with:
	          version: '0.18.17'
	      - name: Create CML report
	        env:
	          REPO_TOKEN: ${{ secrets.GITHUB_TOKEN }}
	        working-directory: docs/advanced-concepts/train-the-model-on-a-kubernetes-cluster-with-cml
	        run: |
	          # Fetch all other Git branches
	          git fetch --depth=1 origin main:main
	
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
	git diff .github/workflows/mlops.yml
	```

	The output should be similar to this:

	```diff
	diff --git a/.github/workflows/mlops.yml b/.github/workflows/mlops.yml
	index 0ca4d29..10afa49 100644
	--- a/.github/workflows/mlops.yml
	+++ b/.github/workflows/mlops.yml
	@@ -12,9 +12,47 @@ on:
	   # Allows you to run this workflow manually from the Actions tab
	   workflow_dispatch:
	 
	+permissions:
	+  contents: read
	+  id-token: write
	+
	 jobs:
	-  train:
	+  setup-runner:
	     runs-on: ubuntu-latest
	+    steps:
	+      - name: Checkout repository
	+        uses: actions/checkout@v3
	+      - name: Login to Google Cloud
	+        uses: 'google-github-actions/auth@v1'
	+        with:
	+          credentials_json: '${{ secrets.GCP_SERVICE_ACCOUNT_KEY }}'
	+      - name: Get Google Cloud's Kubernetes credentials
	+        uses: 'google-github-actions/get-gke-credentials@v1'
	+        with:
	+          cluster_name: 'mlops-kubernetes'
	+          location: 'europe-west6-a'
	+      - name: Setup CML
	+        uses: iterative/setup-cml@v1
	+        with:
	+          version: '0.18.17'
	+      - name: Initialize runner on Kubernetes
	+        env:
	+          REPO_TOKEN: ${{ secrets.CML_PAT }}
	+        run: |
	+          export KUBERNETES_CONFIGURATION=$(cat $KUBECONFIG)
	+          # https://cml.dev/doc/ref/runner#--cloud-type
	+          # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resources/task#machine-type
	+          # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resources/task#{cpu}-{memory}   	+{accelerator}*{count}
	+          cml runner \
	+            --name="CML" \
	+            --labels="cml-runner" \
	+            --cloud="kubernetes" \
	+            --reuse-idle
	+
	+  train:
	+    needs: setup-runner
	+    runs-on: [self-hosted, cml-runner]
	+    timeout-minutes: 50400 # 35 days
	     steps:
	       - name: Checkout repository
	         uses: actions/checkout@v3
	```

	Take some time to understand the changes made to the file.

=== ":simple-gitlab: GitLab"

	Update the `.gitlab-ci.yml` file.

	```yaml title=".gitlab-ci.yml" hl_lines="2 19-43 48-51"
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
	  rules:
	    - if: $CI_COMMIT_BRANCH == "main"
	    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
	  variables:
	    # Set the path to Google Service Account key for DVC - https://dvc.org/doc/command-reference/remote/	add#google-cloud-storage
	    GOOGLE_APPLICATION_CREDENTIALS: "${CI_PROJECT_DIR}/google-service-account-key.json"
	  before_script:
	    # Install Google Cloud CLI (gcloud)
	    - sudo apt-get install apt-transport-https ca-certificates gnupg
	    - curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/cloud.google.gpg
	    - sudo apt-get update && sudo apt-get install google-cloud-cli
	    # Set the Google Service Account key
	    - echo "${GCP_SERVICE_ACCOUNT_KEY}" | base64 -d > $GOOGLE_APPLICATION_CREDENTIALS
	    # Authenticate to Google Cloud with the service key
	    - gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
	  script:
	    # https://cml.dev/doc/ref/runner
	    - cml runner
	        --name="CML"
	        --labels="cml-runner"
	        --cloud="kubernetes"
	        --reuse-idle
	
	train:
	  stage: train
	  image: iterativeai/cml:0-dvc2-base1
	  tags:
	    - cml-runner
	  needs:
	    - setup-runner
	  rules:
	    - if: $CI_COMMIT_BRANCH == "main"
	    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
	  variables:
	    # Set the path to Google Service Account key for DVC - https://dvc.org/doc/command-reference/remote/	add#google-cloud-storage
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
	@@ -1,4 +1,5 @@
	 stages:
	+  - setup runner
	   - train
	   - report
	 
	@@ -15,9 +16,39 @@ cache:
	   paths:
	     - .cache/pip
	 
	+setup-runner:
	+  stage: setup runner
	+  image: iterativeai/cml:0-dvc2-base1
	+  rules:
	+    - if: $CI_COMMIT_BRANCH == "main"
	+    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
	+  variables:
	+    # Set the path to Google Service Account key for DVC - https://dvc.org/doc/command-reference/remote/add#google-cloud-storage
	+    GOOGLE_APPLICATION_CREDENTIALS: "${CI_PROJECT_DIR}/google-service-account-key.json"
	+  before_script:
	+    # Install Google Cloud CLI (gcloud)
	+    - sudo apt-get install apt-transport-https ca-certificates gnupg
	+    - curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo tee /usr/share/keyrings/cloud.google.gpg
	+    - sudo apt-get update && sudo apt-get install google-cloud-cli
	+    # Set the Google Service Account key
	+    - echo "${GCP_SERVICE_ACCOUNT_KEY}" | base64 -d > $GOOGLE_APPLICATION_CREDENTIALS
	+    # Authenticate to Google Cloud with the service key
	+    - gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
	+  script:
	+    # https://cml.dev/doc/ref/runner
	+    - cml runner
	+        --name="CML"
	+        --labels="cml-runner"
	+        --cloud="kubernetes"
	+        --reuse-idle
	+
	 train:
	   stage: train
	   image: iterativeai/cml:0-dvc2-base1
	+  tags:
	+    - cml-runner
	+  needs:
	+    - setup-runner
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

On Google Cloud Console, you can see the pod that has been created on the **Kubernetes Engine > Workloads** page.

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

Highly inspired by the [_Self-hosted (On-premise or Cloud) Runners_ - cml.dev](https://cml.dev/doc/self-hosted-runners), [_Install kubectl and configure cluster access_ - cloud.google.com](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl), [_gcloud container clusters create_ - cloud.google.com](https://cloud.google.com/sdk/gcloud/reference/container/clusters/create), the [_Install Tools_ - kubernetes.io](https://kubernetes.io/docs/tasks/tools/), [_Assigning Pods to Nodes_ - kubernetes.io](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector) and [_Assign Pods to Nodes_ - kubernetes.io](https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes/) guides.

Want to see what the result at the end of this chapter should look like? Have a
look at the Git repository directory here:
[train-the-model-on-a-kubernetes-cluster-with-cml](https://github.com/csia-pme/a-guide-to-mlops/tree/main/docs/advanced-concepts/train-the-model-on-a-kubernetes-cluster-with-cml).
