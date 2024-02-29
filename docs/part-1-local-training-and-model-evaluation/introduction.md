---
title: "Part 1 - Introduction"
---

# Introduction

Learn how to train a model locally and evaluate it using
[:simple-dvc: DVC](../tools.md).

## Environment

This guide has been written with :simple-apple: macOS and :simple-linux: Linux
operating systems in mind. If you use :simple-windows: Windows, you might
encounter issues. Please use the
[Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/)
(WSL 2) for optimal results.

## Requirements

The following requirements are necessary to follow this part:

- An IDE. We recommend to use
  [:simple-visualstudiocode: Visual Studio Code](https://code.visualstudio.com/)
  to follow this guide.
- [:simple-python: Python 3.11](https://www.python.org/downloads/)
- [:simple-python: pip](https://pip.pypa.io/)
- [:simple-git: Git](https://git-scm.com/)
- [wget](https://linux.die.net/man/1/wget)
- [unzip](https://linux.die.net/man/1/unzip)

??? danger "Using a virtual environment manager other than vanilla Python (Conda, Anaconda, etc.)? Read this!"

    While Conda, Anaconda and other Python virtual environment managers might be
    widely used tools for Python dependency management, they do come with certain
    drawbacks. Despite being designed to simplify the installation of Python and its
    packages, they can be complex to work with. This irony arises from the fact that
    they are praised for simplifying processes, yet their usage can be challenging.
    Additionally, they introduce a variety of failure modes, which can be numerous
    and intricate.

    Addressing these failures often requires significant resources and
    troubleshooting skills, leading to a diminished overall benefit for the average
    Python user. Consequently, considering these factors, some users may find that
    the effort and time required to deal with Conda-related issues outweigh the
    advantages it provides.

    In the context of this guide, we highly recommend you to follow it using the
    vanilla Python environment as it has been tested and validated with it. If you
    still want to use Conda/Anaconda/etc., please be aware that you might encounter
    issues.
