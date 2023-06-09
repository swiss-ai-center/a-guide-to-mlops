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


#### Input example 1

**Request body**

```json
{
  "data": [
    "How to create a plot in R?"
  ]
}
```

**Prediction output**

This output means that the input is related to the R programming language.

```json
[
  1
]
```

**Probabilities output**

This output means a 94% probability that the input is related to the R
programming language.

```json
[
  [
    0.06,
    0.94
  ]
]
```

#### Input example 2

**Request body**

```json
{
  "data": [
    "This should not be related as I talk about dogs"
  ]
}
```

**Prediction output**

This output means that the input is not related to the R programming language.

```json
[
  0
]
```

**Probabilities output**

This output means a 22% probability that the input is related to the R
programming language.

```json
[
  [
    0.77650959300044,
    0.22349040699956035
  ]
]
```

#### Input example 3

**Request body**

```json
{
  "data": [
    "My favorite programming language is Python!"
  ]
}
```

**Prediction output**

This output means that the input is not related to the R programming language.

```json
[
  0
]
```

**Probabilities output**

This output means a 10% probability that the input is related to the R
programming language.

```json
[
  [
    0.8910538088128949,
    0.10894619118710518
  ]
]
```

### Check the changes

Check the changes with Git to ensure all wanted files are here.

```sh title="Execute the following command(s) in a terminal"
# Add all the files
git add .

# Check the changes
git status
```

The output of the `git status` command should be similar to this.

```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   .dvcignore
	new file:   .mlem.yaml
	modified:   data/features/.gitignore
	new file:   data/features/tfidf.mlem
	new file:   data/features/vectorizer.mlem
	modified:   dvc.lock
	modified:   dvc.yaml
	new file:   models/.gitignore
	new file:   models/rf.mlem
	modified:   poetry.lock
	modified:   pyproject.toml
	modified:   src/evaluate.py
	modified:   src/featurization.py
	modified:   src/train.py
```

### Push the changes to DVC and Git

Push the changes to DVC and Git.

```sh title="Execute the following command(s) in a terminal"
# Upload the experiment data and cache to the remote bucket
dvc push

# Commit the changes
git commit -m "MLEM can save, load and serve the model"

# Push the changes
git push
```

### Check the results

Congrats! You now have a model served over a REST API!

This chapter is done, you can check the summary.

## Summary

In this chapter, you have successfully:

1. Installed MLEM
2. Initialized and configuring MLEM
3. Updated and ran the experiment to use MLEM to save and load the model
4. Served the model with FastAPI
5. Pushed the changes to DVC and Git

You did fix some of the previous issues:

- ✅ The model can be saved and loaded with all have required artifacts for
  future usage. The model can be served outside of the experiment context.

You could serve this model from anywhere. Additional services could submit
predictions to your model. The usage of FastAPI creates endpoints that are
automatically documented to interact with the model.

You can now safely continue to the next chapter of this guide concluding your
journey and the next things you could do with your model.

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
