---
title: "Step 6: Orchestrate the workflow with a CI/CD pipeline"
---

# {% $markdoc.frontmatter.title %}

## Summary

{% callout type="note" %}
Highly inspired by the [_Using service accounts_ - dvc.org](https://dvc.org/doc/user-guide/setup-google-drive-remote#using-service-accounts) guide.
{% /callout %}

At this stage, we have our code, our data and our execution process that are shared through git and dvc. 

We will now add  CI/CD pipeline to execute the ML experiment remotely, to ensure it can always be executed and to avoid the "but it works on my machine." effect.

To do so we will start by creating an IAM Service Account to grant access to the google project. Then we will create and configure the `CI/CD Pipeline` to run the `dvc pipeline` each time there is a push to main.

At the end of this step, our pipeline will prove the experiment runs in a "blank" environment after each push to main.

More functionalities offered by the CI/CD pipeline will be added in the next steps.

{% callout type="note" %}
Self-hosting your storage with MinIO? Check out the [Deploy MinIO](/advanced-concepts/deploy-minio) guide!
{% /callout %}

## Instructions

{% callout type="warning" %}
This guide has been written with macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use [GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

On the [Google Cloud console](https://console.cloud.google.com/), select **Select a project** in the upper right corner of the screen and select the project that was created in [Step 3: Share your ML experiment data with DVC](/the-guide/step-3-share-your-ml-experiment-data-with-dvc).

On the frontpage, note the project ID, it will be used later.

Create a Google Service Account by going to **IAM & Admin > Service Accounts**  on the left sidebar.

Select **Create Service Account**, name the Service Account Key (_mlopsdemo_) select **Create and continue**, select the _Viewer_ Role, select **Continue** and select **Done**.

Select the newly created service account, select **Keys** and add a new key (JSON format). Save the key under the name `google-service-account-key.json`, it will be used later.

### GitHub Actions

{% callout type="note" %}
Using GitLab? Go to the [GitLab CI](#gitlab-ci) section!
{% /callout %}

{% callout type="note" %}
Highly inspired by the [_Creating encrypted secrets for a repository_ - docs.github.com](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) guide.
{% /callout %}

Store the Google Service Account made earlier in GitHub Secrets.

```sh
# Display the Google Service Account key
cat google-service-account-key.json
```

Store the output as a CI/CD variable by going to the **Settings** section from the top header of your GitHub repository. Select **Secrets > Actions** and select **New repository secret**. Create a new variable named `GCP_SERVICE_ACCOUNT_KEY` with the output value of the Google Service Account key file as its value.Save the variable by selecting "Add secret".

At the root level of your Git repository, create a GitHub Workflow configuration file `.github/workflows/mlops.yml`.

```yaml
name: MLOps

on:
  # Runs on pushes targeting main branch
  push:
    branches:
      - main

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
```

{% callout type="note" %}
Finished? Go to the [Push to the Git repository](#push-to-the-git-repository) section!
{% /callout %}

### GitLab CI

{% callout type="note" %}
Using GitHub? Go to the [GitHub Actions](#github-actions) section!
{% /callout %}

{% callout type="note" %}
Highly inspired by the [_Add a CI/CD variable to a project_ - docs.gitlab.com](https://docs.gitlab.com/ee/ci/variables/#add-a-cicd-variable-to-a-project) guide.
{% /callout %}

Store the Google Service Account made earlier in GitLab CI variables.

```sh
# Transform the Google Service Account key to base64
base64 google-service-account-key.json
```

Store the output as a CI/CD Variable by going to **Settings > CI/CD** from the left sidebar of your GitLab project. Select **Variables** and select **Add variable**. Create a new variable named `GCP_SERVICE_ACCOUNT_KEY` with the base64 value of the Google Service Account key file as its value. Check the _"Mask variable"_ box, uncheck _"Protect variable"_ and save the variable by selecting "Add variable".

At the root level of your Git repository, create a GitLab CI configuration file `.gitlab-ci.yml`.

```yaml
stages:
  - train

# Change pip's cache directory to be inside the project directory since we can
# only cache local items.
variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

# Pip's cache doesn't store the python packages
# https://pip.pypa.io/en/stable/reference/pip_install/#caching
cache:
  paths:
    - .cache/pip

run-ml-experiment:
  stage: train
  image: iterativeai/cml:0-dvc2-base1
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
```

{% callout type="note" %}
Finished? Go to the [Push to the Git repository](#push-to-the-git-repository) section!
{% /callout %}

### Push to the Git repository

Push the changes to Git.

```sh
# Add all the files
git add .

# Commit the changes
git commit -m "A pipeline will run my experiment on each push"

# Push the changes
git push
```

Congrats! You now have a CI/CD pipeline that will run the experiment on each commit to ensure the whole experiment can still be reproduced using the data and the commmands to run using DVC.

## Check the results

Want to see what the result at the end of this chapter should look like? Have a look at the Git repository directory here: [step-6-orchestrate-the-workflow-with-a-cicd-pipeline](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/step-6-orchestrate-the-workflow-with-a-cicd-pipeline).

## State of the MLOps process

- ✅ The codebase can be shared among the developers. The codebase can be improved collaboratively;
- ✅ The dataset can be shared among the developers and is placed in the right directory in order to run the experiment;
- ✅ The steps used to create the model are documented and can be re-executed;
- ✅ The changes done to a model can be visualized with parameters, metrics and plots to identify differences between iterations;
- ✅ The experiment can be executed on a clean machine with the help of the CI/CD pipeline;
- ❌ The model might have required artifacts that can be forgotten or omitted when saving/loading the model for future usage. There is no easy way to use the model outside of the experiment context.

## Next & Previous steps

- **Previous**: [Step 5: Track model evolutions with DVC](/the-guide/step-5-track-model-evolutions-with-dvc)
- **Next**: [Step 7: Track model evolutions in the CI/CD pipeline with CML](/the-guide/step-7-track-model-evolutions-in-the-cicd-pipeline-with-cml)
