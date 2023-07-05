# Tools

Introduction to the tools used in this guide.

## What are the tools used in this guide?

In this guide, we will use the following tools to demonstrate the MLOps process:

- Code management: [Git](https://git-scm.com/)
- Package management: [pip](https://pip.pypa.io/)
- Data management: [DVC](https://dvc.org/)
- Model reproducibility: [DVC](https://dvc.org/)
- Model tracking: [DVC](https://dvc.org/) & [CML](https://cml.dev/)
- Model orchestration: [GitHub Actions](https://github.com/features/actions) or [GitLab CI](https://about.gitlab.com/topics/ci-cd/)
- Cloud provider: [Amazon Web Services](https://aws.amazon.com), [Exoscale](https://www.exoscale.com), [Google Cloud Platform](https://cloud.google.com), [Microsoft Azure](https://azure.microsoft.com) or [Self-hosted Kubernetes](https://kubernetes.io)
- Model serving, distributing and deploying: [MLEM](https://mlem.ai/)
- Data annotation: [Label Studio](https://labelstud.io/)

You will go into details about each tool in the following parts of this guide.

[//]: # "TODO: Add an illustration to display the different tools and their purposes?"

### Git

[Git](https://git-scm.com/)

For more, check out their documentation: [_Documentation_ - git-scm.com](https://git-scm.com/doc).

### Poetry

[Poetry](https://python-poetry.org/)

For more, check out their documentation: [_Documentation_ - python-poetry.org](https://python-poetry.org/docs/).

### DVC

[DVC](https://dvc.org/)

For more, check out their documentation: [_DVC Documentation_ - dvc.org](https://dvc.org/doc).

### Google Cloud Storage

[Google Cloud Storage](https://cloud.google.com/storage)

For more, check out their documentation: [_Google Cloud Storage Documentation_ - cloud.google.com](https://cloud.google.com/storage/docs).

### CML

[CML](https://cml.dev/)

For more, check out their documentation: [_CML Documentation_ - cml.dev](https://cml.dev/doc/).

### GitHub Actions or GitLab CI

[GitHub Actions](https://github.com/features/actions) or [GitLab CI](https://about.gitlab.com/topics/ci-cd/)

For more, check out their documentation:

For more, check out their documentation: [_GitHub Actions_ - docs.github.com](https://docs.github.com/en/actions) or [_GitLab CI/CD_ - docs.gitlab.com](https://docs.gitlab.com/ee/ci/).

### MLEM

[MLEM](https://mlem.ai/)

For more, check out their documentation: [_MLEM Documentation_ - mlem.ai](https://mlem.ai/doc).

### Label Studio

[Label Studio](https://labelstud.io/)

For more, check out their documentation: [_Get started with Label Studio_ - labelstud.io](https://labelstud.io/guide/).


## Related tools

While this guide concentrates solely on the setup and utilization of the mentioned
tools, it is worth noting that there are alternative tools available for each stage
of the workflow.

Here is a list of related tools that can be explored as alternatives. Additionally,
you can find another valuable compilation of tools at [https://mlops.toys](https://mlops.toys).

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
