---
title: "Known issues, Limitations & Considerations"
---

# {% $markdoc.frontmatter.title %}

This section covers the reflexions to improve the current workflow.

## Data and code cannot evolve independently

**Observations**

As DVC is used on top of Git, when the data is updated, the metadata files linked with Git must be updated as well.

**Implications**

It is not possible to make the data evolves using another tool without updating the Git metadata files.

**Ideas considered**

_None at the moment_

## Does the predictions made by our ML model really help the person annotating the dataset

**Observations**

Label Studio can be configured to get predictions from a ML backend. These predictions can help the person annotating the dataset.

**Implications**

As the model helps the person annotating the dataset in order to improve this very specific model, we have concerns about the certainty of the process. It is not impossible that the expert is too influenced by the predictions of the model (by automatism of the process, by excessive confidence in it) and that this leads to a degradation of the performance of the model compared to an absence of annotation assistance.

**Ideas considered**

Make an experiment consisted of two groups of people that have to annotate a dataset to improve the performance of the model. One group has to annotate the dataset with the help of the model's predictions and the other without the help of the model's predictions. See the group that improves the model's performance the best.

## The export of the dataset from Label Studio is manual

**Observations**

When a dataset is improved through Label Studio, the dataset must be manually exported to the ML experiment workspace, manually update DVC and manually update the data metadata with Git.

**Implications**

This is directly related to the limitations stated above where the data cannot evolve without updating the related metadata files with Git.

**Ideas considered**

Extend Label Studio in order to allow a DVC + Git exportation. This implies Label Studio must have access to the Git repository and the permissions to update it. The dataset is exported, committed and pushed to DVC and Git.

## The retraining of the ML model from Label Studio is difficult

**Observations**

Label Studio allows the retraining of a ML model using their ML Backend library. A backend server awaits for `/train` requests that can be initiated from the Label Studio. This action will use the newly annotated dataset, train the model and serve this new model to get predictions.

**Implications**

The training is done in the Docker image that is hosted on the Virtual Machine. This implies that all the tools related to run the ML experiment must be available in order to train the model and share the new model and data.

**Ideas considered**

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

## CML cannot create a runner every time

**Observations**

CML uses Terraform to create a runner on Kubernetes. From time to time, the creation of this runner does not work. The pipeline attempts to create the runner and fails. An example can be found here: <https://git-ext.iict.ch/aii4.0/ml-ops-example/-/jobs/852>. Even with debugging on, I was not able to find the root cause of the problem. Re-running the pipeline solves the problem and is stable for a time before failing again.

**Implications**

The pipeline fails and must be run again. It is time consuming.

**Ideas considered**

View the logs on the Kubernetes cluster to identify the problem.

## CML cannot specify an affinity to run the pod on Kubernetes

**Documentation**

- [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
- [Command Reference: `runner`](https://cml.dev/doc/ref/runner)

**Observations**

CML cannot specifiy the affinity to run the pod on Kubernetes. It can specify the machine type and the kind of GPU, however.

**Implications**

Custom machine types cannot be created. The assigning process is quite limited and further configuration of the cluster must be done.

**Ideas considered**

Configure the Kubernetes cluster to order to consider these machine types. Extend the mechanism to be able to tweak the pods creation in order to pass specific labels or configuration.

## Missing elements in comparison to other user-friendly solutions

This section tries to highlight the missing elements the current solution misses to become as user-friendly as solutions such as [Lobe](https://www.lobe.ai/).

**Observations**

As mentioned above, Label Studio seems to be the limiting factor to be able to have a full life-cycle machine learning experiment platform as it cannot easily retrain the model with new labelized data.

Tools and projects must be manually configured in order to set up a new machine learning environment for a team.

**Implications**

Not a smooth and user-friendly experience.

**Ideas considered**

Use Terraform to configure VCS to:

- Create new organizations and projects with all the required configuration to run the pipeline

Use Ansible to configure hosts to host:

- A Kubernetes cluster
- MinIO service
- Label Studio and its dependencies
- The model with MLEM
