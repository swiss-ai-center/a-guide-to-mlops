# Concept

Introduction to MLOps.

## What is MLOps?

MLOps, short for _Machine Learning Operations_, is the set of practices that
turn a machine learning experiment into a system that can be reproduced,
deployed, monitored, and improved over time. It extends the principles of
software engineering — version control, automated testing, continuous
integration, and deployment — to the specific needs of machine learning, where
code, data, and models all change together.

In practice, MLOps means that a model is never just an artifact produced by a
single run. It is the result of a pipeline whose inputs, parameters, and
environment are versioned and whose outputs can be recreated by anyone with
access to the repository.

## The scope of an ML system

A common mistake is to treat the model as the product. In reality, the model
code and trained weights represent only a small part of a production machine
learning system. The surrounding infrastructure — data pipelines, training
orchestration, experiment tracking, serving infrastructure, monitoring, and
feedback loops — is significantly larger.

![ML system](assets/images/ml_system.svg){ align=center }

MLOps provides the tooling and discipline to manage this surrounding
infrastructure. The goal is not to optimize the model in isolation, but to build
a reliable system around it.

## What MLOps addresses

The following challenges appear as soon as an experiment needs to be shared,
deployed, or maintained:

- **Reproducibility.** The same experiment must produce the same result when run
  by a different person, on a different machine, or months later. This guide uses
  version control and data versioning to make that possible.
- **Automation.** Manual training, evaluation, and reporting steps do not scale
  across a team. This guide moves these steps into a continuous integration
  pipeline so that every change is validated automatically.
- **Deployment.** A trained model is useful only when it can be served and
  accessed by other systems. This guide packages the model, builds a container,
  and deploys it to Kubernetes.
- **Monitoring.** Production data changes, and model performance degrades over
  time. This guide adds monitoring to detect drift and identify when the model
  needs attention.
- **Retraining.** New data closes the loop and improves the model. This guide
  uses Label Studio to label new data, with AI assistance from the model, and
  retrains the model so the system keeps improving.

## Why this matters

Without MLOps, a successful experiment often remains a fragile artifact:
difficult to reproduce, hard to update, and risky to deploy. With MLOps, the
experiment becomes the starting point of a controlled lifecycle in which results
can be tracked, compared, deployed, and improved with confidence.

## This guide

This guide follows a common path in machine learning: it begins with a Jupyter
notebook experiment and progressively turns it into a reproducible, deployed,
and maintainable system. The following chapters walk through that lifecycle step
by step, beginning with a local notebook and ending with a deployed, monitored,
and retrainable system.
