# Philosophy

Who this guide is for, and how we chose the tools.

## Target audience

This guide is for **SMEs** and small teams with
**limited dedicated MLOps infrastructure** who want to bring ML projects from
notebooks to production without a heavy, monolithic platform.

It is especially aimed at two profiles:

- **Data scientists** who train models in notebooks, save artifacts manually,
  and deploy with ad-hoc scripts. The guide gives you practical, incremental steps
  toward reproducibility, automation, deployment, monitoring, and retraining.

- **Software engineers** moving into ML engineering who already know DevOps
  practices. The guide shows how to extend those practices to ML concerns such as
  data versioning, experiment reporting, and drift detection.

## Our principles

We believe MLOps should be:

- **Version-controlled**: track code, parameters, and deployments in Git, and
  keep data versions linked to them, so every model can be reproduced.
- **Composable**: use best-of-breed open-source tools that each solve one
  problem well.
- **Incremental**: adopt one practice at a time, not all at once.
- **Pragmatic**: prioritize reproducibility first, then automation, then
  deployment, then monitoring, then feedback loops.

That is why we avoid all-in-one MLOps platforms that require dedicated
infrastructure or databases. A lightweight, Git-native stack gives you a
pragmatic path from notebooks to production while staying in control of your
tooling.
