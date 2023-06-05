# Chapter 3: Initialize Git and DVC for local training

## Introduction

Now that you have a good understanding of the experiment, it's time to
streamline the code sharing process. We will create a Git repository to enable
tracking of changes and reproducibility.

Later, we will streamline the code sharing process by sharing a remote a Git
repository to enable easy collaboration with the rest of the team.

In this chapter, you will learn how to:

1. Set up a new [Git](../../get-started/the-tools-used-in-this-guide#git)
repository
2. Initialize Git in your project directory
3. Verify Git tracking for your files
4. Exclude experiment results, data, models and Python environment files from
Git commits
5. Push your changes to the Git repository

Let's get started!

At this point, the codebase is made available to team members using Git, but the
experiment data is not.

The goal of this chapter is to store the data of the experiment in a version control system.
Git is not suitable for this purpose because of its size limitations.
Git LFS is a solution to this problem, but it is not as efficient as other version control systems.

[DVC](../../get-started/the-tools-used-in-this-guide#dvc) is a version control system for data.
It uses chunking to store large files efficiently and track their changes.
Similar to Git, DVC allows you to store the dataset in a remote storage, typically a cloud storage provider, and track its changes.

In this chapter, you will learn how to:

4. Install DVC
5. Initialize and configure DVC
6. Update the `.gitignore` file and add the experiment data to DVC
7. Push the data files to DVC
8. Push the metadata files to Git

Let's get started!


## Steps

### Create a new Git repository

#### Initialize Git in your working directory

Use the following commands to set up a local Git repository in your working
directory. Your Git service should provide these instructions as well.

```sh title="Execute the following command(s) in a terminal"
# Initialize Git in your working directory with `main` as the initial branch
git init --initial-branch=main

# Add the remote origin to your newly created repository
git remote add origin <your git repository url>
```

#### Check if Git tracks your files


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
    data/
    evaluation/
    model.pkl
    params.yaml
    poetry.lock
    pyproject.toml
    src/
```

As you can see, no files have been added to Git yet.

#### Create a .gitignore file

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

#### Check the changes


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
    new file:   params.yaml
    new file:   poetry.lock
    new file:   pyproject.toml
    new file:   src/evaluate.py
    new file:   src/featurization.py
    new file:   src/prepare.py
    new file:   src/train.py
```

#### Commit the changes to Git

Commit and push the changes to Git.

```sh title="Execute the following command(s) in a terminal"
# Commit the changes
git commit -m "My first ML experiment shared on Git"

# Push the changes
git push --set-upstream origin main
```

### Create a DVC repository

#### Install DVC

Here, the `dvc[gs]` package enables support for Google Cloud Storage.

```sh title="Execute the following command(s) in a terminal"
poetry add "dvc[gs]==2.37.0"
```

Check the differences with Git to validate the changes.

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff pyproject.toml
```

The output should be similar to this.

```diff
diff --git a/pyproject.toml b/pyproject.toml
index 8a57399..ff11768 100644
--- a/pyproject.toml
+++ b/pyproject.toml
@@ -13,6 +13,7 @@ pyaml = "21.10.1"
scikit-learn = "1.1.3"
scipy = "1.10.1"
matplotlib = "3.6.2"
+dvc = {version = "2.37.0"}

[build-system]
requires = ["poetry-core"]
```

#### Initialize and configure DVC

Initialize DVC with a Google Storage remote bucket. Replace `<my bucket name>` with your own bucket name. The `dvcstore` is a user-defined path on the bucket. You can change it if needed.

```sh title="Execute the following command(s) in a terminal"
# Initialize DVC in the working directory
dvc init
```

The effect of the `dvc init` command is to create a `.dvc` directory in the
working directory. This directory contains the configuration of DVC.


#### Update the .gitignore file and add the experiment data to DVC

Now that DVC has been setup, you can add files to DVC.

Try to add the experiment data. Spoiler: it will fail.

```sh title="Execute the following command(s) in a terminal"
# Try to add the experiment data to DVC
dvc add data/data.xml
```

When executing this command, the following output occurs.

```sh
ERROR: bad DVC file name 'data/data.xml.dvc' is git-ignored.
```

You will have to update the `.gitignore` file so that DVC can create files in
the `data` directory. However, you still don't want the directories
`data/features` and `data/prepared` to be added to Git.

Update the `.gitignore` file by changing `data` to `data/features` and
`data/prepared`.

```sh title=".gitignore" hl_lines="2-3"
# Data used to train the models
data/features
data/prepared

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

Check the differences with Git to validate the changes.

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff .gitignore
```

The output should be similar to this.

```diff
diff --git a/.gitignore b/.gitignore
index be315d6..d65f97a 100644
--- a/.gitignore
+++ b/.gitignore
@@ -1,5 +1,6 @@
# Data used to train the models
-data
+data/features
+data/prepared

# Artifacts
evaluation
```

You can now add the experiment data to DVC without complain!

```sh title="Execute the following command(s) in a terminal"
# Add the experiment data to DVC
dvc add data/data.xml
```

The output should be similar to this. You can safely ignore the warning.

```
To track the changes with git, run:

git add data/data.xml.dvc data/.gitignore

To enable auto staging, run:

dvc config core.autostage true
```

The effect of the `dvc add` command is to create a `data/data.xml.dvc` file and
a `data/.gitignore`. The `.dvc` file contains the metadata of the file that is
used by DVC to download and check the integrity of the files. The `.gitignore`
file is created to add the `data.xml` file to be ignored by Git. The `.dvc`
files must be added to Git.

Various DVC commands will automatically try to update the `.gitignore` files. If a
`.gitignore` file is already present, it will be updated to include the newly
ignored files. You might need to update existing `.gitignore` files accordingly.

#### Push the data files to DVC

DVC works as Git. Once you want to share the data, you can use `dvc push` to
upload the data and its cache to the storage provider.

```sh title="Execute the following command(s) in a terminal"
# Upload the experiment data and cache to the remote bucket
dvc push
```

#### Check the changes

Check the changes with Git to ensure all wanted files are here.

```sh title="Execute the following command(s) in a terminal"
# Add all the files
git add .

# Check the changes
git status
```

The output of the `git status` command should be similar to this.

```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
(use "git restore --staged <file>..." to unstage)
    new file:   .dvc/.gitignore
    new file:   .dvc/config
    new file:   .dvcignore
    modified:   .gitignore
    new file:   data/.gitignore
    new file:   data/README.md
    new file:   data/data.xml.dvc
    modified:   poetry.lock
    modified:   pyproject.toml
```

#### Commit the changes to Git

You can now commit the changes to Git so the data from DVC is tracked along code
changes as well.

```sh title="Execute the following command(s) in a terminal"
# Commit the changes
git commit -m "My ML experiment data is saved with DVC"
```

This chapter is done, you can check the summary.

## Summary

Congrats! You now have a dataset that can be used and shared among the team.

In this chapter, you have successfully:

1. Set up a new Git repository
2. Initialized Git in your project directory
3. Verified Git tracking for your files
4. Excluded experiment results, data, models and Python environment files from Git commits
4. Commited your changes to the Git repository
5. Installed DVC
6. Initialized and configuring DVC
7. Updated the `.gitignore` file and adding the experiment data to DVC
8. Commited the data files to DVC
9. Commited your changes to the Git repository

You fixed some of the previous issues:

- ✅ Data no longer needs manual download and is placed in the right directory.
- ✅ Codebase is versioned

When used by another member of the team, they can easily get a copy of the
experiment data from DVC with the following command.

```sh title="Execute the following command(s) in a terminal"
# Download experiment data from DVC
dvc pull
```

You can now safely continue to the next chapter.

## State of the MLOps process

!!! bug

    `[TBD]`
