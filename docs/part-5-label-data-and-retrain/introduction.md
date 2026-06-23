---
title: "Part 5 - Introduction"
---

# Introduction

Learn how to use the model to label new data using Label Studio and retrain the
model iteratively.

## State of the MLOps process

Production feedback and new data require a way to improve the model iteratively.
In this part, you will address the following issues:

- [ ] Labeling of supplemental data is not systematic or uniform
- [ ] Labeling of supplemental data is time intensive
- [ ] Model needs to be retrained using higher-quality data

!!! note

    This part focuses on labeling data locally so you can experiment without extra
    infrastructure.

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

- A :simple-googlechrome: Chrome or a :material-firefox: Firefox based browser
  for better compatibility
