---
title: "Chapter 5: Track model evolutions with DVC"
---

# {% $markdoc.frontmatter.title %}

## Introduction

In the previous chapter, you did set up a DVC pipeline to reproduce your experiment.

Once this stage is created, you'll be able to change our model's configruation, evaluate the new configuration and compare it's performance with the last commited ones. 

In this chapter, you'll cover:

1. Updating the experiment parameters
2. Reproducing the experiment
3. Visualizing the changes made to the model

Let's get started!

## Steps

{% callout type="warning" %}
This guide has been written with macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use [GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

### Update the experiment parameters

Update your experiment with the following parameters in the `params.yaml` file.

```yaml
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

```sh
# Show the differences with Git
git diff params.yaml
```

The output should be similar to this.

```diff
diff --git a/params.yaml b/params.yaml
index a2a290e..8046f85 100644
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

### Reproduce the experiment

Run the experiment.

```sh
# Run the experiment. DVC will automatically run all required stages
dvc repro
```

### Compare the two iterations

In the next steps, the `HEAD` is always the last commit on the branch you are working on (at this moment, the branch `main`). The `workspace` is the current state of your working directory.

{% callout type="note" %}
Remember? We did set the parameters, metrics and plots in the previous chapter: [Chapter 4: Reproduce the experiment with DVC](/the-guide/chapter-4-reproduce-the-experiment-with-dvc).
{% /callout %}

#### Compare the parameters difference

Compare the the difference between the parameters that were set on `HEAD` and the ones in your current `workspace` with the following command.

```sh
# Compare the parameters' difference
dvc params diff
```

The output should look like this.

```
Path         Param                   HEAD    workspace
params.yaml  featurize.max_features  100     200
params.yaml  featurize.ngrams        1       2
```

DVC shows you the differences so you can easily compare the two iterations.

#### Compare the metrics difference

Compare the the difference between the metrics that were set on `HEAD` and the ones in your current `workspace` with the following command.

```sh
# Compare the metrics' difference
dvc metrics diff
```

The output should look like this.

```
Path                     Metric    HEAD     workspace    Change
evaluation/metrics.json  avg_prec  0.89668  0.9202       0.02353
evaluation/metrics.json  roc_auc   0.92729  0.94096      0.01368
```

DVC shows you the differences so you can easily compare the two iterations.

#### Compare the plots difference

```sh
# Display the plots for the `precision_recall_curve` and the `roc_curve` - the output file can be visualized in a browser
dvc plots diff
```

DVC shows you the differences so you can easily compare the two iterations.

#### Summary of the model evolutions

You should notice the improvements made to the model thanks to the DVC reports. These improvements are very small but illustrate the workflow. Try to tweak the parameters to improve the model and play with the reports to see how your model's performance changes.

Do not push the improved version of your model yet, it will be done in a future chapter.

### Check the results

Congrats! You now have a simple way to compare the models with the used parameters and metrics.

This chapter is done, you can check the summary.

## Summary

In this chapter, you have successfully:

1. Updated the experiment parameters
2. Reproducing the experiment
3. Visualizing the changes made to the model

You did fix some of the previous issues:

- ✅ The changes done to a model can be visualized with parameters, metrics and plots to identify differences between iterations.

You have solid metrics to evaluate the changes before intergrating your work in the code codebase.

You can now safely continue to the next chapter.

## State of the MLOps process

- ✅ The codebase can be shared and improved by multiple developers;
- ✅ The dataset can be shared among the developers and is placed in the right directory in order to run the experiment;
- ✅ The steps used to create the model are documented and can be re-executed;
- ✅ The changes done to a model can be visualized with parameters, metrics and plots to identify differences between iterations;
- ❌ Experiment may not be reproducible on other machines;
- ❌ Model may have required artifacts that are forgotten or omitted in saved/loaded state. There is no easy way to use the model outside of the experiment context.

You will address these issues in the next chapters for improved efficiency and collaboration. Continue the guide to learn how.

## Sources

Highly inspired by the [_Get Started: Metrics, Parameters, and Plots_ - dvc.org](https://dvc.org/doc/start/data-management/metrics-parameters-plots) guide.

Want to see what the result at the end of this chapter should look like? Have a look at the Git repository directory here: [step-5-track-model-evolutions-with-dvc](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/step-5-track-model-evolutions-with-dvc).

## Next & Previous chapters

- **Previous**: [Chapter 4: Reproduce the experiment with DVC](/the-guide/chapter-4-reproduce-the-experiment-with-dvc)
- **Next**: [Chapter 6: Orchestrate the workflow with a CI/CD pipeline](/the-guide/chapter-6-orchestrate-the-workflow-with-a-cicd-pipeline)
