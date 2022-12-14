---
title: "Step 6: Orchestrate the workflow with a CI/CD pipeline"
---

# {% $markdoc.frontmatter.title %}

## Summary

{% callout type="note" %}
Highly inspired by the [_Using service accounts_ - dvc.org](https://dvc.org/doc/user-guide/setup-google-drive-remote#using-service-accounts) guide.
{% /callout %}

The purpose of this step is to set up a CI/CD pipeline to execute the ML experiment remotely, to ensure it can always be executed and to avoid the "but it works on my machine." effect.

More functionalities offered by the CI/CD pipeline will be added in the next steps.

{% callout type="note" %}
Self-hosting your storage with MinIO? Check out the [Deploy MinIO](/advanced-concepts/deploy-minio) guide!
{% /callout %}

## Instructions

{% callout type="warning" %}
This guide has been written for macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use a decent terminal ([GitBash](https://gitforwindows.org/) for instance) or a Windows Subsystem for Linux (WSL) for optimal results.
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

Store the Google Service Account made earlier in GitLab CI variables.

```sh
# Display the Google Service Account key
cat google-service-account-key.json
```

Store the output as a CI/CD Variable by going to **Settings** from the top header of your GitHub repository. Select **Secrets > Actions** and select **New repository secret**. Create a new variable named `GCP_SERVICE_ACCOUNT_KEY` with the output value of the Google Service Account key file as its value.Save the variable by selecting "Add secret".

At the root level of your Git repository, create a GitHub Workflow configuration file `.github/workflows/mlops.yml`.

```yaml

```

{% callout type="note" %}
You might want to see a real example here: <url to the real GitHub Workflow file on the repository>
{% /callout %}

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
  - repro

run-ml-experiment:
  stage: repro
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

Push the changes to git.

```sh
# Add all the files
git add .

# Commit the changes
git commit -m "A pipeline will run my experiment on each push"

# Push the changes
git push
```

From now on, a pipeline will run the experiment on each commit to ensure the whole experiment can still be reproduced using the data and the commmands to run using DVC.

{% callout type="note" %}
Want to see what the result of this step should look like? Have a look at the Git repository directory here: [step-6-orchestrate-the-workflow-with-a-cicd-pipeline](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/step-6-orchestrate-the-workflow-with-a-cicd-pipeline)
{% /callout %}

## State of the MLOps process

## Next & Previous steps

- **Previous**: [Step 5: Track model evolutions with DVC](/the-guide/step-6-orchestrate-the-workflow-with-a-cicd-pipeline)
- **Next**: [Step 7: Visualize model evolutions with CML](/the-guide/step-7-visualize-model-evolutions-with-cml)
