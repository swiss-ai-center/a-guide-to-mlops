---
title: "CML cannot specify an affinity to run the pod on Kubernetes"
---

# {% $markdoc.frontmatter.title %}

## Documentation

- [Assigning Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
- [Command Reference: `runner`](https://cml.dev/doc/ref/runner)

## Observations

CML cannot specifiy the affinity to run the pod on Kubernetes. It can specify the machine type and the kind of GPU, however.

## Implications

Custom machine types cannot be created. The assigning process is quite limited and further configuration of the cluster must be done.

## Ideas considered

Configure the Kubernetes cluster to order to consider these machine types. Extend the mechanism to be able to tweak the pods creation in order to pass specific labels or configuration.
