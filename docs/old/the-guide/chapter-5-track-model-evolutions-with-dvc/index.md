# Chapter 5: Track model evolutions with DVC

## Introduction

In the previous chapter, you did set up a DVC pipeline to reproduce your
experiment.

Once this stage is created, you will be able to change our model's configuration,
evaluate the new configuration and compare its performance with the last
commited ones.

In this chapter, you will learn how to:

1. Update the parameters of the experiment
2. Reproduce the experiment
3. Visualize the changes made to the model

Let's get started!

## Steps

### Update the parameters of the experiment

Update your experiment with the following parameters by editing the
`params.yaml` file.

```yaml title="params.yaml" hl_lines="6-7"
prepare:
  split: 0.20
  seed: 20170428

featurize:
  max_features: 200
  ngrams: 2

train:
  seed: 20170428
  n_est: 50
  min_split: 2
```

Check the differences with Git to validate the changes.

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff params.yaml
```

The output should be similar to this.

```diff
diff --git a/params.yaml b/params.yaml
index 83e7649..586d3e2 100644
--- a/params.yaml
+++ b/params.yaml
@@ -3,8 +3,8 @@ prepare:
   seed: 20170428

 featurize:
-  max_features: 100
-  ngrams: 1
+  max_features: 200
+  ngrams: 2

 train:
   seed: 20170428
```

Here, we simply changed the `max_features` and `ngrams` parameters of the
`featurize` stage, which should slightly affect the model's performance.

### Reproduce the experiment

Let's discover if these changes are positive or not! To do so, you will need to
reproduce the experiment.

```sh title="Execute the following command(s) in a terminal"
# Run the experiment. DVC will automatically run all required stages
dvc repro
```

### Compare the two iterations

We will now use DVC to compare your changes with the last commited ones. For DVC,
`HEAD` refers to the last commit on the branch you are working on (at this
moment, the branch `main`), and `workspace` refers to the current state of your
working directory.

!!! note

	Remember? We did set the parameters, metrics and plots
	in the previous chapter: [Chapter 4: Reproduce the experiment with
	DVC](../chapter-4-reproduce-the-experiment-with-dvc).

#### Compare the parameters difference

In order to compare the parameters, you will need to use the `dvc params diff`.
This command will compare the parameters that were set on `HEAD` and the ones in
your current `workspace`.

```sh title="Execute the following command(s) in a terminal"
# Compare the parameters' difference
dvc params diff
```

The output should look like this.

```
Path         Param                   HEAD    workspace
params.yaml  featurize.max_features  100     200
params.yaml  featurize.ngrams        1       2
```

DVC displays the differences between `HEAD` and `workspace`, so you can easily
compare the two iterations.

#### Compare the metrics difference

Similarly, you can use the `dvc metrics diff` command to compare the metrics
that were computed on `HEAD` and the ones that were computed in your current
`workspace`.

```sh title="Execute the following command(s) in a terminal"
# Compare the metrics' difference
dvc metrics diff
```

The output should look like this.

```
Path                     Metric    HEAD     workspace    Change
evaluation/metrics.json  avg_prec  0.89668  0.9202       0.02353
evaluation/metrics.json  roc_auc   0.92729  0.94096      0.01368
```

Again, DVC shows you the differences, so you can easily compare the two
iterations. Here, you can see that the metrics have slightly improved.

#### Compare the plots difference

```sh title="Execute the following command(s) in a terminal"
# Create the report to display the plots
dvc plots diff --open
```

The effect of the `dvc plots diff` command is to create a `dvc_plots` directory
in the working directory. This directory contains a report to visualize the
plots in a browser.

As for the other commands, DVC shows you the differences so you can easily
compare the two iterations.

Here is a preview of the report:

![Plots Diff](../../assets/images/plots_diff.png){ loading=lazy }

#### Summary of the model evolutions

You should notice the improvements made to the model thanks to the DVC reports.
These improvements are small but illustrate the workflow. Try to tweak the
parameters to improve the model and play with the reports to see how your
model's performance changes.

#### Update the .gitignore file

The `dvc plots diff` creates a `dvc_plots` directory in the working directory.
This directory should be ignored by Git.

Add the `dvc_plots` directory to the `.gitignore` file.

```sh title=".gitignore" hl_lines="8-9"
## Python

# Byte-compiled / optimized / DLL files
__pycache__/

## DVC

# DVC plots
dvc_plots

# DVC will add new files after this line
/model.pkl
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
index 165e2c9..a2e21d2 100644
--- a/.gitignore
+++ b/.gitignore
@@ -5,5 +5,8 @@ __pycache__/
 
 ## DVC
 
+# DVC plots
+dvc_plots
+
 # DVC will add new files after this line
 /model.pkl
```

### Check the results

Check the changes with Git to ensure that all the necessary files are tracked.

```sh title="Execute the following command(s) in a terminal"
# Check the changes
git status
```

The output should look like this.

```
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   .gitignore
	modified:   dvc.lock
	modified:   params.yaml

no changes added to commit (use "git add" and/or "git commit -a")
```

!!! warning
	**Do not commit and push the improved version of your model yet**; it will be done in a future chapter.

This chapter is done, you can check the summary.

## Summary

Congrats! You now have a simple way to compare the two iterations of your experiment.

In this chapter, you have successfully:

1. Updated the experiment parameters
2. Reproduced the experiment
3. Visualized the changes made to the experiment

You fixed some of the previous issues:

- ✅ The changes done to a model can be visualized with parameters, metrics and
  plots to identify differences between iterations

You have solid metrics to evaluate the changes before integrating your work in
the code codebase.

You can now safely continue to the next chapter.

## State of the MLOps process

- ✅ The codebase can be shared and improved by multiple developers
- ✅ The dataset can be shared among the developers and is placed in the right
  directory in order to run the experiment
- ✅ The steps used to create the model are documented and can be re-executed
- ✅ The changes done to a model can be visualized with parameters, metrics and
  plots to identify differences between iterations
- ❌ Experiment may not be reproducible on other machines
- ❌ Model may have required artifacts that are forgotten or omitted in
  saved/loaded state and there is no easy way to use the model outside of the
  experiment context

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by the [_Get Started: Metrics, Parameters, and Plots_ -
dvc.org](https://dvc.org/doc/start/data-management/metrics-parameters-plots)
guide.

Want to see what the result at the end of this chapter should look like on your GitHub/GitLab Git repository? Have a
look at the Git repository directory here:
[step-5-track-model-evolutions-with-dvc](https://github.com/csia-pme/a-guide-to-mlops/tree/main/docs/the-guide/step-5-track-model-evolutions-with-dvc).