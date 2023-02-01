---
title: "Chapter 7: Track model evolutions in the CI/CD pipeline with CML"
---

# {% $markdoc.frontmatter.title %}

## Introduction

The purpose of this chapter is to track the model evolutions and generate reports directly in the CI/CD pipeline so it can be discussed collectively online before commiting the changes to the codebase.

In this chapter, you'll cover:

1. Updating the CI/CD configuration file to generate a CML report
2. Pushing the updated CI/CD configuration file to Git
3. Opening an issue in your issue tracker
4. Creating a new branch to add your changes
5. Checking out to the new branch
6. Commiting and pushing the changes that were not commited in [Chapter 5: Track model evolutions with DVC](/the-guide/chapter-5-track-model-evolutions-with-dvc)
7. Creating a pull request/merge request
8. Visualizing the execution of the CI/CD pipeline
9. Visualizing the CML report that is added to your pull request/merge request
10. Merging the pull request/merge request to the main branch
11. Switching back to the main branch and pulling latest changes

{% callout type="note" %}
CML can do much more than just generating reports. Have a look to the [Train the model on a Kubernetes cluster with CML](/advanced-concepts/train-the-model-on-a-kubernetes-cluster-with-cml) guide.
{% /callout %}

## Steps

{% callout type="warning" %}
This guide has been written with macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use [GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

The reports generated by CML compare the current run with a target reference.

The target reference can be a specific commit (what are the differences between the current run and the run from the target commit) or a branch (what are the differences between the current run and the run from the target branch).

Many workflows exist to discuss and integrate the work done to a target reference. For the sake of simplicity, in this guide, we will present two methods that are commonly used on GitHub - pull requests (PRs) - and GitLab - merge requests (MRs) - to integrate the work done to the `main` branch.

### GitHub

{% callout type="note" %}
Using GitLab? Go to the [GitLab](#gitlab) section!
{% /callout %}

#### Update GitHub Actions configuration file

The new "report" job is responsible for reporting the results of the model evaluation and comparing it with the main branch.

This job is triggered only when a pull request is opened and all future commits made to it.

The job checks out the repository, downloads the evaluation results, sets up DVC and CML, creates a report using the data obtained from the training job, and finally publishes the report as a pull request comment.

Update the `.github/workflows/mlops.yml` file.

```yaml
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
          path: evaluation
          retention-days: 5

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
      - name: Download evaluation results
        uses: actions/download-artifact@v3
      - name: Copy evaluation results
        shell: bash
        run: |
          # Delete current evaluation results
          rm -rf evaluation
          # Replace with the new evaluation results
          mv artifact evaluation
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

Explore this file to understand the updated jobs and the steps.

This GitHub Workflow will create CML reports on each pushes that are related to a pull request.

Check the differences with Git to validate the changes.

```sh
# Show the differences with Git
git diff .github/workflows/mlops.yml
```

The output should be similar to this.

```diff
diff --git a/.github/workflows/mlops.yml b/.github/workflows/mlops.yml
index 0ca4d29..9275231 100644
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
 
@@ -36,3 +39,95 @@ jobs:
           dvc pull
           # Run the experiment
           dvc repro
+      - name: Upload evaluation results
+        uses: actions/upload-artifact@v3
+        with:
+          path: evaluation
+          retention-days: 5
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
+      - name: Download evaluation results
+        uses: actions/download-artifact@v3
+      - name: Copy evaluation results
+        shell: bash
+        run: |
+          # Delete current evaluation results
+          rm -rf evaluation
+          # Replace with the new evaluation results
+          mv artifact evaluation
+      - name: Setup DVC
+        uses: iterative/setup-dvc@v1
+        with:
+          version: '2.37.0'
+      - name: Setup CML
+        uses: iterative/setup-cml@v1
+        with:
+          version: '0.18.17'
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
+          # Publish the CML report
+          cml comment create --target=pr --publish report.md
```

#### Push the changes to GitHub

```sh
# Add the updated workflow
git add .github/workflows/mlops.yml

# Commit the changes
git commit -m "Enable CML reports on pull requests"

# Push the changes
git push
```

#### Open an issue on GitHub

Create a new issue by going to the **Issues** section from the top header of your GitHub repository. Select **New issue** and describe the work/improvements/ideas that you want to integrate to the codebase. In this guide, we will name the issue _Demonstrate chapter 7_. Create the issue by selecting **Submit new issue**.

The issue opens.

#### Create a branch on GitHub

On the newly created issue, select **Create a branch for this issue or link a pull request** from the right sidebar. Create the branch by selecting **Create branch**. A new pop-up opens with the name of the branch you want to checkout to.

#### Checkout the new GitHub branch

On your machine, check out the new branch.

```sh
# Get the latest updates from the remote origin
git fetch origin

# Check to the new branch
git checkout <the name of the new branch>
```

#### Check the changes

Check the changes with Git to ensure all wanted files are here.

```sh
# Add all the files
git add .

# Check the status
git status
```

The output of the `git status` command should be similar to this.

```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   .gitignore
        modified:   dvc.lock
        modified:   evaluation/metrics.json
        modified:   evaluation/plots/importance.png
        modified:   evaluation/plots/metrics/avg_prec.tsv
        modified:   evaluation/plots/metrics/roc_auc.tsv
        modified:   evaluation/plots/prc.json
        modified:   evaluation/plots/sklearn/confusion_matrix.json
        modified:   evaluation/plots/sklearn/roc.json
        modified:   evaluation/report.html
        modified:   params.yaml
```

#### Commit and push the experiment changes to GitHub

Remember the changes done in [Chapter 5: Track model evolutions with DVC](/the-guide/chapter-5-track-model-evolutions-with-dvc)?

You can now commit them to trigger a change on the remote repository.

If you don't have changes in your working directory, just update the paramerters of the experiment in `params.yaml` and reproduce the experiment with `dvc repro`. You can then commit the changes.

```sh
# Upload the experiment data and cache to the remote bucket
dvc push

# Commit the changes
git commit -m "I made some changes to the model"

# Push the changes
git push
```

#### Create a pull request on GitHub

Go back to your GitHub repository. A new **Compare & pull request** button should automatically display.

Click on it. Name the pull request and select **Create pull request** to create the pull request.

#### Visualize the execution of the CI/CD pipeline on GitHub

The pull request opens and automatically starts the workflow `MLOps / train (pull_request)` under the **Some checks haven’t completed yet** section. You can click on **Details** to see the details.

Explore the output and try to see how the configuration file shows up in GitHub.

Once the workflow is done, a new workflow `MLOps / report (pull_request)` is started under the **Some checks haven’t completed yet** section. You can click on **Details** to see the details.

Explore the output and try to see how the configuration file shows up in GitHub.

Once all workflows are successfully executed, the **Some checks haven't completed yet** section should become **All checks have passed**.

#### Visualize the CML report on GitHub

When the CI/CD pipeline completes, a new comment is added to your pull request. Check the pull request and examine the report made by CML. As it uses the evaluation data that was generated with DVC, it can uses it to display all the plots.

#### Merging the pull request on GitHub

Once you are satisfied with the model's performance, you can merge the changes. 

Go back to the pull request. At the end of the page, select **Merge pull request**. Confirm the merge by selecting **Confirm merge**.

The associated issue will be automatically closed as well.

You can delete the branch by clicking **Delete branch** to clean up your repository. If you ever need to go back to this branch, you can always restore the branch from this menu.

Congrats! You can now iterate on your model while keeping a trace of the improvements made to it. You can visualize and discuss the changes made to a model before adding the changes to the codebase.

{% callout type="note" %}
Finished? Go to the [Switch back to the main branch](#switch-back-to-the-main-branch) step!
{% /callout %}

### GitLab

{% callout type="note" %}
Using GitHub? Go to the [GitHub](#github) section!
{% /callout %}

#### Create a Personal Access Token

In order to allow CML to generate reports, a Personal Access Token (PAT) must be created. A Project or a Group Access Token are not sufficient for the usage of CML's runners that will be used in the next steps.

To create a Personal Access Token, go in your **Profile preferences > Access Tokens**.

**Token name**: _CML_
**Expiration date**: _None_
**Select scopes**: `api`, `read_repository` and `write_repository`

Select **Create personal access token** to create the token. Copy it. It will be displayed only once.

Store the PAT as a CI/CD Variable by going to **Settings > CI/CD** from the left sidebar of your GitLab project.

Select **Variables** and select **Add variable**.

Create a new variable named `CML_PAT_TOKEN` with the PAT value as its value.

- **Protect variable**: _Unchecked_
- **Mask variable**: _Checked_
- **Expand variable reference**: _Unchecked_

Save the variable by clicking **Add variable**.

#### Update GitLab CI configuration file

The new "report" job is responsible for reporting the results of the model evaluation and comparing it with the main branch.

This job is triggered only when a merge request is opened and all future commits made to it.

The job checks out the repository, downloads the evaluation results, sets up DVC and CML, creates a report using the data obtained from the training job, and finally publishes the report as a merge request comment.

Update the `.gitlab-ci.yml` file.

```yaml
stages:
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
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  variables:
    REPO_TOKEN: $CML_PAT_TOKEN
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

Explore this file to understand the updated stages and the steps.

This GitLab CI will create CML reports on each pushes that are related to a merge request.

Check the differences with Git to validate the changes.

```sh
# Show the differences with Git
git diff .gitlab-ci.yml
```

The output should be similar to this.

```diff
diff --git a/.gitlab-ci.yml b/.gitlab-ci.yml
index 561d04f..61dea20 100644
--- a/.gitlab-ci.yml
+++ b/.gitlab-ci.yml
@@ -1,5 +1,6 @@
 stages:
   - train
+  - report
 
 variables:
   # Change pip's cache directory to be inside the project directory since we can
@@ -33,3 +34,73 @@ train:
     - dvc pull
     # Run the experiment
     - dvc repro
+  artifacts:
+    expire_in: 1 week
+    paths:
+      - "evaluation"
+
+report:
+  stage: report
+  image: iterativeai/cml:0-dvc2-base1
+  needs:
+    - job: train
+      artifacts: true
+  rules:
+    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
+  variables:
+    REPO_TOKEN: $CML_PAT_TOKEN
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
+      # Publish the CML report
+      cml comment create --target=pr --publish report.md
```

#### Push the changes to GitLab

```sh
# Add the updated GitLab CI
git add .gitlab-ci.yml

# Commit the changes
git commit -m "Enable CML reports on merge requests"

# Push the changes
git push
```

#### Open an issue on GitLab

Create a new issue by going to the **Issues** section from the left sidebar of your GitLab project. Select **New issue** and describe the work/improvements/ideas that you want to integrate to the codebase. In this guide, we will name the issue _Demonstrate chapter 7_. Create the issue by selecting **Submit new issue**.

The issue opens.

#### Create a merge request on GitLab

Select **Create merge request** and change the merge request configuration if needed. Create the merge request by selecting **Create merge request**.

#### Checkout the new GitLab branch

On your machine, check out the new branch.

```sh
# Get the latest updates from the remote origin
git fetch origin

# Check to the new branch
git checkout <the name of the new branch>
```

#### Check the changes

Check the changes with Git to ensure all wanted files are here.

```sh
# Add all the files
git add .

# Check the status
git status
```

The output of the `git status` command should be similar to this.

```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   .gitignore
        modified:   dvc.lock
        modified:   evaluation/metrics.json
        modified:   evaluation/plots/importance.png
        modified:   evaluation/plots/metrics/avg_prec.tsv
        modified:   evaluation/plots/metrics/roc_auc.tsv
        modified:   evaluation/plots/prc.json
        modified:   evaluation/plots/sklearn/confusion_matrix.json
        modified:   evaluation/plots/sklearn/roc.json
        modified:   evaluation/report.html
        modified:   params.yaml
```

#### Commit and push the experiment changes to GitLab

Remember the changes done in [Chapter 5: Track model evolutions with DVC](/the-guide/chapter-5-track-model-evolutions-with-dvc)?

You can now commit them to trigger a change on the remote repository.

If you don't have changes in your working directory, just update the paramerters of the experiment in `params.yaml` and reproduce the experiment with `dvc repro`. You can then commit the changes.

```sh
# Upload the experiment data and cache to the remote bucket
dvc push

# Commit the changes
git commit -m "I made some changes to the model"

# Push the changes
git push
```

#### Visualize the execution of the CI/CD pipeline on GitLab

Open the merge request. The pipeline should start. Click on the pipeline number to see the details of the pipeline.

Explore the stages and jobs and try to see how the configuration file shows up in GitLab.

#### Visualize the CML report on GitLab

When the CI/CD pipeline completes, a new comment is added to your merge request. Check the merge request and examine the report made by CML. As it uses the evaluation data that was generated with DVC, it can uses it to display all the plots.

#### Merging the merge request on GitLab

Once you are satisfied with the model's performance, you can merge the changes. 

Go back to the merge request. Select **Mark as ready**. This will allow to merge the changes. Confirm the merge by selecting **Merge** (you might need to refresh the page to see this button).

The associated issue will be automatically closed as well.

Congrats! You can now iterate on your model while keeping a trace of the improvements made to it. You can visualize and discuss the changes made to a model before adding the changes to the codebase.

{% callout type="note" %}
Finished? Go to the [Switch back to the main branch](#switch-back-to-the-main-branch) step!
{% /callout %}

### Switch back to the main branch and pull latest changes

Now that the merge is done, you can get the changes on the main branch.

```sh
# Get the latest updates from the remote origin
git fetch origin

# Check to the main branch
git checkout main

# Pull the changes made by the pull request/merge request
git pull
```

This chapter is done, you can check the summary.

## Summary

In this chapter, you have successfully:

1. Updated the CI/CD configuration file to generate a CML report
2. Pushed the updated CI/CD configuration file to Git
3. Opened an issue in your issue tracker
4. Created a new branch to add your changes
5. Checked out to the new branch
6. Commit and pushed the changes that were not commited in [Chapter 5: Track model evolutions with DVC](/the-guide/chapter-5-track-model-evolutions-with-dvc)
7. Created a pull request/merge request
8. Visualized the execution of the CI/CD pipeline
9. Visualized the CML report that is added to your pull request/merge request
10. Merged the pull request/merge request to the main branch
11. Switched back to the main branch and pulled latest changes

However, you might have identified the following areas for improvement:

- ❌ How can I serve my model to the rest of the world?

In the next chapters, you will enhance the workflow to fix those issues.

You can now safely continue to the next chapter.

## State of the MLOps process

- ✅ The codebase can be shared and improved by multiple developers;
- ✅ The dataset can be shared among the developers and is placed in the right directory in order to run the experiment;
- ✅ The steps used to create the model are documented and can be re-executed;
- ✅ The changes done to a model can be visualized with parameters, metrics and plots to identify differences between iterations;
- ✅ The experiment can be executed on a clean machine with the help of a CI/CD pipeline and CML;
- ❌ Model may have required artifacts that are forgotten or omitted in saved/loaded state. There is no easy way to use the model outside of the experiment context.

## Sources

Highly inspired by the [_Get Started with CML on GitHub_ - cml.dev](https://cml.dev/doc/start/github), [_Creating an issue_ - docs.github.com](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue), [_Creating a branch to work on an issue_ - docs.github.com](https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-a-branch-for-an-issue), [_Get Started with CML on GitLab_ - cml.dev](https://cml.dev/doc/start/gitlab), [_Personal access tokens_ - docs.gitlab.com](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) guides and the [`example_cml` - github.com](https://github.com/iterative/example_cml), [`cml_dvc_case` - github.com](https://github.com/iterative/cml_dvc_case), [`example_cml` - gitlab.com](https://gitlab.com/iterative.ai/example_cml), [`cml-dvc-case` - gitlab.com](https://gitlab.com/iterative.ai/cml-dvc-case) Git repositories.

Want to see what the result at the end of this chapter should look like? Have a look at the Git repository directory here: [chapter-7-track-model-evolutions-in-the-cicd-pipeline-with-cml](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/chapter-7-track-model-evolutions-in-the-cicd-pipeline-with-cml).

## Next & Previous chapters

- **Previous**: [Chapter 6: Orchestrate the workflow with a CI/CD pipeline](/the-guide/chapter-6-orchestrate-the-workflow-with-a-cicd-pipeline)
- **Next**: [Chapter 8: Serve the model with MLEM](/the-guide/chapter-8-serve-the-model-with-mlem)