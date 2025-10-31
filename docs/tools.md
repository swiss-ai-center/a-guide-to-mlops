# Tools

Introduction to the tools used in this guide.

## What are the tools used in this guide?

In this guide, you will use the following tools to demonstrate the MLOps
process:

- Code management: [:simple-git: Git](https://git-scm.com/)
- Package management: [:simple-python: pip](https://pip.pypa.io/)
- Data management: [:simple-dvc: DVC](https://dvc.org/)
- Model reproducibility: [:simple-dvc: DVC](https://dvc.org/)
- Model tracking: [:simple-dvc: DVC](https://dvc.org/) & [CML](https://cml.dev/)
- Model orchestration:
  [:simple-github: GitHub Actions](https://github.com/features/actions)
- A [:simple-googlecloud: Google Cloud](https://cloud.google.com) account
- Model serving and distributing:
  [:simple-bentoml: BentoML](https://bentoml.com/) and
  [:simple-docker: Docker](https://docker.com/)
- Model deploying: [:simple-kubernetes: Kubernetes](https://kubernetes.io/)
- Data annotation: [Label Studio](https://labelstud.io/)

You will go into details about each tool in the following parts of this guide.

<!-- TODO: Add an illustration to display the different tools and their
purposes? -->

## Related tools

While this guide concentrates solely on the setup and utilization of the
mentioned tools, it is worth noting that there are alternative tools available
for each stage of the workflow.

Here is a list of related tools that can be explored as alternatives.
Additionally, you can find another valuable compilation of tools at
[https://mlops.toys](https://mlops.toys).

### Data management

These are alternatives to DVC.

- [LakeFS](https://lakefs.io/) - Transform your data lake into a Git-like
  repository
- [DagsHub](https://dagshub.com/) - Open Source Data Science Collaboration
- [DoltHub](https://www.dolthub.com/) - DoltHub is where people collaboratively
  build, manage, and distribute structured data
- [Delta Lake](https://delta.io/) - An open-source storage framework that
  enables building a Lakehouse architecture with compute engines

### Monitoring/tracking

These are alternatives to CML.

- [GuildAi](https://guild.ai/) - An open source experiment tracking toolkit. Use
  it to build better machine learning models faster
- [Aim](https://aimstack.io/) - An open-source, self-hosted ML experiment
  tracking tool
- [Evidently AI](https://evidentlyai.com/) - A first-of-its-kind monitoring tool
  that makes debugging machine learning models simple and interactive

### Data annotation

At the moment, Label Studio is the only solution that allows to annotate many
kinds of data. Other competitors only allow a certain kind of data. Have a look
at the
[`awesome-data-labeling`](https://github.com/heartexlabs/awesome-data-labeling)
Git repository for specific alternatives.

### Model orchestration

These are alternatives to GitHub Actions.

- [GitLab CI](https://about.gitlab.com/topics/ci-cd/) - A complete DevOps platform with built-in CI/CD and container registry
- [Gitea](https://about.gitea.com/) - A painless self-hosted Git service with
  built-in CI/CD using GitHub Actions-compatible syntax
- [Forgejo](https://forgejo.org/) - A self-hosted Git service and soft fork of
  Gitea with GitHub Actions-compatible workflows

### Model management/deployment

These are alternatives to BentoML and Docker.

- [Kubeflow](https://www.kubeflow.org/) - The Kubeflow project is dedicated to
  making deployments of machine learning (ML) workflows on Kubernetes simple,
  portable and scalable
- [MLEM](https://mlem.ai/) - The open-source tool to simplify your ML model
  deployments
- [Cog](https://github.com/replicate/cog) - An open-source tool that lets you
  package machine learning models in a standard, production-ready container
- [Podman](https://podman.io/) - A daemonless, open source, Linux native tool
  designed to make it easy to find, run, build, share and deploy applications
  using Open Container Initiative containers and images

### End-to-end

These tools can be used to manage the entire lifecycle of the ML experiment.
These tools were considered at the beginning of this document redaction. But as
most of the tools are often opinionated and may lack the flexibility needed for
the scope of this project, they were omitted.

- [MLFlow](https://mlflow.org/) - An open source platform for the machine
  learning lifecycle
- [MLRun](https://www.mlrun.org/) - An open source framework to orchestrate
  MLOps from the research stage to production-ready AI applications
