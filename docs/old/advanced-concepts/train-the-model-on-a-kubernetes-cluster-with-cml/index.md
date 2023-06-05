# Train the model on a Kubernetes cluster with CML

!!! warning

	The feature presented in this guide is still a work in progress. The PRs are opened on GitHub and are soon to be closed. Check this issue for more information: <https://github.com/iterative/cml/issues/1365>.

## Introduction

[moved]

## Steps

### Enable the Google Kubernetes Engine API

[moved]

### Create the Kubernetes cluster

[moved]

### Install kubectl

[moved]

### Validate kubectl can access the cluster

[moved]

### Display the nodes labels

[moved]

### Labelize the nodes

[moved]

### Update the CI/CD configuration file

[moved]

### Push the CI/CD pipeline configuration file to Git

[moved]

### Check the results

[moved]

## Summary

[moved]

### Destroy the Kubernetes cluster

[moved]

## State of the MLOps process

- ✅ The training of the model can be done on a custom infrastructure with custom hardware for specific use-cases.

## Sources

Highly inspired by the [_Self-hosted (On-premise or Cloud) Runners_ - cml.dev](https://cml.dev/doc/self-hosted-runners), [_Install kubectl and configure cluster access_ - cloud.google.com](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl), [_gcloud container clusters create_ - cloud.google.com](https://cloud.google.com/sdk/gcloud/reference/container/clusters/create), the [_Install Tools_ - kubernetes.io](https://kubernetes.io/docs/tasks/tools/), [_Assigning Pods to Nodes_ - kubernetes.io](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector) and [_Assign Pods to Nodes_ - kubernetes.io](https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes/) guides.

Want to see what the result at the end of this chapter should look like? Have a
look at the Git repository directory here:
[train-the-model-on-a-kubernetes-cluster-with-cml](https://github.com/csia-pme/a-guide-to-mlops/tree/main/docs/advanced-concepts/train-the-model-on-a-kubernetes-cluster-with-cml).
