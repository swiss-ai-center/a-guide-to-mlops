---
title: "Part 3 - Introduction"
---

# Introduction

Learn how to serve and deploy the model using MLEM and CML.

## Environment

This guide has been written with macOS and Linux operating systems in mind. If
you use Windows, you might encounter issues. Please use the
[Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/)
(WSL2) for optimal results.

For this part, you also need to have [Docker Desktop](https://www.docker.com/)
installed. Docker will be utilized for setting up and managing the container
registry.

## Requirements

The following requirements are necessary to follow this part in addition to
those described in the
[first part](../part-1-local-training-and-model-evaluation/introduction.md#requirements):

- A [:simple-github: GitHub](https://github.com) or a
  [:simple-gitlab: GitLab](https://gitlab.com) account
- A cloud provider account:
    - [:simple-amazonaws: Amazon Web Services](https://aws.amazon.com) (coming soon)
    - [:simple-exoscale: Exoscale](https://www.exoscale.com) (coming soon)
    - [:simple-googlecloud: Google Cloud Platform](https://cloud.google.com)
    - [:simple-microsoftazure: Microsoft Azure](https://azure.microsoft.com) (coming
      soon)
    - [:simple-kubernetes: Self-hosted Kubernetes](https://kubernetes.io) (coming
      soon)
- [:simple-docker: Docker](https://www.docker.com/)

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
