---
title: "Part 4 - Introduction"
---

# Introduction

!!! warning

    This part of the guide is a work in progress. Once completed, it will cover how
    to keep a model healthy in production by observing its behavior over time and
    reacting to changes.

Learn how to monitor and maintain the model using
[:simple-fluentbit: Fluent Bit](../tools.md) and [Evidently AI](../tools.md).

## Environment

This guide has been written with :simple-apple: macOS and :simple-linux: Linux
operating systems in mind. If you use :fontawesome-brands-windows: Windows, you
might encounter issues. Please use the
[Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/)
(WSL 2) for optimal results.

## Requirements

The following requirements are necessary to follow this part in addition to
those described in the
[first part](../part-1-local-training-and-evaluation/introduction.md#requirements):

- A [:simple-github: GitHub](https://github.com) account
- A [:simple-googlecloud: Google Cloud](https://cloud.google.com) account

??? info "Using different platforms? Read this!"

    While this guide uses GitHub and Google Cloud for examples, the core MLOps
    principles and architecture patterns apply to other platforms with some
    adjustments:

    - **Development platforms**: Works with on-premise solutions like
      [GitLab](https://about.gitlab.com/) (comprehensive built-in CI/CD system) and
      [Gitea](https://about.gitea.com/) (largely compatible with GitHub Actions
      syntax).
    - **Cloud providers**: Adaptable to other cloud platforms with appropriate
      service mappings.

!!! note

    **A credit card might be necessary to use cloud services.**

    Before proceeding with this section, please ensure that you have a valid payment
    method, as it may be required to utilize cloud services. It is important to note
    that at the conclusion of this section, you will need to
    [delete the cloud resources](../clean-up.md) that were created to avoid any
    potential charges.

    While the costs associated with this section are **expected to be free**, it is
    recommended to review the pricing details of cloud services before initiating
    this part.

## State of the MLOps process

Once the model is deployed, it needs to be observed and maintained in
production. In this part, you will address the following issues:

- [ ] Model predictions cannot be monitored in production
- [ ] Data drift and concept drift are not monitored
- [ ] No automated reports or dashboard are configured
- [ ] Drift signals do not trigger actionable alerts
- [ ] Drift alerts do not lead to a reviewed decision
