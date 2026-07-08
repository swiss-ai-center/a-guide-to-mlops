# Concept

Introduction to MLOps.

## What is MLOps?

MLOps, short for _Machine Learning Operations_, is the set of practices that
turns a machine learning experiment into a system that can be reproduced,
deployed, monitored, and improved over time.

It sits at the intersection of machine learning, DevOps, and data engineering:

![MLOps Venn diagram](assets/images/mlops-venn-diagram.svg){ align=center }

MLOps draws on the practices of these three fields. It applies version control,
automated testing, continuous integration, and continuous deployment to machine
learning. A model becomes the result of a pipeline that versions code, data,
parameters, and environment so anyone can recreate its outputs. Teams can then
share experiments, deploy confidently, monitor performance, and retrain when
production data drifts.

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

MLOps turns experiments into systems that teams can reproduce, deploy, and
improve.
