---
title: "Step 2: Share your ML experiment code with Git"
---

# {% $markdoc.frontmatter.title %}

## Summary

The purpose of this step is to share the code of the simple ML experiment with the rest of the team using Git.

## Instructions

{% callout type="warning" %}
This guide has been written for macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use a decent terminal ([GitBash](https://gitforwindows.org/) for instance) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

Create a new repository on your favorite Git service. Clone the repository and switch to your newly cloned repository.

{% callout type="note" %}
Using GitHub? Follow the related documentation [_Creating a new repository_ - docs.github.com](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) to create a new GitHub repository for this step.
{% /callout %}

{% callout type="note" %}
Using GitLab? Follow the related documentation [_Create a project_ - docs.gitlab.com](https://docs.gitlab.com/ee/user/project/working_with_projects.html#create-a-project) to create a new GitLab project for this step.
{% /callout %}

Create a `.gitignore` file to ignore the experiment results and some files related to Python.

```sh
## Custom experiment

# Data used to train the models
data

# The models
*.pkl

# The models evaluations
evaluation

## Python

# Environments
.venv

# Byte-compiled / optimized / DLL files
__pycache__/
```

Push the changes to Git.

```sh
# Add all the files
git add .

# Commit the changes
git commit -m "My first ML experiment shared on GitLab"

# Push the changes
git push
```

Congrats! You now have a codebase that can be used and shared among the team.

When used by another member of the team, they can easily clone the experiment from Git.

```sh
# Clone the Git repository
git clone <the git repository url>
```

## Check the results

Want to see what the result of this step should look like? Have a look at the Git repository directory here: [step-2-share-your-ml-experiment-code-with-git](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/step-2-share-your-ml-experiment-code-with-git).

## State of the MLOps process

- The codebase can be shared among the developers. The codebase can be improved collaboratively;
- The dataset still needs to be downloaded and placed in the right directory in order to run the experiment;
- The steps used to create the model can be forgotten;
- The changes done to a model cannot be visualized and improvements and/or deteriorations are hard to identify;
- There is no guarantee that the experiment can be executed on another machine;
- The model might have required artifacts that can be forgotten or omitted when saving/loading the model for future usage;
- There is no easy way to serve and distribute the model outside of the experiment.

## Next & Previous steps

- **Previous**: [Step 1: Run a simple ML experiment](/the-guide/step-1-run-a-simple-ml-experiment)
- **Next**: [Step 3: Share your ML experiment data with DVC](/the-guide/step-3-share-your-ml-experiment-data-with-dvc)
