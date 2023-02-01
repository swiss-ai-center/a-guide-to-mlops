---
title: "Chapter 6: Orchestrate the workflow with a CI/CD pipeline"
---

# {% $markdoc.frontmatter.title %}

## Introduction

At this point, you have your code, your data and your execution process that are shared through Git and DVC. 

One of great advantages of using a DVC pipeline is the facility to reproduce the experiment. You will now add CI/CD pipeline to execute the ML experiment remotely, to ensure it can always be executed and to avoid the "but it works on my machine" effect.

In this chapter, you'll cover:

1. Creating a Google Service Account to grant access to the Google Cloud project from the CI/CD pipeline
2. Storing the Google Service Account key in GitHub/GitLab CI/CD configuration
3. Creating the CI/CD pipeline configuration file
4. Pushing the CI/CD pipeline configuration file to Git
5. Visualizing the execution of the CI/CD pipeline

## Steps

{% callout type="warning" %}
This guide has been written with macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use [GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

### Create a Google Service Account to be used by the CI/CD pipeline

DVC will need to log in to Google Cloud in order to download the data inside the CI/CD pipeline.

Google Cloud allows the creation of "Service Account" so you don't have to store/share your own credentials. A Service Account can be deleted, revoking all the accesses it has.

You will now create a Google Service Account.

On the [Google Cloud console](https://console.cloud.google.com/), select **Select a project** in the upper right corner of the screen and select the project that was created in [Chapter 3: Share your ML experiment data with DVC](/the-guide/chapter-3-share-your-ml-experiment-data-with-dvc).

On the frontpage, note the project ID, it will be used later (`mlopsdemo-project` from [Chapter 3: Share your ML experiment data with DVC](/the-guide/chapter-3-share-your-ml-experiment-data-with-dvc)).

Create a Google Service Account by going to **IAM & Admin > Service Accounts**  on the left sidebar.

Select **Create Service Account**.

- **Service Account Key name**: _mlopsdemo-service-account-key_)
- Select **Create and continue**
- Select the **Basic > Viewer Role** role
- Select **Continue**
- Select **Done**

Select the newly created service account, select **Keys** and add a new key (JSON format). Save the key in your **Downloads** directory. Remember the name of the file as it will be used later. For the rest of this guide, this service key account file will be referenced as `google-service-account-key.json`.

**Note**: You must **not** add and commit this file to your working directory. It is a sensitive data that you must keep safe.

### Store the Google Service Account key and setup your repository CI/CD pipeline

You are about the setup the CI/CD pipeline to run the experiment each time there is a push to main. 

Please refer to the correct instructions based on your Git repository provider. The instructions are slightly different for GitHub and GitLab.

#### GitHub Actions

{% callout type="note" %}
Using GitLab? Go to the [GitLab CI](#gitlab-ci) step!
{% /callout %}

**Display the Google Service Account key**

Display the Google Service Account key that you have downloaded from Google Cloud.

```sh
# Display the Google Service Account key
cat ~/Downloads/google-service-account-key.json
```

**Store the Google Service Account key as a CI/CD variable**

Store the output as a CI/CD variable by going to the **Settings** section from the top header of your GitHub repository.

Select **Secrets > Actions** and select **New repository secret**.

Create a new variable named `GCP_SERVICE_ACCOUNT_KEY` with the output value of the Google Service Account key file as its value. Save the variable by selecting **Add secret**.

**Create the CI/CD pipeline configuration file**

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

Explore this file to understand the jobs and the steps.

**Push the CI/CD pipeline configuration file to Git**

Push the CI/CD pipeline configuration file to Git.

```sh
# Add the configuration file
git add .github/workflows/mlops.yml

# Commit the changes
git commit -m "A pipeline will run my experiment on each push"

# Push the changes
git push
```

{% callout type="note" %}
Finished? Go to the [Check the results](#check-the-results) step!
{% /callout %}

#### GitLab CI

{% callout type="note" %}
Using GitHub? Go to the [GitHub Actions](#github-actions) step!
{% /callout %}

Store the Google Service Account made earlier in GitLab CI variables.

```sh
# Transform the Google Service Account key to base64
base64 -i google-service-account-key.json
```

Store the output as a CI/CD Variable by going to **Settings > CI/CD** from the left sidebar of your GitLab project.

Select **Variables** and select **Add variable**.

Create a new variable named `GCP_SERVICE_ACCOUNT_KEY` with the `base64` value of the Google Service Account key file as its value.

Check the _"Mask variable"_ box, uncheck _"Protect variable"_.

Save the variable by selecting **Add variable**.

At the root level of your Git repository, create a GitLab CI configuration file `.gitlab-ci.yml`.

```yaml
stages:
  - train

# Change pip's cache directory to be inside the project directory since we can
# only cache local items.
variables:
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
```

Explore this file to understand the stages and the steps.

{% callout type="note" %}
Finished? Go to the [Check the results](#check-the-results) step!
{% /callout %}

### Check the results

Congrats! You now have a CI/CD pipeline that will run the experiment on each commit.

For GitLab, you can see the pipeline running on the **CI/CD > Pipelines** page.

For GitHub, you can see the pipeline running on the **Actions** page.

You should see a newly created pipeline. The pipeline should log into Google Cloud, pull the data from DVC and reproduce the experiment. Ensure you have pushed all data to DVC (`dvc push`) if you have cache errors.

This chapter is done, you can check the summary.

## Summary

In this chapter, you have successfully:

1. Created a Google Service Account to grant access to the Google Cloud project from the CI/CD pipeline
2. Stored the Google Service Account key in GitHub/GitLab CI/CD configuration
3. Created the CI/CD pipeline configuration file
4. Pushed the CI/CD pipeline configuration file to Git
5. Visualized the execution of the CI/CD pipeline

You did fix some of the previous issues:

- ✅ The experiment can be executed on a clean machine with the help of a CI/CD pipeline.

You have a CI/CD pipeline to ensure the whole experiment can still be reproduced using the data and the commmands to run using DVC over time.

You can now safely continue to the next chapter.

## State of the MLOps process

- ✅ The codebase can be shared and improved by multiple developers;
- ✅ The dataset can be shared among the developers and is placed in the right directory in order to run the experiment;
- ✅ The steps used to create the model are documented and can be re-executed;
- ✅ The changes done to a model can be visualized with parameters, metrics and plots to identify differences between iterations;
- ✅ The experiment can be executed on a clean machine with the help of a CI/CD pipeline;
- ❌ Model may have required artifacts that are forgotten or omitted in saved/loaded state. There is no easy way to use the model outside of the experiment context.

You will address these issues in the next chapters for improved efficiency and collaboration. Continue the guide to learn how.

## Sources

Highly inspired by the [_Using service accounts_ - dvc.org](https://dvc.org/doc/user-guide/setup-google-drive-remote#using-service-accounts), [_Creating encrypted secrets for a repository_ - docs.github.com](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) and [_Add a CI/CD variable to a project_ - docs.gitlab.com](https://docs.gitlab.com/ee/ci/variables/#add-a-cicd-variable-to-a-project) guides.

Want to see what the result at the end of this chapter should look like? Have a look at the Git repository directory here: [chapter-6-orchestrate-the-workflow-with-a-cicd-pipeline](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/chapter-6-orchestrate-the-workflow-with-a-cicd-pipeline).

## Next & Previous chapters

- **Previous**: [Chapter 5: Track model evolutions with DVC](/the-guide/chapter-5-track-model-evolutions-with-dvc)
- **Next**: [Chapter 7: Track model evolutions in the CI/CD pipeline with CML](/the-guide/chapter-7-track-model-evolutions-in-the-cicd-pipeline-with-cml)
