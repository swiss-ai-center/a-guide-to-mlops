# Chapter 13: Train the model on a Kubernetes pod with CML

??? info "You want to take over from this chapter? Collapse this section and follow the instructions below."

    _Work in progress._

    [//]: # "TODO"

## Introduction

Some experiments can require specific hardware to run. For example, you may need a GPU to train a deep learning model.

Training these experiments locally can be challenging. You may not have the required hardware, or you may not want to use your local machine for training. In this case, you can use a specialized Kubernetes pod to train your model.

In this chapter, you will learn how to train the model on a Kubernetes pod with CML.

In this chapter, you will learn how to:

1. Configure CML to start a runner on Kubernetes
2. Start the training of the model from your CI/CD pipeline on the Kubernetes cluster

## Steps

### Display the nodes names and labels

Display the nodes with the following command.

```sh title="Execute the following command(s) in a terminal"
kubectl get nodes --show-labels
```

The output should be similar to this. As noticed, you have two nodes in your cluster with their labels.

```
NAME                                              STATUS   ROLES    AGE   VERSION            LABELS
gke-mlops-kubernetes-default-pool-d4f966ea-8rbn   Ready    <none>   49s   v1.24.9-gke.3200   beta.kubernetes.io/arch=amd64,[...]
gke-mlops-kubernetes-default-pool-d4f966ea-p7qm   Ready    <none>   50s   v1.24.9-gke.3200   beta.kubernetes.io/arch=amd64,[...]
```

Export the name of the two nodes as environment variables. Replace the `<your node 1 name>` and `<your node 2 name>` placeholders with the names of your nodes (`gke-mlops-kubernetes-default-pool-d4f966ea-8rbn` and `gke-mlops-kubernetes-default-pool-d4f966ea-p7qm` in this example).

```sh title="Execute the following command(s) in a terminal"
export K8S_NODE_1_NAME=<your node 1 name>
```

```sh title="Execute the following command(s) in a terminal"
export K8S_NODE_2_NAME=<your node 2 name>
```

### Labelize the nodes

Let's imagine one node has a GPU and the other one doesn't. You can labelize the nodes to be able to use the GPU node for the training of the model. For our expiriment, there is no need to have a GPU to train the model but it's for demonstration purposes.

```sh title="Execute the following command(s) in a terminal"
kubectl label nodes $K8S_NODE_1_NAME gpu=true
kubectl label nodes $K8S_NODE_2_NAME gpu=false
```

You can check the labels with the `kubectl get nodes --show-labels` command. You should see the node with the `gpu=true`/`gpu=false` labels.

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

	```yaml title=".github/workflows/mlops.yml" hl_lines="15-18 21-51 54-56"
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
	      - uses: iterative/setup-cml@v1
	        with:
	          version: '0.19.0'
	      - name: Initialize runner on Kubernetes
	        env:
	          REPO_TOKEN: ${{ secrets.CML_PAT }}
	        run: |
	          export KUBERNETES_CONFIGURATION=$(cat $KUBECONFIG)
	          # https://cml.dev/doc/ref/runner
	          # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resources/task#machine-type
	          # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resources/task#{cpu}-{memory}
	          cml runner \
	            --labels="cml-runner" \
	            --cloud="kubernetes" \
	            --cloud-type="1-2000" \
	            --cloud-kubernetes-node-selector="gpu=true" \
	            --single

	  train:
	    needs: setup-runner
	    runs-on: [self-hosted, cml-runner]
	    timeout-minutes: 50400 # 35 days
	    steps:
	      - name: Checkout repository
	        uses: actions/checkout@v3
	      - name: Install poetry
	        run: pip install poetry==1.4.0
	      - name: Setup Python
	        uses: actions/setup-python@v4
	        with:
	          python-version: '3.10'
	          cache: 'poetry'
	      - name: Install dependencies
	        run: poetry install
	      - name: Enable Poetry virtual environment
	        run: source `poetry env info --path`/bin/activate
	      - name: Setup DVC
	        uses: iterative/setup-dvc@v1
	        with:
	          version: '2.37.0'
	      - name: Login to Google Cloud
	        uses: 'google-github-actions/auth@v1'
	        with:
	          credentials_json: '${{ secrets.GCP_SERVICE_ACCOUNT_KEY }}'
	      - name: Train model
	        run: |
	          # Pull data from DVC
	          dvc pull
	          # Run the experiment
	          dvc repro --force

	  report:
	    permissions: write-all
	    needs: train
	    if: github.event_name == 'pull_request'
	    runs-on: ubuntu-latest
	    steps:
	      - name: Checkout repository
	        uses: actions/checkout@v3
	        with:
	          ref: ${{ github.event.pull_request.head.sha }}
	      - name: Setup DVC
	        uses: iterative/setup-dvc@v1
	        with:
	          version: '2.37.0'
	      - name: Login to Google Cloud
	        uses: 'google-github-actions/auth@v1'
	        with:
	          credentials_json: '${{ secrets.GCP_SERVICE_ACCOUNT_KEY }}'
	      - name: Setup CML
	        uses: iterative/setup-cml@v1
	        with:
	          version: '0.19.0'
	      - name: Create CML report
	        env:
	          REPO_TOKEN: ${{ secrets.GITHUB_TOKEN }}
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

	          echo "## Importance" >> report.md
	          echo >> report.md
	          dvc plots diff --target evaluation/plots/importance.png -- main
	          echo '![](./dvc_plots/static/main_evaluation_plots_importance.png "Importance (main)")' >> report.md
	          echo >> report.md
	          echo '![](./dvc_plots/static/workspace_evaluation_plots_importance.png "Importance (workspace)")' >> report.md
	          echo >> report.md

	          # Publish the CML report
	          cml comment update --target=pr --publish report.md
	```

	Check the differences with Git to validate the changes.

	```sh title="Execute the following command(s) in a terminal"
	# Show the differences with Git
	git diff .github/workflows/mlops.yml
	```

	The output should be similar to this:

	```diff
	diff --git a/.github/workflows/mlops.yml b/.github/workflows/mlops.yml
	index f79856a..ce556c7 100644
	--- a/.github/workflows/mlops.yml
	+++ b/.github/workflows/mlops.yml
	@@ -12,9 +12,46 @@ on:
	   # Allows you to run this workflow manually from the Actions tab
	   workflow_dispatch:

	+# Allow the creation and usage of self-hosted runners
	+permissions:
	+  contents: read
	+  id-token: write
	+
	 jobs:
	-  train:
	+  setup-runner:
	     runs-on: ubuntu-latest
	+    container: iterativeai/cml:0-dvc2-base1
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

	```yaml title=".gitlab-ci.yml" hl_lines="2 22-43 48-52"
	stages:
	  - setup runner
	  - train
	  - report

	variables:
	  # Change pip's cache directory to be inside the project directory since we can
	  # only cache local items.
	  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
	  # https://dvc.org/doc/user-guide/troubleshooting?tab=GitLab-CI-CD#git-shallow
	  GIT_DEPTH: "0"
	  # https://python-poetry.org/docs/#ci-recommendations
	  POETRY_HOME: "$CI_PROJECT_DIR/.cache/poetry"

	# Pip's cache doesn't store the python packages
	# https://pip.pypa.io/en/stable/reference/pip_install/#caching
	cache:
	  paths:
	    - .cache/pip
	    - .cache/poetry

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
	    # https://cml.dev/doc/ref/runner
	    # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resources/task#machine-type
	    # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resources/task#{cpu}-{memory}
	    - cml runner
	        --labels="cml-runner"
	        --cloud="kubernetes"
	        --cloud-type="1-2000"
	        --cloud-kubernetes-node-selector="gpu=true"
	        --single

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
	    # Set the path to Google Service Account key for DVC - https://dvc.org/doc/command-reference/remote/	add#google-cloud-storage
	    GOOGLE_APPLICATION_CREDENTIALS: "${CI_PROJECT_DIR}/google-service-account-key.json"
	  before_script:
	    # Set the Google Service Account key
	    - echo "${GCP_SERVICE_ACCOUNT_KEY}" | base64 -d > $GOOGLE_APPLICATION_CREDENTIALS
	    # Install Poetry
	    - pip install poetry==1.4.0
	    # Install dependencies
	    - poetry install
	    - source `poetry env info --path`/bin/activate
	  script:
	    # Pull data from DVC
	    - dvc pull
	    # Run the experiment
	    - dvc repro --force
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
	      cml comment update --target=pr --publish report.md
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

	@@ -18,9 +19,37 @@ cache:
	     - .cache/pip
	     - .cache/poetry

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
	+    # https://cml.dev/doc/self-hosted-runners?tab=Kubernetes#cloud-compute-resource-c
	redentials
	+    - export KUBERNETES_CONFIGURATION=$(cat $GCP_KUBECONFIG)
	+  script:
	+    # https://cml.dev/doc/ref/runner#--cloud-type
	+    # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resourc
	es/task#machine-type
	+    # https://registry.terraform.io/providers/iterative/iterative/latest/docs/resourc
	es/task#{cpu}-{memory}
	+    - cml runner
	+        --labels="cml-runner"
	+        --cloud="kubernetes"
	+        --cloud-type="1-2000"
	+        --cloud-kubernetes-node-selector="gpu=true"
	+        --single
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

The pod should be created on the Kubernetes Cluster.


=== ":simple-amazonaws: Amazon Web Services"

	TODO

=== ":simple-googlecloud: Google Cloud"

    On Google Cloud Console, you can see the pod that has been created on the **Kubernetes Engine > Workloads** page. Open the pod and go to the **YAML** tab to see the configuration of the pod. You should notice that the pod has been created with the node selector `gpu=true` and that it has been created on the right node.

=== ":simple-microsoftazure: Microsoft Azure"

	TODO

=== ":simple-rancher: Self-hosted Rancher"

	TODO

This chapter is done, you can check the summary.

## Summary

Congrats! You now can train your model on on a custom infrastructure with custom hardware for specific use-cases.

In this chapter, you have successfully:

1. Created a Kubernetes cluster on Google Cloud
2. Configured CML to start a runner on Kubernetes
3. Trained the model on the Kubernetes cluster

For more information, you can check the following resources: [CML Command Reference: `runner` #Using `--cloud-kubernetes-node-selector`](https://cml.dev/doc/ref/runner#using---cloud-kubernetes-node-selector).

### Destroy the Kubernetes cluster

When you are done with the chapter, you can destroy the Kubernetes cluster.

```sh title="Execute the following command(s) in a terminal"
gcloud container clusters delete --zone europe-west6-a mlops-kubernetes
```

## State of the MLOps process

- [x] Notebook has been transformed into scripts for production
- [x] Codebase and dataset are versioned
- [x] Steps used to create the model are documented and can be re-executed
- [x] Changes done to a model can be visualized with parameters, metrics and plots to identify
differences between iterations
- [x] Dataset can be shared among the developers and is placed in the right
directory in order to run the experiment
- [x] Codebase can be shared and improved by multiple developers
- [x] Experiment can be executed on a clean machine with the help of a CI/CD
pipeline
- [x] Changes to model can be thoroughly reviewed and discussed before integrating them into the codebase
- [x] Model can be saved and loaded with all required artifacts for future usage
- [x] Model can be easily used outside of the experiment context.
- [x] Model can be accessed from a Kubernetes cluster
- [x] Model can be trained on a custom infrastructure with custom hardware for specific use-cases

You can now safely continue to the next chapter of this guide concluding your
journey and the next things you could do with your model.

## Sources

Highly inspired by the [_Self-hosted (On-premise or Cloud) Runners_ - cml.dev](https://cml.dev/doc/self-hosted-runners), [_Install kubectl and configure cluster access_ - cloud.google.com](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl), [_gcloud container clusters create_ - cloud.google.com](https://cloud.google.com/sdk/gcloud/reference/container/clusters/create), the [_Install Tools_ - kubernetes.io](https://kubernetes.io/docs/tasks/tools/), [_Assigning Pods to Nodes_ - kubernetes.io](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector) and [_Assign Pods to Nodes_ - kubernetes.io](https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes/) guides.

Want to see what the result at the end of this chapter should look like? Have a
look at the Git repository directory here:
[train-the-model-on-a-kubernetes-cluster-with-cml](https://github.com/csia-pme/a-guide-to-mlops/tree/main/docs/advanced-concepts/train-the-model-on-a-kubernetes-cluster-with-cml).
