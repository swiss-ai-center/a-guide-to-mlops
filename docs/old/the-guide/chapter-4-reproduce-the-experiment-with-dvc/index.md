# Chapter 4: Reproduce the experiment with DVC

## Introduction

[moved]

## Steps

### Remove custom rules from the .gitignore file

[moved]

### Setup the DVC pipeline stages

[moved]

### Visualize the pipeline

[moved]

### Execute the pipeline

[moved]

### Check the changes

[moved]

### Push the changes to DVC and Git

[moved]

## Summary

[moved]

## State of the MLOps process

- ✅ The codebase can be shared and improved by multiple developers
- ✅ The dataset can be shared among the developers and is placed in the right
  directory in order to run the experiment
- ✅ The steps used to create the model are documented and can be re-executed
- ❌ Changes to model are not easily visualized
- ❌ Experiment may not be reproducible on other machines
- ❌ Model may have required artifacts that are forgotten or omitted in
  saved/loaded state and there is no easy way to use the model outside of the
  experiment context

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by the [_Get Started: Data Pipelines_ -
dvc.org](https://dvc.org/doc/start/data-management/data-pipelines) guide.

Want to see what the result at the end of this chapter should look like on your GitHub/GitLab Git repository? Have a
look at the Git repository directory here:
[chapter-4-reproduce-the-experiment-with-dvc](https://github.com/csia-pme/a-guide-to-mlops/tree/main/docs/the-guide/chapter-4-reproduce-the-experiment-with-dvc).
