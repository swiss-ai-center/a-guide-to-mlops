# Concept

Introduction to MLOps.

## What is MLOps?

MLOps, short for _Machine Learning Operations_, is the set of practices that
turns a machine learning experiment into a system that can be reproduced,
deployed, monitored, and improved over time. It applies the principles of
software engineering (version control, automated testing, continuous
integration, and deployment) to machine learning, where code, data, and models
change together.

A model in MLOps is more than an artifact from a single run. It is the result of
a pipeline that versions its inputs, parameters, and environment and lets anyone
with access to the repository recreate its outputs.

## The scope of an ML system

A common mistake is to treat the model as the product. The model code and
trained weights are only a small part of a production machine learning system.
The surrounding infrastructure is far larger: data pipelines, training
orchestration, experiment tracking, serving infrastructure, monitoring, and
feedback loops.

![ML system](assets/images/ml_system.svg){ align=center }

MLOps provides the tools and discipline to manage this infrastructure. The goal
is to build a reliable system around the model rather than tune the model on its
own.

## What MLOps addresses

These challenges arise when an experiment must be shared, deployed, or
maintained:

- **Reproducibility.** The same experiment must produce the same result for a
  different person, on a different machine, or months later. Version control and
  data versioning ensure the same result every time.
- **Automation.** Manual training, evaluation, and reporting steps do not scale
  across a team. A continuous integration pipeline automates these steps and
  validates every change.
- **Deployment.** A trained model is useful only when it can serve other
  systems. Packaging it into a container and deploying it to Kubernetes makes it
  available.
- **Monitoring.** Production data changes, and model performance degrades over
  time. Monitoring detects drift and signals when a model needs attention.
- **Retraining.** New data closes the loop. Labeling it with AI assistance and
  retraining the model improves the system over time.

## Why this matters

Without MLOps, a successful experiment often remains a fragile artifact:
difficult to reproduce, hard to update, and risky to deploy. With MLOps, the
experiment becomes the starting point of a lifecycle in which results can be
tracked, compared, deployed, and improved.
