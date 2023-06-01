# Chapter 5: Track model evolutions with DVC

## Introduction

[moved]

## Steps

### Update the parameters of the experiment

[moved]

### Reproduce the experiment

[moved]

### Compare the two iterations

[moved]

#### Update the .gitignore file

[moved]

### Check the results

[moved]

## Summary

[moved]

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
