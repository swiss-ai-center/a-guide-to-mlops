---
title: "Chapter 2: Share your ML experiment code with Git"
---

# {% $markdoc.frontmatter.title %}

## Introduction

Now that you have a good understanding of how the experiment operates, it's time to streamline the codebase sharing process. Instead of relying on outdated methods like transferring from a USB stick, we'll create a Git repository to enable easy collaboration with the rest of the team.

In this chapter, you'll cover:

1. Setting up a new [Git](/get-started/the-tools-used-in-this-guide#git) repository
2. Initializing Git in your project directory
3. Verifying Git tracking for your files
4. Excluding experiment results, data, models and Python environment files from Git commits
5. Pushing your changes to the Git repository

Let's get started!

## Steps

{% callout type="warning" %}
This guide has been written with macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use [GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

### Create a new Git repository

Create a Git repository to collaborate with peers on your preferred Git service.

#### GitHub

Using GitHub? Follow the related documentation [_Creating a new repository_ - docs.github.com](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) to create a new GitHub repository for this chapter.

#### GitLab

Using GitLab? Follow the related documentation [_Create a project_ - docs.gitlab.com](https://docs.gitlab.com/ee/user/project/working_with_projects.html#create-a-project) to create a new GitLab project for this chapter.

### Initialize Git in your working directory

Use the following commands to set up a local Git repository in your working directory. Your Git service should provide instructions for initializing the repository.

```sh
# Initialize Git in your working directory with `main` as the initial branch
git init --initial-branch=main

# Add the remote origin to your newly created repository
git remote add origin <your git repository url>
```

### Check if Git tracks your files

Initialize Git in your working directory. Verify available files for committing with these commands.

```sh
# Check Git status
git status
```

The output should be similar to this.

```
On branch main

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .venv/
        data/
        evaluation/
        src/
        model.pkl
        params.yaml
```

As you can see, no files have been added to Git yet but all available files are shown here to add them.

#### Create a `.gitignore` file

Create a `.gitignore` file to exclude data, models and Python environment to improve repository size and clone time. The data and models will be managed by DVC in the next chapters. You keep the model's evaluation as it doesn't take much space and you can have a history of the improvements made to your model.

```sh
# Data used to train the models
data

# The models
*.pkl

## Python

# Environments
.venv

# Byte-compiled / optimized / DLL files
__pycache__/
```

Verify available files for committing with these commands.

```sh
# Check Git status
git status
```

The output should now be similar to this.

```
On branch main

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        src/
        params.yaml
```

### Push the metadata to Git

```sh
# Add all the available files
git add .

# Commit the changes
git commit -m "My first ML experiment shared on Git"

# Push the changes
git push --set-upstream origin main
```

If you go on your online Git repository, you should see the files.

### Check the results

Congrats! You now have a codebase that can be used and shared among the team.

This chapter is done, you can check the summary.

## Summary

In this chapter, you have successfully:

1. Set up a new Git repository
2. Initialized Git in your project directory
3. Verified Git tracking for your files
4. Excluded experiment results, data, models and Python environment files from Git commits
5. Pushed your changes to the Git repository

You did fix some of the previous issues:

- ✅ Codebase no longer needs manual download and is versioned

When used by another member of the team, they can easily clone the experiment from Git with the following commands.

```sh
# Clone the Git repository
git clone <your git repository url>
```

You can now safely continue to the next chapter.

## State of the MLOps process

- ✅ The codebase can be shared and improved by multiple developers;
- ❌ Dataset requires manual download and placement;
- ❌ Model steps rely on verbal communication and may be undocumented;
- ❌ Changes to model are not easily visualized;
- ❌ Experiment may not be reproducible on other machines;
- ❌ Model may have required artifacts that are forgotten or omitted in saved/loaded state. There is no easy way to use the model outside of the experiment context.

You will address these issues in the next chapters for improved efficiency and collaboration. Continue the guide to learn how.

## Sources

Highly inspired by the [_Creating a new repository_ - docs.github.com](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) and [_Create a project_ - docs.gitlab.com](https://docs.gitlab.com/ee/user/project/working_with_projects.html#create-a-project) guides.

Want to see what the result at the end of this chapter should look like? Have a look at the Git repository directory here: [chapter-2-share-your-ml-experiment-code-with-git](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/chapter-2-share-your-ml-experiment-code-with-git).

## Next & Previous chapters

- **Previous**: [Chapter 1: Run a simple ML experiment](/the-guide/chapter-1-run-a-simple-ml-experiment)
- **Next**: [Chapter 3: Share your ML experiment data with DVC](/the-guide/chapter-3-share-your-ml-experiment-data-with-dvc)
