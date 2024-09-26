---
title: "Part 2 - Introduction"
---

# Introduction

Learn how to collaborate online using [:simple-git: Git](../tools.md), enable
seamless integration with a CI/CD pipeline and visualize reports with
[CML](../tools.md).

## Environment

This guide has been written with :simple-apple: macOS and :simple-linux: Linux
operating systems in mind. If you use :fontawesome-brands-windows: Windows, you
might encounter issues. Please use the
[Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/)
(WSL 2) for optimal results.

## Requirements

The following requirements are necessary to follow this part in addition to
those described in the
[first part](../part-1-local-training-and-model-evaluation/introduction.md#requirements):

- A [:simple-github: GitHub](https://github.com) or a
  [:simple-gitlab: GitLab](https://gitlab.com) account
- A [:simple-googlecloud: Google Cloud](https://cloud.google.com) account

??? info "Using another cloud provider? Read this!"

    This guide has been written with Google Cloud in mind. We are open to
    contributions to add support for other cloud providers such as
    [:simple-amazonwebservices: Amazon Web Services](https://aws.amazon.com),
    [:simple-exoscale: Exoscale](https://www.exoscale.com),
    [:material-microsoft-azure: Microsoft Azure](https://azure.microsoft.com) or
    [:simple-kubernetes: Self-hosted Kubernetes](https://kubernetes.io) but we might
    not officially support them.

    If you want to contribute, please open an issue or a pull request on the
    [GitHub repository](https://github.com/swiss-ai-center/a-guide-to-mlops). Your
    help is greatly appreciated!

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
