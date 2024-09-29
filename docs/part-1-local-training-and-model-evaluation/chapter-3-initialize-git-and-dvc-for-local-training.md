# Chapter 3 - Initialize Git and DVC for local training

## Introduction

Now that you have a good understanding of the experiment, it's time to improve
the code and data sharing process. To share the codebase, you will create a
[:simple-git: Git](../tools.md) repository.

However, when it comes to managing large files, Git has some limitations.
Although Git LFS is an option for handling large files in Git repositories, it
may not be the most efficient solution.

This is the reason you will use [:simple-dvc: DVC](../tools.md), a version
control system specifically designed to share the data and integrates well with
Git. DVC utilizes chunking to efficiently store large files and track their
changes.

In this chapter, you will learn how to:

1. Set up a new Git repository
2. Initialize Git in your project directory
3. Verify Git tracking for your files
4. Exclude experiment results, data, models and Python environment files from
   Git commits
5. Commit your changes to the Git repository
6. Install DVC
7. Initialize and configure DVC
8. Update the gitignore file and add the experiment data to DVC
9. Push the data files to DVC
10. Commit the metadata files to Git

The following diagram illustrates the control flow of the experiment at the end
of this chapter:

```mermaid
flowchart TB
    dot_dvc[(.dvc)]
    dot_git[(.git)]
    data[data/raw] <-.-> dot_dvc
    workspaceGraph <-....-> dot_git
    subgraph cacheGraph[CACHE]
        dot_dvc
        dot_git
    end
    subgraph workspaceGraph[WORKSPACE]
        data --> prepare
        prepare[prepare.py] --> train
        train[train.py] --> evaluate[evaluate.py]
        params[params.yaml] -.- prepare
        params -.- train
    end
    style workspaceGraph opacity:0.4,color:#7f7f7f80
    style prepare opacity:0.4,color:#7f7f7f80
    style train opacity:0.4,color:#7f7f7f80
    style evaluate opacity:0.4,color:#7f7f7f80
    style params opacity:0.4,color:#7f7f7f80
    linkStyle 2 opacity:0.4,color:#7f7f7f80
    linkStyle 3 opacity:0.4,color:#7f7f7f80
    linkStyle 4 opacity:0.4,color:#7f7f7f80
    linkStyle 5 opacity:0.4,color:#7f7f7f80
    linkStyle 6 opacity:0.4,color:#7f7f7f80
```

In future chapters, you will improve the code sharing process by setting up
remote Git and DVC repositories to enable easy collaboration with the rest of
the team.

## Steps

### Create a new Git repository

#### Initialize Git in your working directory

Use the following command to set up a local Git repository in your working
directory:

```sh title="Execute the following command(s) in a terminal"
# Initialize Git in your working directory with `main` as the initial branch
git init --initial-branch=main
```

#### Check if Git tracks your files

Initialize Git in your working directory. Verify available files for committing
with this command:

```sh title="Execute the following command(s) in a terminal"
# Check the changes
git status
```

The output should be similar to this:

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
    .venv/
    README.md
    data/
    evaluation/
    model/
    params.yaml
    requirements-freeze.txt
    requirements.txt
    src/

nothing added to commit but untracked files present (use "git add" to track)
```

As you can see, no files have been added to Git yet.

#### Create a .gitignore file

Create a `.gitignore` file to exclude data, models, and Python environment to
improve repository size and clone time. The data and models will be managed by
DVC in the next chapters. Keep the model's evaluation as it doesn't take much
space and you can have a history of the improvements made to your model.
Additionally, this will help to ensure that the repository size and clone time
remain optimized:

```sh title=".gitignore"
# Data used to train the models
data/

# Evaluation results
evaluation/

# The models
model/

## Python
.venv/

# Byte-compiled / optimized / DLL files
__pycache__/
```

!!! info

    If using macOS, you might want to ignore `.DS_Store` files as well to avoid
    pushing Apple's metadata files to your repository.

#### Check the changes

Check the changes with Git to ensure all wanted files are here with the
following commands:

```sh title="Execute the following command(s) in a terminal"
# Add all the available files
git add .

# Check the changes
git status
```

The output of the `git status` command should be similar to this:

```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
    new file:   .gitignore
    new file:   README.md
    new file:   params.yaml
    new file:   requirements-freeze.txt
    new file:   requirements.txt
    new file:   src/evaluate.py
    new file:   src/prepare.py
    new file:   src/train.py
    new file:   src/utils/__init__.py
    new file:   src/utils/seed.py
```

#### Commit the changes

Commit the changes to Git:

```sh title="Execute the following command(s) in a terminal"
# Commit the changes
git commit -m "My first ML experiment versioned with Git"
```

### Create a DVC repository

#### Install DVC

Add the main `dvc` dependency to the `requirements.txt` file:

```txt title="requirements.txt" hl_lines="4"
tensorflow==2.17.0
matplotlib==3.9.2
pyyaml==6.0.2
dvc==3.53.2
```

Check the differences with Git to validate the changes:

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff requirements.txt
```

The output should be similar to this:

```diff
diff --git a/requirements.txt b/requirements.txt
index 250f32c..152b868 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -1,3 +1,4 @@
 tensorflow==2.17.0
 matplotlib==3.9.2
 pyyaml==6.0.2
+dvc==3.53.2
```

Install the dependencies and update the freeze file:

!!! warning

    Prior to running any pip commands, it is crucial to ensure the virtual
    environment is activated to avoid potential conflicts with system-wide Python
    packages.

    To check its status, simply run `pip -V`. If the virtual environment is active,
    the output will show the path to the virtual environment's Python executable. If
    it is not, you can activate it with `source .venv/bin/activate`.

```sh title="Execute the following command(s) in a terminal"
# Install the dependencies
pip install --requirement requirements.txt

# Freeze the dependencies
pip freeze --local --all > requirements-freeze.txt
```

#### Initialize DVC

Initialize DVC in the current project.

```sh title="Execute the following command(s) in a terminal"
# Initialize DVC in the working directory
dvc init
```

The `dvc init` command creates a `.dvc` directory in the working directory,
which serves as the configuration directory for DVC.

#### Update the .gitignore file and add the experiment data to DVC

With DVC now set up, you can begin adding files to it.

Try to add the experiment data. Spoiler, it will fail:

```sh title="Execute the following command(s) in a terminal"
# Try to add the experiment data to DVC
dvc add data/raw/
```

When executing this command, the following output occurs:

```text
ERROR: bad DVC file name 'data/data.raw.dvc' is git-ignored.
```

You will have to update the gitignore file so that DVC can create files in the
`data` directory. However, you still don't want the directories `data/raw` and
`data/prepared` to be added to Git.

Update the gitignore file by changing `data/` to `data/raw/` and
`data/prepared/`:

```sh title=".gitignore" hl_lines="2-3"
# Data used to train the models
data/raw/
data/prepared/

# Evaluation results
evaluation/

# The models
model/

## Python
.venv/

# Byte-compiled / optimized / DLL files
__pycache__/
```

!!! info

    If using macOS, you might want to ignore `.DS_Store` files as well to avoid
    pushing Apple's metadata files to your repository.

Check the differences with Git to validate the changes:

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff .gitignore
```

The output should be similar to this:

```diff
diff --git a/.gitignore b/.gitignore
index dc17ed7..1c13140 100644
--- a/.gitignore
+++ b/.gitignore
@@ -1,5 +1,6 @@
 # Data used to train the models
-data/
+data/raw/
+data/prepared/

 # Evaluation results
 evaluation/
```

You can now add the experiment data to DVC without complain:

```sh title="Execute the following command(s) in a terminal"
# Add the experiment data to DVC
dvc add data/raw/
```

The output should be similar to this. You can safely ignore the message:

```text
To track the changes with git, run:

    git add data/raw.dvc data/.gitignore

To enable auto staging, run:

    dvc config core.autostage true
```

The effect of the `dvc add` command is to create a `data/data.raw.dvc` file and
a `data/.gitignore`. The `.dvc` file contains the metadata of the file that is
used by DVC to download and check the integrity of the files. The gitignore file
is created to add the files in `data/raw` to be ignored by Git. The `.dvc` files
must be added to Git.

Various DVC commands will automatically try to update the gitignore files. If a
gitignore file is already present, it will be updated to include the newly
ignored files. You might need to update existing `.gitignore` files accordingly.

#### Check the changes

Check the changes with Git to ensure all wanted files are here.

```sh title="Execute the following command(s) in a terminal"
# Add all the files
git add .

# Check the changes
git status
```

The output of the `git status` command should be similar to this.

```text
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
    new file:   .dvc/.gitignore
    new file:   .dvc/config
    new file:   .dvcignore
    modified:   .gitignore
    new file:   data/.gitignore
    new file:   data/README.md
    new file:   data/raw.dvc
    modified:   requirements-freeze.txt
    modified:   requirements.txt
```

#### Commit the changes to Git

You can now commit the changes to Git so the data from DVC is tracked along code
changes as well.

```sh title="Execute the following command(s) in a terminal"
# Commit the changes
git commit -m "My first ML experiment data versioned with DVC"
```

This chapter is done, you can check the summary.

## Summary

Congratulations! You now have a codebase and a dataset that is versioned with
Git and DVC. At the moment, these tools are only used locally. In the next
chapters, you will learn how to share the codebase and the dataset with the rest
of the team.

In this chapter, you have successfully:

1. Set up a new Git repository
2. Initialized Git in your project directory
3. Verified Git tracking for your files
4. Excluded experiment results, data, models and Python environment files from
   Git commits
4. Commited your changes to the Git repository
5. Installed DVC
6. Initialized DVC
7. Updated the gitignore file and adding the experiment data to DVC
8. Commited the data files to DVC
9. Commited your changes to the Git repository

You fixed some of the previous issues:

- [x] Data no longer needs manual download and is placed in the right directory.
- [x] Codebase is versioned

You can now safely continue to the next chapter.

## State of the MLOps process

- [x] Notebook has been transformed into scripts for production
- [x] Codebase and dataset are versioned
- [ ] Model steps rely on verbal communication and may be undocumented
- [ ] Changes to model are not easily visualized
- [ ] Codebase requires manual download and setup
- [ ] Dataset requires manual download and placement
- [ ] Experiment may not be reproducible on other machines
- [ ] CI/CD pipeline does not report the results of the experiment
- [ ] Changes to model are not thoroughly reviewed and discussed before
      integration
- [ ] Model may have required artifacts that are forgotten or omitted in
      saved/loaded state
- [ ] Model cannot be easily used from outside of the experiment context
- [ ] Model requires manual publication to the artifact registry
- [ ] Model is not accessible on the Internet and cannot be used anywhere
- [ ] Model requires manual deployment on the cluster
- [ ] Model cannot be trained on hardware other than the local machine

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by:

- [_Get Started_ - dvc.org](https://dvc.org/doc/start)
- [_Get Started: Data Versioning_ - dvc.org](https://dvc.org/doc/start/data-management)
