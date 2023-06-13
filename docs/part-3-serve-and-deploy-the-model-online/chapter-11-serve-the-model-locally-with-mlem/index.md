# Chapter 11: Serve the model locally with MLEM

## Introduction

Now that the model is using MLEM, enabling the extraction of metadata upon saving, we will serve the
model and leverage the capabilities of [FastAPI](https://fastapi.tiangolo.com/) to create local
endpoints for interacting with the model.

In this chapter, you will learn how to:

1. Serve the model with FastAPI
2. Push the changes to DVC and Git

## Steps

### Serve the model with FastAPI

FastAPI will generate a REST API that we can use to get predictions from our
model.

!!! info

    FastAPI is only one of the available backends that MLEM can use to serve the model. Check out
    their official documentation for more options.

Serve the model with FastAPI.

```sh title="Execute the following command(s) in a terminal"
# Serve the model with FastAPI
mlem serve fastapi --model models/rf
```

MLEM will load the model, create the FastAPI app and start it. You can then
access the auto-generated model documentation on <http://localhost:8080/docs>{:target="\_blank"}.

!!! info

    Remember the `sample_data` variable discussed in the previous chapter? This will be used by MLEM
    to generate the FastAPI endpoints with the right OpenAPI/Swagger specifications.

The following endpoints have been created:

- `/predict`: Get a string as the input and display the prediction of the input
as true (1) if it is related to the R programming language or as false (0) if
it is is not related to the R programming language.
- `/predict_proba`: Get a string as the input and display the probability of the
input as a array of two numbers. The first number is the probability from 0 to
1 of the input as not related to the R programming language. The second number
is the probability from 0 to 1 of the input as related to the R programming
language.

You can try out predictions by inputing some sentences to the model through the
REST API!

Here are some request bodies you can use as examples.

!!! warning

    Please be aware that this model is a toy. Some
    inputs may be incorrectly predicted.

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

1. Served the model with FastAPI
2. Pushed the changes to DVC and Git

You did fix some of the previous issues:

- ✅ Model can be easily used outside of the experiment context.

You could serve this model from anywhere. Additional services could submit
predictions to your model. The usage of FastAPI creates endpoints that are
automatically documented to interact with the model.

You can now safely continue to the next chapter of this guide concluding your
journey and the next things you could do with your model.

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
- ✅ Changes to model can be thoroughly reviewed and discussed before integrating them into the codebase
- ✅ Model can be saved and loaded with all required artifacts for future usage
- ✅ Model can be easily used outside of the experiment context.

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by:

* [_Serving models_ - mlem.ai](https://mlem.ai/doc/user-guide/serving)
