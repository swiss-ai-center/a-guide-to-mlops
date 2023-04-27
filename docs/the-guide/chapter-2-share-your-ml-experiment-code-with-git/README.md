# Code

This branch is only intended to keep a backup of the codebase mentioned in the [Get Started: Data Pipelines](https://dvc.org/doc/start/data-management/pipelines). It is only intended to simulate the traditional approach to store and share code among the team.

The codebase contains files to prepare, extract feature, train and evaluate a model from the dataset. The parameters of the experiment can be set in a separted YAML file.

The initial codebase was obtained using the following steps:

```sh
# Download the archive containing the code
wget https://code.dvc.org/get-started/code.zip

# Extract the code
unzip code.zip

# Remove the archive
rm -f code.zip

# Add all the files
git add .

# Commit the changes
git commit -m "Add the code"

# Push the changes
git push
```

As of 2022-12-13, some new Git repositories [_DVC Get Started_ - github.com](https://github.com/iterative/example-get-started) and [_Get Started Tutorial (sources)_ - github.com](https://github.com/iterative/example-repos-dev) have been created that contains the code used in the MLOps guide.
