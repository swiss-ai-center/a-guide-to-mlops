# Tools

The tools used in this guide.

## Core tools

- Code management: [:simple-git: Git](https://git-scm.com/)
- Package management: [:simple-python: pip](https://pip.pypa.io/) or
  [:simple-uv: uv](https://docs.astral.sh/uv/) as an alternative
- Data and model versioning: [:simple-dvc: DVC](https://dvc.org/)
- ML experiment versioning and branching: [:simple-dvc: DVC experiments](https://dvc.org/doc/start/experiments)
- Live ML metrics logging: [DVClive](https://dvc.org/doc/dvclive)
- ML experiment reporting: [CML](https://cml.dev/)
- ML experiment visualization: [TensorBoard](https://github.com/tensorflow/tensorboard)
- Pipeline orchestration:
  [:simple-github: GitHub Actions](https://github.com/features/actions)
- Cloud infrastructure:
  [:simple-googlecloud: Google Cloud](https://cloud.google.com)
- Model packaging and serving: [:simple-bentoml: BentoML](https://bentoml.com/)
  and [:simple-docker: Docker](https://docker.com/)
- Model deployment: [:simple-kubernetes: Kubernetes](https://kubernetes.io/)
- Model observability and monitoring:
  [:simple-fluentbit: Fluent Bit](https://fluentbit.io/) and
  [Evidently AI](https://evidentlyai.com/)
- Data annotation: [Label Studio](https://labelstud.io/)

The following chapters explain each tool in detail.

## Related tools

This guide covers one toolset, but alternatives exist for every stage. For a
broader compilation, see [MLOps.toys](https://tools.mlops.community/).

### Data management

Alternatives to DVC.

- [LakeFS](https://lakefs.io/) - Git-like version control for data lakes
- [DagsHub](https://dagshub.com/) - Data science collaboration platform
- [DoltHub](https://www.dolthub.com/) - Collaborative versioned databases
- [Delta Lake](https://delta.io/) - Open-source storage layer for lakehouses

### Experiment tracking

Alternatives to the composable DVC experiments + DVClive + TensorBoard stack.
End-to-end platforms are listed at the end of this page.

- [Guild AI](https://github.com/guildai/guildai) - Open-source toolkit for
  running, tracking, and optimizing ML experiments
- [Aim](https://github.com/aimhubio/aim) - Open-source, self-hosted tool for
  tracking and visualizing ML experiments

### Model monitoring

These are alternatives to Evidently AI for monitoring models in production.

- [NannyML](https://www.nannyml.com/) - Detect model and data drift, including
  estimated performance degradation, without ground truth labels
- [Deepchecks](https://deepchecks.com/) - Test and validate ML models and data,
  with a library or self-hosted UI
- [Seldon Alibi Detect](https://github.com/SeldonIO/alibi-detect) - Algorithms
  for outlier, adversarial, and drift detection

### Logging and observability

Alternatives to Fluent Bit for collecting, processing, and forwarding logs and
observability data.

- [Vector](https://vector.dev/) - High-performance, end-to-end observability
  data pipeline for logs, metrics, and traces

### Data annotation

Label Studio handles many data types, but most competitors specialize in one.
See the
[`awesome-data-labeling`](https://github.com/heartexlabs/awesome-data-labeling)
repository for specific alternatives.

### Pipeline orchestration

Alternatives to GitHub Actions.

- [GitLab CI](https://about.gitlab.com/topics/ci-cd/) - DevOps platform with
  built-in CI/CD and container registry
- [Gitea](https://about.gitea.com/) - Self-hosted Git service with built-in
  CI/CD using GitHub Actions-compatible syntax
- [Forgejo](https://forgejo.org/) - Self-hosted Git service and soft fork of
  Gitea with GitHub Actions-compatible workflows

### Model packaging and serving

Alternatives to BentoML for packaging and serving models.

- [MLEM](https://mlem.ai/) - Open-source tool to simplify ML model deployments
- [Cog](https://github.com/replicate/cog) - Package machine learning models in
  standard, production-ready containers
- [Seldon Core](https://www.seldon.io/seldon-core) - Open-source platform to
  deploy ML models on Kubernetes
- [Kubeflow](https://www.kubeflow.org/) - ML workflows on Kubernetes, including
  training and serving

### Container tools

Alternatives to Docker.

- [Podman](https://podman.io/) - Daemonless, open-source tool for running,
  building, and sharing OCI containers and images

### Self-hosted infrastructure

Tools for running the MLOps stack on your own hardware instead of managed cloud
services.

- [CNCF Landscape](https://landscape.cncf.io/) - Graduated CNCF projects
  considered production-ready
- [Kubespray](https://kubespray.io/) - Deploy production-ready Kubernetes
  clusters on bare-metal or virtual machines
- [Argo](https://argoproj.github.io/) - Kubernetes-native continuous delivery
  (Argo CD) and workflow orchestration (Argo Workflows)
- [Harbor](https://goharbor.io/) - Self-hosted container registry with
  vulnerability scanning and RBAC
- [Distribution Registry](https://distribution.github.io/distribution/) -
  Lightweight local container registry, also known as Docker Registry
- [Helm](https://helm.sh/) - Package manager for Kubernetes; commonly used to
  install and manage Argo, registries, and CI runners
- [Docker Swarm](https://docs.docker.com/engine/swarm/) - Simpler, built-in
  container orchestration alternative to Kubernetes

### End-to-end platforms

Tools that cover the whole ML lifecycle in one platform. They are often
opinionated, so this guide prefers composable tools.

- [MLFlow](https://mlflow.org/) - Open-source platform for the machine learning
  lifecycle
- [MLRun](https://www.mlrun.org/) - Open-source framework to orchestrate MLOps
  from research to production
