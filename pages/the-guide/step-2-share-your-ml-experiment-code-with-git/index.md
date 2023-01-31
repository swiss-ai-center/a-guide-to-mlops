---
title: "Chapter 2: Share your ML experiment code with Git"
---

# {% $markdoc.frontmatter.title %}

## Introduction

Great! You have a grasp on how the experiment runs. The USB stick from your collegue was kind of an old-school way to transfer files right?

Our first improvement will only concern the experiment codebase. It will ensure it can be shared with the team 

To do so we will create a new Git repository, and push our existing code to it. An important part of this step is to configure the `.gitignore` correctly to avoid pushing our data to the repository.

At the end of this step we will have a versioned codebase we can share with our team !

## Instructions

{% callout type="warning" %}
This guide has been written with macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use [GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

### Create a new Git repository

Create a new repository on your favorite Git service. Clone the repository and switch to your newly cloned repository.

{% callout type="note" %}
Using GitHub? Follow the related documentation [_Creating a new repository_ - docs.github.com](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) to create a new GitHub repository for this step.
{% /callout %}

{% callout type="note" %}
Using GitLab? Follow the related documentation [_Create a project_ - docs.gitlab.com](https://docs.gitlab.com/ee/user/project/working_with_projects.html#create-a-project) to create a new GitLab project for this step.
{% /callout %}

#### Create a `.gitignore` file

Create a `.gitignore` file to ignore the experiment results, the data, the models and the Python environment.

```sh
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
# Initialize the repository
git init

# Rename the master branch
git branch -M main

# Add all the files
git add .

# Commit the changes
git commit -m "My first ML experiment shared on GitLab"

# Add your remote repository
git remote add origin <git@example.com:username/repository.git>

# Push the changes
git push --set-upstream origin main
```

Congrats! You now have a codebase that can be used and shared among the team.

When used by another member of the team, they can easily clone the experiment from Git.

```sh
# Clone the Git repository
git clone <the git repository url>
```

## Check the results

Want to see what the result at the end of this chapter should look like? Have a look at the Git repository directory here: [step-2-share-your-ml-experiment-code-with-git](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/step-2-share-your-ml-experiment-code-with-git).

## State of the MLOps process

- ✅ The codebase can be shared among the developers. The codebase can be improved collaboratively;
- ❌ The dataset still needs to be downloaded and placed in the right directory in order to run the experiment;
- ❌ Someone has to tell you the steps used to create the model and they can be forgotten/undocumented;
- ❌ The changes done to a model cannot be visualized and improvements and/or deteriorations are hard to identify;
- ❌ There is no guarantee that the experiment can be executed on another machine;
- ❌ The model might have required artifacts that can be forgotten or omitted when saving/loading the model for future usage. There is no easy way to use the model outside of the experiment context.

## Next & Previous steps

- **Previous**: [Chapter 1: Run a simple ML experiment](/the-guide/chapter-1-run-a-simple-ml-experiment)
- **Next**: [Step 3: Share your ML experiment data with DVC](/the-guide/step-3-share-your-ml-experiment-data-with-dvc)
