---
title: "The tools used in this guide"
---

# {% $markdoc.frontmatter.title %}

In this example, the following tools are selected to demonstrate the ML Ops process:

- Code management: Git
- Data management: DVC
- Model management: MLEM
- Data annotation: Label Studio
- Lifecycle: DVC + GitHub Actions/GitLab CI + CML + MLEM

## Git

## DVC

## CML

## MLEM

## Label Studio

## GitHub Actions / GitLab CI

## Related tools

This is a list of related tools that address each part of the workflow. A good collection of tools can be found here: [https://mlops.toys](https://mlops.toys).

### Data management

These are alternatives to DVC.

- [LakeFS](https://lakefs.io/) - Transform your data lake into a Git-like repository
- [DagsHub](https://dagshub.com/) - Open Source Data Science Collaboration
- [DoltHub](https://www.dolthub.com/) - DoltHub is where people collaboratively build, manage, and distribute structured data
- [Delta Lake](https://delta.io/) - An open-source storage framework that enables building a Lakehouse architecture with compute engines

### Monitoring/tracking

These are alternatives to GitLab + CML.

- [GuildAi](https://guild.ai/) - An open source experiment tracking toolkit. Use it to build better machine learning models faster
- [Aim](https://aimstack.io/) - An open-source, self-hosted ML experiment tracking tool

### Data annotation

At the moment, Label Studio is the only solution that allows to annotate many kinds of data. Other competitors only allow a certain kind of data. Have a look at the [`awesome-data-labeling`](https://github.com/heartexlabs/awesome-data-labeling) Git repository for specific alternatives.

### Model management/deployment

These are alternatives to MLEM.

- [DVC](https://dvc.org) - DVC is built to make ML models shareable and reproducible
- [Kubeflow](https://www.kubeflow.org/) - The Kubeflow project is dedicated to making deployments of machine learning (ML) workflows on Kubernetes simple, portable and scalable
- [BentoML](https://www.bentoml.com/) - An open platform that simplifies ML model deployment and enables you to serve your models at production scale in minutes
- [Evidently AI](https://evidentlyai.com/) - A first-of-its-kind monitoring tool that makes debugging machine learning models simple and interactive

### End-to-end

These tools can be used to manage the entire lifecycle of the ML experiment. These tools were considered at the beginning of this document redaction. But as most of the tools are often opinionated and may lack the flexibility needed for the scope of this project, they were omitted.

- [MLFlow](https://mlflow.org/) - An open source platform for the machine learning lifecycle
- [MLRun](https://www.mlrun.org/) - An open source framework to orchestrate MLOps from the research stage to production-ready AI applications
