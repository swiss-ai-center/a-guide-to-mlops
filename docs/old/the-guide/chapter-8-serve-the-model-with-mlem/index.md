# Chapter 8: Serve the model with MLEM

## Introduction

[moved]

## Steps

### Install MLEM

[moved]

### Initialize and configure MLEM.

[moved]

### Update the experiment

#### Update `src/featurization.py`

[moved]

#### Update `src/train.py`

[moved]

#### Update `src/evaluate.py`

[moved]

### Update the DVC pipeline

[moved]

### Run the experiment

[moved]

### Serve the model with FastAPI

[moved]

### Check the changes

[moved]

### Push the changes to DVC and Git

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
  pipeline and CML
- ✅ The model can be saved and loaded with all required artifacts for future
  usage and the model can be served outside of the experiment context.

## Sources

Highly inspired by the [_Get Started_ -
mlem.ai](https://mlem.ai/doc/get-started), [_Saving models_ -
mlem.ai](https://mlem.ai/doc/get-started/saving), [_Working with Data_ -
mlem.ai](https://mlem.ai/doc/user-guide/data), [_Serving models_ -
mlem.ai](https://mlem.ai/doc/user-guide/serving), [_Versioning MLEM objects with
DVC_ - mlem.ai](https://mlem.ai/doc/use-cases/dvc), [_`mlem.api.save()`_ -
mlem.ai](https://mlem.ai/doc/api-reference/save) and [_`mlem.api.load()`_ -
mlem.ai](https://mlem.ai/doc/api-reference/load) guides.

Want to see what the result at the end of this chapter should look like on your GitHub/GitLab Git repository? Have a
look at the Git repository directory here:
[chapter-8-serve-the-model-with-mlem](https://github.com/csia-pme/a-guide-to-mlops/tree/main/docs/the-guide/chapter-8-serve-the-model-with-mlem).
