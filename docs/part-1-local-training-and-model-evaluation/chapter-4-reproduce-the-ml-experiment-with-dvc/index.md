# Chapter 4: Reproduce the ML experiment with DVC

## Introduction

At this point, the codebase is made available to team members using Git, but the
experiment data is not.

The goal of this chapter is to store the data of the experiment in a version control system.
Git is not suitable for this purpose because of its size limitations.
Git LFS is a solution to this problem, but it is not as efficient as other version control systems.

[DVC](../../get-started/the-tools-used-in-this-guide#dvc) is a version control system for data.
It uses chunking to store large files efficiently and track their changes.
Similar to Git, DVC allows you to store the dataset in a remote storage, typically a cloud storage provider, and track its changes.



4. Install DVC
5. Initialize and configure DVC
6. Update the `.gitignore` file and add the experiment data to DVC
7. Push the data files to DVC
8. Push the metadata files to Git

## Steps

### Install DVC

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
+dvc = {version = "2.37.0", extras = ["gs"]}

[build-system]
requires = ["poetry-core"]
```

### Initialize and configure DVC

Initialize DVC with a Google Storage remote bucket. Replace `<my bucket name>` with your own bucket name. The `dvcstore` is a user-defined path on the bucket. You can change it if needed.

```sh title="Execute the following command(s) in a terminal"
# Initialize DVC in the working directory
dvc init

# Add the Google Storage remote bucket
dvc remote add -d data gs://<my bucket name>/dvcstore
```

The effect of the `dvc init` command is to create a `.dvc` directory in the
working directory. This directory contains the configuration of DVC.

### Update the .gitignore file and add the experiment data to DVC

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

### Push the data files to DVC

DVC works as Git. Once you want to share the data, you can use `dvc push` to
upload the data and its cache to the storage provider.

```sh title="Execute the following command(s) in a terminal"
# Upload the experiment data and cache to the remote bucket
dvc push
```

### Check the changes

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

### Push the changes to Git

You can now push the changes to Git so all team members can get the data from
DVC as well.

```sh title="Execute the following command(s) in a terminal"
# Commit the changes
git commit -m "My ML experiment data is saved with DVC"

# Push the changes
git push
```

This chapter is done, you can check the summary.