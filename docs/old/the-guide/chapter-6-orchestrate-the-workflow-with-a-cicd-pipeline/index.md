# Chapter 6: Orchestrate the workflow with a CI/CD pipeline

## Introduction

[moved]

## Steps

### Create a Google Service Account key to be used by the CI/CD pipeline

[moved]

### Store the Google Service Account key and setup the CI/CD pipeline

[moved]

### Display the Google Service Account key

[moved]

### Store the Google Service Account key as a CI/CD variable

[moved]

### Create the CI/CD pipeline configuration file

[moved]

### Push the CI/CD pipeline configuration file to Git

[moved]

### Check the results

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
  pipeline
- ❌ Model may have required artifacts that are forgotten or omitted in
  saved/loaded state and there is no easy way to use the model outside of the
  experiment context

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by the [_Creating and managing service accounts_ - cloud.google.com](https://cloud.google.com/iam/docs/creating-managing-service-accounts), [_Create and manage service account keys_ - cloud.google.com](https://cloud.google.com/iam/docs/creating-managing-service-account-keys), [_IAM basic and predefined roles reference_ - cloud.google.com](https://cloud.google.com/iam/docs/understanding-roles), [_Using service accounts_ -
dvc.org](https://dvc.org/doc/user-guide/setup-google-drive-remote#using-service-accounts),
[_Creating encrypted secrets for a repository_ -
docs.github.com](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)
and [_Add a CI/CD variable to a project_ -
docs.gitlab.com](https://docs.gitlab.com/ee/ci/variables/#add-a-cicd-variable-to-a-project)
guides.

Want to see what the result at the end of this chapter should look like on your GitHub/GitLab Git repository? Have a
look at the Git repository directory here:
[chapter-6-orchestrate-the-workflow-with-a-cicd-pipeline](https://github.com/csia-pme/a-guide-to-mlops/tree/main/docs/the-guide/chapter-6-orchestrate-the-workflow-with-a-cicd-pipeline).
