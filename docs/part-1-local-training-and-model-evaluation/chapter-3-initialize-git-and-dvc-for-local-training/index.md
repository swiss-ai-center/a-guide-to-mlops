# Chapter 3: Initialize Git and DVC for local training

## Introduction

Now that you have a good understanding of the experiment, it's time to
streamline the code sharing process. Instead of relying on ZIP archives, we will
create a Git repository to enable easy collaboration with the rest of the team.

In this chapter, you will learn how to:

1. Set up a new [Git](../../get-started/the-tools-used-in-this-guide#git)
repository
2. Initialize Git in your project directory
3. Verify Git tracking for your files
4. Exclude experiment results, data, models and Python environment files from
Git commits
5. Push your changes to the Git repository

Let's get started!

## Steps

### Create a new Git repository

### Initialize Git in your working directory

Use the following commands to set up a local Git repository in your working
directory. Your Git service should provide these instructions as well.

```sh title="Execute the following command(s) in a terminal"
# Initialize Git in your working directory with `main` as the initial branch
git init --initial-branch=main

# Add the remote origin to your newly created repository
git remote add origin <your git repository url>
```

### Check if Git tracks your files


Initialize Git in your working directory. Verify available files for committing
with these commands.

```sh title="Execute the following command(s) in a terminal"
# Check the changes
git status
```

The output should be similar to this.

```
On branch main

No commits yet

Untracked files:
(use "git add <file>..." to include in what will be committed)
    README.md
    data/
    evaluation/
    model.pkl
    params.yaml
    poetry.lock
    pyproject.toml
    src/
```

As you can see, no files have been added to Git yet.

### Create a .gitignore file

Create a `.gitignore` file to exclude data, models, and Python environment to
improve repository size and clone time. The data and models will be managed by
DVC in the next chapters. Keep the model's evaluation as it doesn't take much
space and you can have a history of the improvements made to your model.
Additionally, this will help to ensure that the repository size and clone time
remain optimized.

```sh title=".gitignore"
# Data used to train the models
data

# Artifacts
evaluation

# The models
*.pkl

## Python

# Byte-compiled / optimized / DLL files
__pycache__/
```

!!! info

    If using macOS, you might want to ignore `.DS_Store` files as well to avoid pushing Apple's metadata files to your repository.

### Check the changes


Check the changes with Git to ensure all wanted files are here.

```sh title="Execute the following command(s) in a terminal"
# Add all the available files
git add .

# Check the changes
git status
```

The output of the `git status` command should be similar to this.

```
On branch main

No commits yet

Changes to be committed:
(use "git rm --cached <file>..." to unstage)
    new file:   .gitignore
    new file:   README.md
    new file:   params.yaml
    new file:   poetry.lock
    new file:   pyproject.toml
    new file:   src/evaluate.py
    new file:   src/featurization.py
    new file:   src/prepare.py
    new file:   src/train.py
```

### Commit the changes to Git

Commit and push the changes to Git.

```sh title="Execute the following command(s) in a terminal"
# Commit the changes
git commit -m "My first ML experiment shared on Git"

# Push the changes
git push --set-upstream origin main
```

## Summary

[TBD]

## State of the MLOps process

[TBD]
