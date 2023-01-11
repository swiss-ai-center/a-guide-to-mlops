---
title: "Label Studio: The retraining of the ML model is difficult"
---

# {% $markdoc.frontmatter.title %}

## Observations

Label Studio allows the retraining of a ML model using their ML Backend library. A backend server awaits for `/train` requests that can be initiated from the Label Studio. This action will use the newly annotated dataset, train the model and serve this new model to get predictions.

## Implications

The training is done in the Docker image that is hosted on the Virtual Machine. This implies that all the tools related to run the ML experiment must be available in order to train the model and share the new model and data.

## Ideas considered

Create a Docker image with all the required tools to train and serve the new model with an integration of DVC and Git for the rest of the team.

Add the new data to DVC and Git and trigger the training of the model on GitLab to run a pipeline to generate and deploy the new model.

or

Three services could solve this issue:

- A Label Studio ML Backend service
- A MLEM service
- A proxy service to translate Label Studio ML Backend <-> MLEM requests

The first service would embedded the Label Studio ML Backend.

The second service would embedded MLEM to get predictions.

The third service would translate the requests from Label Studio ML Backend to get predictions and retrain the model on GitLab.

These three services could be embedded together but are separated to keep the single responsibility concerns applicable: a simple Label Studio ML Backend calls the proxy that is in charge to trigger GitLab to retrain a model or get prediction from the third service and the MLEM service that can be redeployed on-the-fly with new models.
