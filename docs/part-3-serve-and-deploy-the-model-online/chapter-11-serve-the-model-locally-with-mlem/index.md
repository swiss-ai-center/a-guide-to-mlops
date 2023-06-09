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

## Summary

In this chapter, you have successfully:

1. Served the model with FastAPI
2. Pushed the changes to DVC and Git

You did fix some of the previous issues:

- ✅ The model can be saved and loaded with all have required artifacts for
future usage. The model can be served outside of the experiment context.

You could serve this model from anywhere. Additional services could submit
predictions to your model. The usage of FastAPI creates endpoints that are
automatically documented to interact with the model.

You can now safely continue to the next chapter of this guide concluding your
journey and the next things you could do with your model.

## State of the MLOps process

!!! bug

    `[TBD]`
