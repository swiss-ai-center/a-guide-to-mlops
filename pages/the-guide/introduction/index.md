---
title: "Introduction"
---

# {% $markdoc.frontmatter.title %}

## Welcome

👋 Welcome! We are glad that you are here. 

This guide will help you take your ML projects from experiment to production
with ease. In this half-day MLOps workshop, gain hands-on experience with Git
for code versioning, DVC for data versioning, CML for performance tracking, and
MLEM for deployment. We hope that this guide will help you streamline your
workflows, ensure reproducibility, and move your models from the lab to the
real-world with confidence.

## Environment

This guide has been written with macOS and Linux operating systems in mind. If
you use Windows, you might encounter issues. Please use
[GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for
optimal results.

## Requirements

The following requirements are necessary to follow this guide.

- A [GitHub](https://github.com/) or a [GitLab](https://gitlab.com/) account
- A [Google Cloud](https://console.cloud.google.com/) account
    - Google Cloud might need a credit card
- An IDE
    - We recommend to use [Visual Studio Code](https://code.visualstudio.com/)
      to follow this guide.
- [Python 3](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [wget](https://linux.die.net/man/1/wget)
- [unzip](https://linux.die.net/man/1/unzip)
- [Google Cloud CLI (`gcloud`)](https://cloud.google.com/sdk/docs/install-sdk)

At the time of writing, the following versions of the requirements were used (on
macOS).

```sh
# Python 3
> python3 --version
Python 3.10.9

# Git
> git --version
git version 2.37.1 (Apple Git-137.1)

# wget
> wget --version
GNU Wget 1.21.3 built on darwin22.1.0.

# unzip
> unzip -v       
UnZip 6.00 of 20 April 2009

# Google Cloud CLI
> gcloud --version
Google Cloud SDK 412.0.0

# Visual Studio Code
> code --version
1.74.3
97dec172d3256f8ca4bfb2143f3f76b503ca0534
x64
```

## Next chapter

- **Next**: [Chapter 1: Run a simple ML
  experiment](/the-guide/chapter-1-run-a-simple-ml-experiment)
