---
title: "The tools used in this guide"
---

# {% $markdoc.frontmatter.title %}

In this guide, the following tools are selected to demonstrate the MLOps process:

- Code management: [Git](#git)
- Data management: [DVC](#dvc)
- Model reproducibility: [DVC](#dvc)
- Model tracking: [DVC](#dvc) & [CML](#cml)
- Model orchestration: [GitHub Actions](#github-actions) or [GitLab CI](#gitlab-ci)
- Model serving, distributing and deploying: [MLEM](#mlem)
- Data annotation: [Label Studio](#label-studio)

We did try to find and use the tools that cause the less friction in established workflows and teams.

## The tools

### Git

[Git](https://git-scm.com/) 

For more, check out their documentation: [_Documentation_ - git-scm.com](https://git-scm.com/doc).

### DVC

[DVC](https://dvc.org/) 

For more, check out their documentation: [_DVC Documentation_ - dvc.org](https://dvc.org/doc).

### CML

[CML](https://cml.dev/) 

For more, check out their documentation: [_CML Documentation_ - cml.dev](https://cml.dev/doc/).

### GitHub Actions

[GitHub Actions](https://github.com/features/actions) 

For more, check out their documentation: [_GitHub Actions_ - docs.github.com](https://docs.github.com/en/actions).

### GitLab CI

[GitLab CI](https://about.gitlab.com/topics/ci-cd/) 

For more, check out their documentation: [_GitLab CI/CD_ - docs.gitlab.com](https://docs.gitlab.com/ee/ci/).

### MLEM

[MLEM](https://mlem.ai/) is an _open-source tool to simplify ML model deployment_".

For more, check out their documentation: [_MLEM Documentation_ - mlem.ai](https://mlem.ai/doc).

### Label Studio

[Label Studio](https://labelstud.io/) 

For more, check out their documentation: [_Get started with Label Studio_ - labelstud.io](https://labelstud.io/guide/).

## Related tools

This is a list of related tools that address each part of the workflow. A good collection of tools can be found here: [https://mlops.toys](https://mlops.toys).

### Data management

These are alternatives to DVC.

- [LakeFS](https://lakefs.io/) - Transform your data lake into a Git-like repository
- [DagsHub](https://dagshub.com/) - Open Source Data Science Collaboration
- [DoltHub](https://www.dolthub.com/) - DoltHub is where people collaboratively build, manage, and distribute structured data
- [Delta Lake](https://delta.io/) - An open-source storage framework that enables building a Lakehouse architecture with compute engines

### Monitoring/tracking

These are alternatives to CML.

- [GuildAi](https://guild.ai/) - An open source experiment tracking toolkit. Use it to build better machine learning models faster
- [Aim](https://aimstack.io/) - An open-source, self-hosted ML experiment tracking tool
- [Evidently AI](https://evidentlyai.com/) - A first-of-its-kind monitoring tool that makes debugging machine learning models simple and interactive

### Data annotation

At the moment, Label Studio is the only solution that allows to annotate many kinds of data. Other competitors only allow a certain kind of data. Have a look at the [`awesome-data-labeling`](https://github.com/heartexlabs/awesome-data-labeling) Git repository for specific alternatives.

### Model management/deployment

These are alternatives to MLEM.

- [DVC](https://dvc.org) - DVC is built to make ML models shareable and reproducible
- [Kubeflow](https://www.kubeflow.org/) - The Kubeflow project is dedicated to making deployments of machine learning (ML) workflows on Kubernetes simple, portable and scalable
- [BentoML](https://www.bentoml.com/) - An open platform that simplifies ML model deployment and enables you to serve your models at production scale in minutes

### End-to-end

These tools can be used to manage the entire lifecycle of the ML experiment. These tools were considered at the beginning of this document redaction. But as most of the tools are often opinionated and may lack the flexibility needed for the scope of this project, they were omitted.

- [MLFlow](https://mlflow.org/) - An open source platform for the machine learning lifecycle
- [MLRun](https://www.mlrun.org/) - An open source framework to orchestrate MLOps from the research stage to production-ready AI applications

## Next

- [The guide - Introduction](/the-guide/introduction)
