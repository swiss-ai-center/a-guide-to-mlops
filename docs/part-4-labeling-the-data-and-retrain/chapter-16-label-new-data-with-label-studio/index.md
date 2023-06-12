# Chapter 16: Label new data with Label Studio

??? info "You want to take over from this chapter? Collapse this section and follow the instructions below."

    _Work in progress._

    [//]: # "TODO"

!!! warning "This is a work in progress"

    This chapter is a work in progress. Please check back later for updates. Thank
    you!

## Introduction

Let's add some new data to Label Studio. For this, we will incorporate
additional images and engage humans in the loop to accurately label this
additional data.

With clear guidelines and some training over potential challenges they might
encounter during the labelling process, humans can contribute to a bigger and
higher quality dataset which will in turn improve the performance of our model.

In this chapter, you will learn how to:

1. Import new data into Label Studio

Let's get started!

## Steps

### Run the experiment

Run the experiment with the updated dataset. As we only added 10 new items to
the dataset, the model performance should not change much.

```
dvc repro
```

## Commit and push the new data

Push the changes to DVC and git.

```
# Upload the experiment data and cache to the remote bucket
dvc push

# Add all the files
git add .

# Commit the changes
git commit -m "My dataset can now be used with Label Studio"

# Push the changes
git push
```

## Summary

The dataset can now be augmented, improved, shared and fixed using Label Studio.
New version of this dataset can be used in the ML experiment and still be used
with Git, DVC, CML and GitHub/GitLab.

## State of the MLOps process

- ✅ Dataset can be improved individually or as a team to improve the model's
  performance
- ❌ Model cannot be retrained easily with improved dataset
- ❌ Model prediction cannot be used in the annotation process

## Sources
