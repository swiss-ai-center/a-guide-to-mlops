# Chapter 18: Link the model to Label Studio and get predictions

??? info "You want to take over from this chapter? Collapse this section and follow the instructions below."

    _Work in progress._

    [//]: # "TODO"

!!! warning "This is a work in progress"

    This chapter is a work in progress. Please check back later for updates. Thank
    you!

## Introduction

Label Studio can now annotate new data, and the model can be further retrained.
To help the annotation process, you can integrate your model development
pipeline with your data labeling workflow by adding a machine learning backend
to Label Studio. This allows you to get predictions from our model while
annotating and to see where the model is right or wrong regarding our dataset.

In this chapter, you will learn how to:

1. Set up your machine learning backend for ML-assisted labeling

Let's get started!

Beside interactive preannotations, other possibilities include the following:

* **Pre-labeling** by letting the model predicts labels and then have annotators
  perform further manual refinements.
* **Auto-labeling** by letting models create automatic annotations.
* **Online Learning** by simultaneously updating your model while new
  annotations are created, letting you retrain your model on-the-fly.
* **Active Learning** by selecting example tasks that the model is uncertain how
  to label for your annotators to label manually.

## Steps

### Get predictions from new data

Open the Label Studio project and select Settings. Select Machine Learning.
Enable Retrieve predictions when loading a task automatically and Show
predictions to annotators in the Label Stream and Quick View. Select Add Model.
Give a title to the model (CustomTextClassifier) and the URL to the Label Studio
ML Backend (http://label-studio-ml-backend:9090). Enable the Use for interactive
preannotations and select Validate and save. From now on, while annotating new
StackOverflow posts, the ML backend will be used in order to get predictions
about the current post. This can help the people annotating the dataset and see
when posts are incorrectly annotated.

### Link the Label Studio ML Backend to Label Studio

Open the Label Studio project and select Settings. Select Machine Learning.
Enable Retrieve predictions when loading a task automatically and Show
predictions to annotators in the Label Stream and Quick View. Select Add Model.
Give a title to the model (CustomTextClassifier) and the URL to the Label Studio
ML Backend (http://label-studio-ml-backend:9090). Enable the Use for interactive
preannotations and select Validate and save. From now on, while annotating new
StackOverflow posts, the ML backend will be used in order to get predictions
about the current post. This can help the people annotating the dataset and see
when posts are incorrectly annotated.

## Summary

## State of the MLOps process

- ✅ Dataset can be improved individually or as a team to improve the model's
  performance
- ✅ Model can be linked to get interactive prediction in the annotation process
- ✅ Model can be retrained with improved dataset

## Sources

* [Add a ML backend to Label Studio](https://docs.heartex.com/guide/ml.html#Add-an-ML-backend-to-Label-Studio)
