# Chapter 8: Reproduce the ML experiment in a CI/CD pipeline

## Introduction

At this point, your code, your data and your execution process should be
shared with Git and DVC.

Now, it's time to enhance your workflow further by incorporating a CI/CD
(Continuous Integration/Continuous Deployment) pipeline. This addition will
enable you to execute your ML experiments remotely and reproduce it, ensuring
that any changes made to the project won't inadvertently break. This helps
eliminate the notorious "but it works on my machine" effect, where code behave
differently across different environments.

In this chapter, you will learn how to:

1. Create a Google Service Account to grant access to the Google Cloud project
from the CI/CD pipeline
2. Store the Google Service Account key in GitHub/GitLab CI/CD configuration
3. Create the CI/CD pipeline configuration file
4. Push the CI/CD pipeline configuration file to Git
5. Visualize the execution of the CI/CD pipeline

```mermaid
flowchart LR
	dot_dvc[(.dvc)] -->|dvc push| s3_storage[(S3 Storage)]
	s3_storage -->|dvc pull| dot_dvc
	dot_git[(.git)] -->|git push| gitGraph[Git Remote]
	gitGraph -->|git pull| dot_git
    localGraph <-....-> dot_git
	data[data.csv] <-.-> dot_dvc
    subgraph cloudGraph[CLOUD]
        s3_storage
        subgraph gitGraph[Git Remote]
            repository[Repository] --> action[Action]
            action -->|dvc pull| action_data[data.csv]
            action_data -->|dvc repro| 732730[metrics &amp; plots]
        end
	end
	subgraph cacheGraph[CACHE]
		dot_dvc
		dot_git
	end
	subgraph localGraph[LOCAL]
		prepare[prepare.py] <-.-> dot_dvc
		train[train.py] <-.-> dot_dvc
		evaluate[evaluate.py] <-.-> dot_dvc
		data --> prepare
		subgraph dvcGraph[dvc.yaml]
			prepare --> train
			train --> evaluate
		end
        params[params.yaml] -.- prepare
        params -.- train
        params <-.-> dot_dvc
	end
    style cacheGraph opacity:0.4,color:#7f7f7f80
    style localGraph opacity:0.4,color:#7f7f7f80
    style dot_git opacity:0.4,color:#7f7f7f80
    style dot_dvc opacity:0.4,color:#7f7f7f80
    style data opacity:0.4,color:#7f7f7f80
    style prepare opacity:0.4,color:#7f7f7f80
    style params opacity:0.4,color:#7f7f7f80
    style train opacity:0.4,color:#7f7f7f80
    style evaluate opacity:0.4,color:#7f7f7f80
    style dvcGraph opacity:0.4,color:#7f7f7f80
    style s3_storage opacity:0.4,color:#7f7f7f80
    style repository opacity:0.4,color:#7f7f7f80
    linkStyle 0 opacity:0.4,color:#7f7f7f80
    linkStyle 1 opacity:0.4,color:#7f7f7f80
    linkStyle 2 opacity:0.4,color:#7f7f7f80
    linkStyle 3 opacity:0.4,color:#7f7f7f80
    linkStyle 4 opacity:0.4,color:#7f7f7f80
    linkStyle 5 opacity:0.4,color:#7f7f7f80
    linkStyle 9 opacity:0.4,color:#7f7f7f80
    linkStyle 10 opacity:0.4,color:#7f7f7f80
    linkStyle 11 opacity:0.4,color:#7f7f7f80
    linkStyle 12 opacity:0.4,color:#7f7f7f80
    linkStyle 13 opacity:0.4,color:#7f7f7f80
    linkStyle 14 opacity:0.4,color:#7f7f7f80
    linkStyle 15 opacity:0.4,color:#7f7f7f80
    linkStyle 16 opacity:0.4,color:#7f7f7f80
    linkStyle 17 opacity:0.4,color:#7f7f7f80
```

## Steps

### Create a Google Service Account key to be used by the CI/CD pipeline

DVC will need to log in to Google Cloud to download the data inside the
CI/CD pipeline.

Google Cloud allows the creation of a "Service Account", so you don't have to
store/share your own credentials. A Service Account can be deleted, hence
revoking all the access it had.

Create the Google Service Account and its associated Google Service Account Key
to access Google Cloud without your own credentials.

Replace `<id of your gcp project>` with your own project ID.

The key will be stored in your **~/.config/gcloud** directory under the name
`dvc-google-service-account-key.json`.

!!! danger

    You must **never** add and commit this file to your working directory.
    It is a sensitive data that you must keep safe.

```sh title="Execute the following command(s) in a terminal"
# Create the Google Service Account
gcloud iam service-accounts create dvc-service-account \
--display-name="DVC Service Account"

# Set the permissions for the Google Service Account
gcloud projects add-iam-policy-binding <id of your gcp project> \
    --member="serviceAccount:dvc-service-account@<id of your gcp project>.iam.gserviceaccount.com" \
    --role="roles/viewer"

# Create the Google Service Account Key
gcloud iam service-accounts keys create ~/.config/gcloud/dvc-google-service-account-key.json \
    --iam-account=dvc-service-account@<id of your gcp project>.iam.gserviceaccount.com
```

!!! info

    The path `~/.config/gcloud` should be created when installing `gcloud`. If
    it does not exist, you can create it by running `mkdir -p ~/.config/gcloud`

### Store the Google Service Account key and setup the CI/CD pipeline

You are about the setup the CI/CD pipeline to run the experiment each time there
is a pull request or a push to the main branch.

Please refer to the correct instructions based on your Git repository provider.

### Display the Google Service Account key

=== ":simple-github: GitHub"

    Display the Google Service Account key that you have downloaded from Google
    Cloud.

    ```sh title="Execute the following command(s) in a terminal"
    # Display the Google Service Account key
    cat ~/.config/gcloud/dvc-google-service-account-key.json
    ```

=== ":simple-gitlab: GitLab"

    Encode and display the Google Service Account key that you have downloaded from
    Google Cloud as `base64`. It allows to hide the secret in GitLab CI logs as a
    security measure.

    !!! tip

        If on Linux, you can use the command `base64 -w 0 -i ~/.config/gcloud/dvc-google-service-account-key.json`.

    ```sh title="Execute the following command(s) in a terminal"
    # Encode the Google Service Account key to base64
    base64 -i ~/.config/gcloud/dvc-google-service-account-key.json
    ```

### Store the Google Service Account key as a CI/CD variable

=== ":simple-github: GitHub"

    Store the output as a CI/CD variable by going to the **Settings** section from
    the top header of your GitHub repository.

    Select **Secrets and variables > Actions** and select **New repository secret**.

    Create a new variable named `GCP_SERVICE_ACCOUNT_KEY` with the output value of
    the Google Service Account key file as its value. Save the variable by selecting
    **Add secret**.

=== ":simple-gitlab: GitLab"

    Store the output as a CI/CD Variable by going to **Settings > CI/CD** from
    the left sidebar of your GitLab project.

    Select **Variables** and select **Add variable**.

    Create a new variable named `GCP_SERVICE_ACCOUNT_KEY` with
    the Google Service Account key file encoded in `base64` as its value.

    - **Protect variable**: _Unchecked_
    - **Mask variable**: _Checked_
    - **Expand variable reference**: _Unchecked_

    Save the variable by clicking **Add variable**.

### Create the CI/CD pipeline configuration file

=== ":simple-github: GitHub"

    At the root level of your Git repository, create a GitHub Workflow
    configuration file `.github/workflows/mlops.yml`.

    Take some time to understand the train job and its steps.

    ```yaml title=".github/workflows/mlops.yml"
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
    ```

    You may notice the usage of the `poetry run` prefix before each command. As we are in the context of a GitHub Workflow, we need to prefix each command with `poetry run` to ensure that the command is executed in the virtual environment created by Poetry. Locally, you enabled the Poetry virtual environment with `poetry shell` that is not needed in the context of a GitHub Workflow.

=== ":simple-gitlab: GitLab"

    At the root level of your Git repository, create a GitLab CI configuration
    file `.gitlab-ci.yml`.

    Explore this file to understand the train stage and its steps.

    ```yaml title=".gitlab-ci.yml"
    stages:
      - train

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
    ```

    You may notice the usage of the `poetry run` prefix before each command. As we are in the context of a GitLab CI pipeline, we need to prefix each command with `poetry run` to ensure that the command is executed in the virtual environment created by Poetry. Locally, you enabled the Poetry virtual environment with `poetry shell` that is not needed in the context of a GitLab CI pipeline.

### Push the CI/CD pipeline configuration file to Git

=== ":simple-github: GitHub"

    Push the CI/CD pipeline configuration file to Git.

    ```sh title="Execute the following command(s) in a terminal"
    # Add the configuration file
    git add .github/workflows/mlops.yml

    # Commit the changes
    git commit -m "A pipeline will run my experiment on each push"

    # Push the changes
    git push
    ```

=== ":simple-gitlab: GitLab"

    Push the CI/CD pipeline configuration file to Git.

    ```sh title="Execute the following command(s) in a terminal"
    # Add the configuration file
    git add .gitlab-ci.yml

    # Commit the changes
    git commit -m "A pipeline will run my experiment on each push"

    # Push the changes
    git push
    ```

### Check the results

On GitHub, you can see the pipeline running on the **Actions** page.

On GitLab, you can see the pipeline running on the **CI/CD > Pipelines** page.

You should see a newly created pipeline. The pipeline should log into Google
Cloud, pull the data from DVC and reproduce the experiment. If you encounter
cache errors, verify that you have pushed all data to DVC with `dvc push`.

You may have noticed that DVC was able to skip all stages as its cache is up to
date. It helps you to ensure the experiment can be run (all data and metadata
are up to date) and that the experiment can be reproduced (the results are the
same).

This chapter is done, you can check the summary.

## Summary

Congrats! You now have a CI/CD pipeline that will run the experiment on each
commit.

In this chapter, you have successfully:

1. Created a Google Service Account to grant access to the Google Cloud project
from the CI/CD pipeline
2. Stored the Google Service Account key in GitHub/GitLab CI/CD configuration
3. Created the CI/CD pipeline configuration file
4. Pushed the CI/CD pipeline configuration file to Git
5. Visualized the execution of the CI/CD pipeline

You fixed some of the previous issues:

- ✅ The experiment can be executed on a clean machine with the help of a CI/CD
pipeline

You have a CI/CD pipeline to ensure the whole experiment can still be reproduced
using the data and the commands to run using DVC over time.

You can now safely continue to the next chapter.

## State of the MLOps process

- ✅ Notebook has been transformed into scripts for production
- ✅ Codebase and dataset are versioned
- ✅ Steps used to create the model are documented and can be re-executed
- ✅ Changes done to a model can be visualized with parameters, metrics and plots to identify
differences between iterations
- ✅ Dataset can be shared among the developers and is placed in the right
directory in order to run the experiment
- ✅ Codebase can be shared and improved by multiple developers
- ✅ Experiment can be executed on a clean machine with the help of a CI/CD
pipeline
- ❌ Changes to model are not thoroughly reviewed and discussed before integration
- ❌ Model may have required artifacts that are forgotten or omitted in saved/loaded state
- ❌ Model cannot be easily used from outside of the experiment context

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources