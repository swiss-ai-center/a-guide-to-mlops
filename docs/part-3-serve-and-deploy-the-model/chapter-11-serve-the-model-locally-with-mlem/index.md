# Chapter 11: Serve the model locally with MLEM

??? info "You want to take over from this chapter? Collapse this section and follow the instructions below."

    _Work in progress._

    [//]: # "TODO"

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
mlem serve fastapi --model model
```

MLEM will load the model, create the FastAPI app and start it. You can then
access the auto-generated model documentation on <http://localhost:8080/docs>{:target="\_blank"}.

!!! info

    Remember the `sample_data` variable discussed in the previous chapter? This will be used by MLEM
    to generate the FastAPI endpoints with the right OpenAPI/Swagger specifications.

The following endpoint has been created:

- `/predict`: Upload a `png` or `jpg` image and get a prediction from the model.

You can try out predictions by inputing some sentences to the model through the
REST API!

Here are some request bodies you can use as examples.

!!! warning

    Please be aware that this model is for demonstration purposes. Some
    inputs may be incorrectly predicted.

#### Input example

**Prediction output**

Below is a sample output of the prediction endpoint.

```json
{
  "prediction": "MakeMake",
  "probabilities": {
    "Earth": 5.705472982953097e-9,
    "Jupiter": 0.0072588552720844746,
    "MakeMake": 0.9552229046821594,
    "Mars": 0.0019777403213083744,
    "Mercury": 0.006808419246226549,
    "Moon": 0.021822085604071617,
    "Neptune": 0.000005649140803143382,
    "Pluto": 0.0005069805774837732,
    "Saturn": 1.4994084862607338e-9,
    "Uranus": 8.170881642399763e-7,
    "Venus": 0.006396543234586716
  }
}
```
### Check the results

Congrats! You now have a model served over a REST API!

This chapter is done, you can check the summary.

## Summary

In this chapter, you have successfully:

1. Served the model with FastAPI
2. Pushed the changes to DVC and Git

You did fix some of the previous issues:

- [x] Model can be easily used outside of the experiment context.

You could serve this model from anywhere. Additional services could submit
predictions to your model. The usage of FastAPI creates endpoints that are
automatically documented to interact with the model.

You can now safely continue to the next chapter.

## State of the MLOps process

- [x] Notebook has been transformed into scripts for production
- [x] Codebase and dataset are versioned
- [x] Steps used to create the model are documented and can be re-executed
- [x] Changes done to a model can be visualized with parameters, metrics and plots to identify
differences between iterations
- [x] Dataset can be shared among the developers and is placed in the right
directory in order to run the experiment
- [x] Codebase can be shared and improved by multiple developers
- [x] Experiment can be executed on a clean machine with the help of a CI/CD
pipeline
- [x] Changes to model can be thoroughly reviewed and discussed before integrating them into the codebase
- [x] Model can be saved and loaded with all required artifacts for future usage
- [x] Model can be easily used outside of the experiment context
- [ ] Model cannot be deployed on and accessed from a Kubernetes cluster
- [ ] Model cannot be trained on hardware other than the local machine

You will address these issues in the next chapters for improved efficiency and collaboration. Continue the guide to learn how.

## Sources

Highly inspired by:

* [_Serving models_ - mlem.ai](https://mlem.ai/doc/user-guide/serving)
