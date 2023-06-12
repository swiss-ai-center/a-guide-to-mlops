# Chapter 15: Import existing data to Label Studio

??? info "You want to take over from this chapter? Collapse this section and follow the instructions below."

    _Work in progress._

    [//]: # "TODO"

!!! warning "This is a work in progress"

    This chapter is a work in progress. Please check back later for updates. Thank
    you!

## Introduction

We now have a working installation of LabelStudio. Let's see how to import
existing data.

If you have predictions generated for your dataset from a model, either as
pre-annotated tasks or pre-labeled tasks, you can import the predictions with
your dataset into Label Studio for review and correction. Label Studio
automatically displays the pre-annotations that you import on the Labeling page
for each task.

The data to import can be stored in a cloud storage bucket, at
internet-accessible URLs, or locally. For our experiment, we will import the new
data locally.

In this chapter, you will learn how to:

1. Import existing, pre-annotated data into Label Studio

Let's get started!

## Steps

Label Studio can import labelized data using the following JSON format:
[Raw JSON structure](https://docs.heartex.com/guide/task_format.html).

```
[
    {
        "id": "The ID of the item (optional)",
        "annotations": [
        {
            "result": [
            {
                "type": "choices",
                "value": {
                    "choices": [
                    "Earth"
                    ]
                },
                "to_name": "image",
                "from_name": "choice"
            }
            ],
        }
        ],
        "file_upload": "05ed70cf-Earth_1.jpg",
        "data": {
            "image": "\\/data\\/upload\\/8\\/05ed70cf-Earth_1.jpg"
        }
    },
    {
        ...
    }
]
```

The experiment can be updated to use this Studio JSON format so data can be
imported/exported back and forth. Since our dataset images are simply classified
by being present in the a folder named with the category, we can prepare the
corresponding annotated task files wit ha simple python script.

ls -la

### Create the src/convert.py file
The original pipeline takes the dataset as an XML file. Label Studio can import
labelized data using the following JSON format. The experiment must be updated
to use the Basic Label Studio JSON format so data can be imported/exported back
and forth.

Convert the XML dataset to the Basic Label Studio JSON format and store the new
dataset in DVC. As this will be done once, there is no need to store the command
in a DVC stage.

Update the src/prepare.py file to use the new JSON dataset.

Import the new annotated dataset to Label Studio by selecting the Label Studio
project and select the Import button. Import the data.json file. The 10K
StackOverflow posts should be imported and annotated.

We now have a dataset that uses the Basic Label Studio JSON format. The pipeline
can use the new dataset and it can be imported/exported back and forth to Label
Studio for further improvements by other people.

### Download additional data

```
# Download the archive containing the extra data
wget https://github.com/csia-pme/a-guide-to-mlops/archive/refs/heads/extra-data.zip -O extra-data.zip
```

This archive must be decompressed and its contents be moved in the data
directory in the working directory of the experiment.

### Import data

Import new data, non annotated data with the **Import** button. Select the
`new_data.csv` file. Select **Treat CSV/TSV** as **List of tasks**.

In **Leballing Setup**

labelling config for Label Studio, see `config.xml`:

```

```

```
label-studio my_new_project start --label-config config.xml
```

## Ideas to consider

As the model helps the person annotating the dataset in order to improve this
very specific model, we have concerns about the certainty of the process. It is
not impossible that the expert is too influenced by the predictions of the model
(by automatism of the process, by excessive confidence in it) and that this
leads to a degradation of the performance of the model compared to an absence of
annotation assistance.

TBD: tarnsform this in good practices:

Make an experiment consisting of two groups of people that have to annotate a
dataset to improve the performance of the model. One group has to annotate the
dataset with the help of the model's predictions and the other without the help
of the model's predictions. See the group that improves the model's performance
the best.

## Export the dataset from Label Studio

The export of the dataset from Label Studio is manual

Observations When a dataset is improved through Label Studio, the dataset must
be manually exported to the ML experiment workspace, manually update DVC and
manually update the data metadata with git.

Implications This is directly related to the limitations stated above where the
data cannot evolve without updating the related metadata files with git.

Ideas considered Extend Label Studio in order to allow a DVC + git exportation.
This implies Label Studio must have access to the git repository and the
permissions to update it. The dataset is exported, committed and pushed to DVC
and git.

## Retrain the ML model from Label Studio

retraining of the ML model from Label Studio is difficult

Observations Label Studio allows the retraining of a ML model using their ML
Backend library. A backend server awaits for /train requests that can be
initiated from the Label Studio. This action will use the newly annotated
dataset, train the model and serve this new model to get predictions.

Implications The training is done in the Docker image that is hosted on the
Virtual Machine. This implies that all the tools related to run the ML
experiment must be available in order to train the model and share the new model
and data.

Ideas considered Create a Docker image with all the required tools to train and
serve the new model with an integration of DVC and git for the rest of the team.
Add the new data to DVC and git and trigger the training of the model on GitLab
to run a pipeline to generate and deploy the new model. or Three services could
solve this issue:

A Label Studio ML Backend service A MLEM service A proxy service to translate
Label Studio ML Backend <-> MLEM requests

The first service would embedded the Label Studio ML Backend. The second service
would embedded MLEM to get predictions. The third service would translate the
requests from Label Studio ML Backend to get predictions and retrain the model
on GitLab. These three services could be embedded together but are separated to
keep the single responsibility concerns applicable: a simple Label Studio ML
Backend calls the proxy that is in charge to trigger GitLab to retrain a model
or get prediction from the third service and the MLEM service that can be
redeployed on-the-fly with new models.

## Summary

How to improve our datasets individually or as a team (what if I would like to
annotate the dataset in order to improve the model's performance?). On going.
Link the model to get interactive predictions in our annotation process (for
complexe datasets, can the model help me to annotate the datasets and see where
the current model has flows?). Retrain the model with our improvements (I now
have improved my dataset and code, can I easily retrain the model to a better
version?).

In this chapter, you have successfully:

1. Installed MLEM
2. Initialized and configuring MLEM
3. Updated and ran the experiment to use MLEM to save and load the model

You did fix some of the previous issues:

- ✅ Model can be saved and loaded with all required artifacts for future usage

You can now safely continue to the next chapter.

## State of the MLOps process

- ❌ Dataset cannot be improved easily by labeling to improve the model's
  performance
- ❌ Model cannot be retrained easily with improved dataset
- ❌ Model prediction cannot be used in the annotation process

## Sources

* [Label Studio Task Format - labelstud.io](https://docs.heartex.com/guide/task_format.html)
* [Import pre-annotated data into Label Studio - labelstud.io](https://labelstud.io/guide/predictions.html)

* [Labeling configuration - labelstud.io](https://labelstud.io/guide/setup.html)
* [Integrate Label Studio into your machine learning pipeline - labelstud.io](https://labelstud.io/guide/ml.html)
