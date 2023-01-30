---
title: "Introduction"
---

# {% $markdoc.frontmatter.title %}

## Welcome

Welcome! We are glad that you are here. :)

This guide will help you through incremental steps from a traditional approach of managing ML projects to a modern ML Ops approach designed to improve team collaboration and reproducibility.

For the rest of the guide, an _experiment_ is a machine learning project.

We chose the term _experiment_ to address the experimental nature of the machine learning field before finding a suitable model.

## Disclaimer

This guide has been written for macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use [GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for optimal results.

This guide assumes that the steps to be performed are done in a working directory independently of it.

The tools and approach must be adapted to your specific use-case and experiments as well.

## Requirements

The following tools must be installed to follow this guide.

- [Python 3](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [wget](https://linux.die.net/man/1/wget)
- [unzip](https://linux.die.net/man/1/unzip)
- [Google Cloud CLI (`gcloud`)](https://cloud.google.com/sdk/docs/install-sdk)

We recommend to use [Visual Studio Code](https://code.visualstudio.com/) to follow this guide.

At the time of writing this guide, the following versions of the requirements are as follow (on macOS).

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

## Next step

- **Next**: [Chapter 1: Run a simple ML experiment](/the-guide/chapter-1-run-a-simple-ml-experiment)
