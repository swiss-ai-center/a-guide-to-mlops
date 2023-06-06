# Chapter 7: Track model evolutions in the CI/CD pipeline with CML

## Introduction

[moved]

## Steps

[moved]

### Update the CI/CD pipeline configuration file

=== ":simple-github: GitHub"

	Update the `.github/workflows/mlops.yml` file.

	Take some time to understand the report job and its steps.

	```yaml  title=".github/workflows/mlops.yml" hl_lines="9-10 41-133"
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

	jobs:
	  train:
	    runs-on: ubuntu-latest
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
	      - name: Login to Google Cloud
	        uses: 'google-github-actions/auth@v1'
	        with:
	          credentials_json: '${{ secrets.GCP_SERVICE_ACCOUNT_KEY }}'
	      - name: Train model
	        run: |
	          # Pull data from DVC
	          poetry run dvc pull
	          # Run the experiment
	          poetry run dvc repro

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
	      - name: Setup Node
	        uses: actions/setup-node@v3
	        with:
	          node-version: '16'
	      - name: Setup CML
	        uses: iterative/setup-cml@v1
	        with:
	          version: '0.18.17'
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

	You may notice that the `report` job doesn't use Poetry. As we do not need to reproduce the experiment, we can install DVC using the `iterative/setup-dvc@v1` GitHub action without Poetry. DVC will then retrieve the data stored on the bucket on its own.

	Check the differences with Git to validate the changes.

	```sh title="Execute the following command(s) in a terminal"
	# Show the differences with Git
	git diff .github/workflows/mlops.yml
	```

	The output should be similar to this:

	```diff
	diff --git a/.github/workflows/mlops.yml b/.github/workflows/mlops.yml
	index f4232c9..9041212 100644
	--- a/.github/workflows/mlops.yml
	+++ b/.github/workflows/mlops.yml
	@@ -6,6 +6,9 @@ on:
		branches:
		- main

	+  # Runs on pull requests
	+  pull_request:
	+
	# Allows you to run this workflow manually from the Actions tab
	workflow_dispatch:

	@@ -34,3 +37,93 @@ jobs:
			poetry run dvc pull
			# Run the experiment
			poetry run dvc repro
	+
	+  report:
	+    permissions: write-all
	+    needs: train
	+    if: github.event_name == 'pull_request'
	+    runs-on: ubuntu-latest
	+    steps:
	+      - name: Checkout repository
	+        uses: actions/checkout@v3
	+        with:
	+          ref: ${{ github.event.pull_request.head.sha }}
	+      - name: Setup DVC
	+        uses: iterative/setup-dvc@v1
	+        with:
	+          version: '2.37.0'
	+      - name: Login to Google Cloud
	+        uses: 'google-github-actions/auth@v1'
	+        with:
	+          credentials_json: '${{ secrets.GCP_SERVICE_ACCOUNT_KEY }}'
	+      - name: Setup CML
	+        uses: iterative/setup-cml@v1
	+        with:
	+          version: '0.18.17'
	+      - name: Setup Node
	+        uses: actions/setup-node@v3
	+        with:
	+          node-version: '16'
	+      - name: Create CML report
	+        env:
	+          REPO_TOKEN: ${{ secrets.GITHUB_TOKEN }}
	+        run: |
	+          # Fetch all other Git branches
	+          git fetch --depth=1 origin main:main
	+
	+          # Compare parameters to main branch
	+          echo "# Params workflow vs. main" >> report.md
	+          echo >> report.md
	+          dvc params diff main --show-md >> report.md
	+          echo >> report.md
	+
	+          # Compare metrics to main branch
	+          echo "# Metrics workflow vs. main" >> report.md
	+          echo >> report.md
	+          dvc metrics diff main --show-md >> report.md
	+          echo >> report.md
	+
	+          # Create plots
	+          echo "# Plots" >> report.md
	+          echo >> report.md
	+
	+          echo "## Precision recall curve" >> report.md
	+          echo >> report.md
	+          dvc plots diff \
	+            --target evaluation/plots/prc.json \
	+            -x recall \
	+            -y precision \
	+            --show-vega main > vega.json
	+          vl2png vega.json > prc.png
	+          echo '![](./prc.png "Precision recall curve")' >> report.md
	+          echo >> report.md
	+
	+          echo "## Roc curve" >> report.md
	+          echo >> report.md
	+          dvc plots diff \
	+            --target evaluation/plots/sklearn/roc.json \
	+            -x fpr \
	+            -y tpr \
	+            --show-vega main > vega.json
	+          vl2png vega.json > roc.png
	+          echo '![](./roc.png "Roc curve")' >> report.md
	+          echo >> report.md
	+
	+          echo "## Confusion matrix" >> report.md
	+          echo >> report.md
	+          dvc plots diff \
	+            --target evaluation/plots/sklearn/confusion_matrix.json \
	+            --template confusion \
	+            -x actual \
	+            -y predicted \
	+            --show-vega main > vega.json
	+          vl2png vega.json > confusion_matrix.png
	+          echo '![](./confusion_matrix.png "Confusion Matrix")' >> report.md
	+          echo >> report.md
	+
	+          echo "## Importance" >> report.md
	+          echo >> report.md
	+          dvc plots diff --target evaluation/plots/importance.png -- main
	+          echo '![](./dvc_plots/static/main_evaluation_plots_importance.png "Importance (main)")' >> report.md
	+          echo >> report.md
	+          echo '![](./dvc_plots/static/workspace_evaluation_plots_importance.png "Importance (workspace)")' >> report.md
	+          echo >> report.md
	+
	+          # Publish the CML report
	+          cml comment update --target=pr --publish report.md
	```

	The new `report` job is responsible for reporting the results of the model
	evaluation and comparing it with the main branch. This job is triggered only
	when a pull request is opened and commits are made to it. The job checks out the
	repository, sets up DVC and CML, creates and publishes the report as a pull request comment.

	Take some time to understand the changes made to the file.

=== ":simple-gitlab: GitLab"

	In order to allow CML to generate reports, a Personal Access Token (PAT) must be
	created. A Project or a Group Access Token are not sufficient for the usage of
	CML's runners that will be used in the next steps.

	To create a Personal Access Token, go in your **Profile preferences > Access
	Tokens**.

	- **Token name**: _CML_
	- **Expiration date**: _None_
	- **Select scopes**: `api`, `read_repository` and `write_repository`

	Select **Create personal access token** to create the token. Copy it. It will be
	displayed only once.

	Store the PAT as a CI/CD Variable by going to **Settings > CI/CD** from the left
	sidebar of your GitLab project.

	Select **Variables** and select **Add variable**.

	Create a new variable named `CML_PAT` with the PAT value as its value.

	- **Protect variable**: _Unchecked_
	- **Mask variable**: _Checked_
	- **Expand variable reference**: _Unchecked_

	Save the variable by clicking **Add variable**.

	Update the `.gitlab-ci.yml` file.

	Explore this file to understand the report stage and its steps.

	```yaml title=".gitlab-ci.yml" hl_lines="3 44-119"
	stages:
	  - train
	  - report

	variables:
	  # Change pip's cache directory to be inside the project directory since we can
	  # only cache local items.
	  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
	  # Change poetry's cache directory to be inside the project directory since we can
	  # only cache local items.
	  POETRY_CACHE_DIR: "$CI_PROJECT_DIR/.cache/poetry"
	  # https://dvc.org/doc/user-guide/troubleshooting?tab=GitLab-CI-CD#git-shallow
	  GIT_DEPTH: "0"

	# Pip's cache doesn't store the python packages
	# https://pip.pypa.io/en/stable/reference/pip_install/#caching
	cache:
	  paths:
	    - .cache/pip
	    - .cache/poetry

	train:
	  stage: train
	  image: iterativeai/cml:0-dvc2-base1
	  rules:
	    - if: $CI_COMMIT_BRANCH == "main"
	    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
	  variables:
	    # Set the path to Google Service Account key for DVC - https://dvc.org/doc/command-reference/remote/add#google-cloud-storage
	    GOOGLE_APPLICATION_CREDENTIALS: "${CI_PROJECT_DIR}/google-service-account-key.json"
	  before_script:
	    # Set the Google Service Account key
	    - echo "${GCP_SERVICE_ACCOUNT_KEY}" | base64 -d > $GOOGLE_APPLICATION_CREDENTIALS
	    # Install Poetry
	    - pip install poetry==1.4.0
	    # Install dependencies
	    - poetry install
	  script:
	    # Pull data from DVC
	    - poetry run dvc pull
	    # Run the experiment
	    - poetry run dvc repro

	report:
	  stage: report
	  image: iterativeai/cml:0-dvc2-base1
	  needs:
	    - train
	  rules:
	    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
	  variables:
	    # Set the path to Google Service Account key for DVC - https://dvc.org/doc/command-reference/remote/add#google-cloud-storage
	    GOOGLE_APPLICATION_CREDENTIALS: "${CI_PROJECT_DIR}/google-service-account-key.json"
	    REPO_TOKEN: $CML_PAT
	  before_script:
	    # Set the Google Service Account key
	    - echo "${GCP_SERVICE_ACCOUNT_KEY}" | base64 -d > $GOOGLE_APPLICATION_CREDENTIALS
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

	You may notice that the `report` stage doesn't use Poetry. As we do not need to reproduce the experiment, we can use DVC from the `iterativeai/cml:0-dvc2-base1` Docker image without Poetry. DVC will then retrieve the data stored on the bucket on its own.

	Check the differences with Git to validate the changes.

	```sh title="Execute the following command(s) in a terminal"
	# Show the differences with Git
	git diff .gitlab-ci.yml
	```

	The output should be similar to this:

	```diff
	diff --git a/.gitlab-ci.yml b/.gitlab-ci.yml
	index aa15df3..0587f9b 100644
	--- a/.gitlab-ci.yml
	+++ b/.gitlab-ci.yml
	@@ -1,5 +1,6 @@
	stages:
	- train
	+  - report

	variables:
	# Change pip's cache directory to be inside the project directory since we can
	@@ -34,8 +35,87 @@ train:
		- pip install poetry==1.4.0
		# Install dependencies
		- poetry install
	script:
		# Pull data from DVC
		- poetry run dvc pull
		# Run the experiment
		- poetry run dvc repro
	+
	+report:
	+  stage: report
	+  image: iterativeai/cml:0-dvc2-base1
	+  needs:
	+    - train
	+  rules:
	+    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
	+  variables:
	+    # Set the path to Google Service Account key for DVC - https://dvc.org/doc/command-reference/remote/add#google-cloud-storage
	+    GOOGLE_APPLICATION_CREDENTIALS: "${CI_PROJECT_DIR}/google-service-account-key.json"
	+    REPO_TOKEN: $CML_PAT
	+  before_script:
	+    # Set the Google Service Account key
	+    - echo "${GCP_SERVICE_ACCOUNT_KEY}" | base64 -d > $GOOGLE_APPLICATION_CREDENTIALS
	+  script:
	+    - |
	+      # Compare parameters to main branch
	+      echo "# Params workflow vs. main" >> report.md
	+      echo >> report.md
	+      dvc params diff main --show-md >> report.md
	+      echo >> report.md
	+
	+      # Compare metrics to main branch
	+      echo "# Metrics workflow vs. main" >> report.md
	+      echo >> report.md
	+      dvc metrics diff main --show-md >> report.md
	+      echo >> report.md
	+
	+      # Create plots
	+      echo "# Plots" >> report.md
	+      echo >> report.md
	+
	+      echo "## Precision recall curve" >> report.md
	+      echo >> report.md
	+      dvc plots diff \
	+        --target evaluation/plots/prc.json \
	+        -x recall \
	+        -y precision \
	+        --show-vega main > vega.json
	+      vl2png vega.json > prc.png
	+      echo '![](./prc.png "Precision recall curve")' >> report.md
	+      echo >> report.md
	+
	+      echo "## Roc curve" >> report.md
	+      echo >> report.md
	+      dvc plots diff \
	+        --target evaluation/plots/sklearn/roc.json \
	+        -x fpr \
	+        -y tpr \
	+        --show-vega main > vega.json
	+      vl2png vega.json > roc.png
	+      echo '![](./roc.png "Roc curve")' >> report.md
	+      echo >> report.md
	+
	+      echo "## Confusion matrix" >> report.md
	+      echo >> report.md
	+      dvc plots diff \
	+        --target evaluation/plots/sklearn/confusion_matrix.json \
	+        --template confusion \
	+        -x actual \
	+        -y predicted \
	+        --show-vega main > vega.json
	+      vl2png vega.json > confusion_matrix.png
	+      echo '![](./confusion_matrix.png "Confusion Matrix")' >> report.md
	+      echo >> report.md
	+
	+      echo "## Importance" >> report.md
	+      echo >> report.md
	+      dvc plots diff --target evaluation/plots/importance.png -- main
	+      echo '![](./dvc_plots/static/main_evaluation_plots_importance.png "Importance (main)")' >> report.md
	+      echo >> report.md
	+      echo '![](./dvc_plots/static/workspace_evaluation_plots_importance.png "Importance (workspace)")' >> report.md
	+      echo >> report.md
	+
	+      # Publish the CML report
	+      cml comment update --target=pr --publish report.md
	```

	The new `report` job is responsible for reporting the results of the model
	evaluation and comparing it with the main branch. This job is triggered only
	when a merge request is opened and commits are made to it. The job checks out
	the repository, sets up DVC and CML, creates and publishes the report
	as a merge request comment.

	Take some time to understand the changes made to the file.

### Push the CI/CD pipeline configuration file to Git

[moved]

### Open an issue

[moved]

### Create a branch for the issue

[moved]

### Checkout the new branch

[moved]

### Commit and push the experiment changes

[moved]

### Create a pull request/merge request

[moved]

### Visualize the execution of the CI/CD pipeline

[moved]

### Visualize the CML report

[moved]

### Merge the pull request/merge request

[moved]

### Switch back to the main branch and pull latest changes

[moved]

## Summary

[moved]

## State of the MLOps process

- ✅ The codebase can be shared and improved by multiple developers
- ✅ The dataset can be shared among the developers and is placed in the right
  directory in order to run the experiment
- ✅ The steps used to create the model are documented and can be re-executed
- ✅ The changes done to a model can be visualized with parameters, metrics and
  plots to identify differences between iterations
- ✅ The experiment can be executed on a clean machine with the help of a CI/CD
  pipeline and CML
- ❌ Model may have required artifacts that are forgotten or omitted in
  saved/loaded state and there is no easy way to use the model outside of the
  experiment context

## Sources

Highly inspired by the [_Get Started with CML on GitHub_ -
cml.dev](https://cml.dev/doc/start/github), [_Creating an issue_ -
docs.github.com](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue),
[_Creating a branch to work on an issue_ -
docs.github.com](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-a-branch-for-an-issue),
[_Get Started with CML on GitLab_ - cml.dev](https://cml.dev/doc/start/gitlab),
[_Personal access tokens_ -
docs.gitlab.com](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)
guides and the [`example_cml` -
github.com](https://github.com/iterative/example_cml), [`cml_dvc_case` -
github.com](https://github.com/iterative/cml_dvc_case), [`example_cml` -
gitlab.com](https://gitlab.com/iterative.ai/example_cml), [`cml-dvc-case` -
gitlab.com](https://gitlab.com/iterative.ai/cml-dvc-case) Git repositories.

Want to see what the result at the end of this chapter should look like on your GitHub/GitLab Git repository? Have a
look at the Git repository directory here:
[chapter-7-track-model-evolutions-in-the-cicd-pipeline-with-cml](https://github.com/csia-pme/a-guide-to-mlops/tree/main/docs/the-guide/chapter-7-track-model-evolutions-in-the-cicd-pipeline-with-cml).
