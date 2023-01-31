---
title: "Chapter 5: Track model evolutions with DVC"
---

# {% $markdoc.frontmatter.title %}

## Summary

{% callout type="note" %}
Highly inspired by the [_Get Started: Metrics, Parameters, and Plots_ - dvc.org](https://dvc.org/doc/start/data-management/metrics-parameters-plots) guide.
{% /callout %}

Now that the first 3 steps of the experiment are configured as the stages of a DVC pipeline, we will add the last step `evaluate` and configure dvc plots to display it.

Our `evaluate` step generates a `metrics.json` file used to store performance indicators of our model with it's new parameters.

We will configure a DVC stage that evaluates the model and enables us to compare the result of the unstaged evaluation with the last commited evaluation.

Once this stage is created, we will be able to change our model's configruation, evaluate the new configuration and compare it's performance with the last commited ones with. 

## Instructions

{% callout type="warning" %}
This guide has been written with macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use [GitBash](https://gitforwindows.org/) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

Update the `.gitignore` file.

```sh
## Python

# Environments
.venv

# Byte-compiled / optimized / DLL files
__pycache__/

## DVC

# The plots created by DVC
dvc_plots

# Files added by DVC
/model.pkl
```

#### Create a DVC stage to evaluate the model

Store the command to evaluate the model in DVC.

```sh
dvc stage add -n evaluate \
  -d src/evaluate.py -d model.pkl -d data/features \
  -O evaluation/plots/metrics \
  --metrics-no-cache evaluation/metrics.json \
  --plots-no-cache evaluation/plots/prc.json \
  --plots-no-cache evaluation/plots/sklearn/roc.json \
  --plots-no-cache evaluation/plots/sklearn/confusion_matrix.json \
  --plots evaluation/plots/importance.png \
  python src/evaluate.py model.pkl data/features
```

This command adds a new stage called _evaluate_ that has the `src/evaluate.py`, `model.pkl` and `data/features` files as a dependency.

If any of these files change, DVC will run the command `python src/evaluate.py model.pkl data/features` when using `dvc repro`.

This command writes the model's metrics to `evaluation/metrics.json`. It writes the `confusion_matrix` to `evaluation/plots/sklearn/confusion_matrix.json`, the `precision_recall_curve` to `evaluation/plots/prc.json ` and the `roc_curve` to `evaluation/plots/sklearn/roc.json` that will be used to create plots.

#### Visualize the pipeline.

```sh
# Display the Directed Acyclic Graph of the pipeline
dvc dag
```

```
    +-------------------+
    | data/data.xml.dvc |
    +-------------------+
              *
              *
              *
         +---------+
         | prepare |
         +---------+
              *
              *
              *
        +-----------+
        | featurize |
        +-----------+
         **        **
       **            *
      *               **
+-------+               *
| train |             **
+-------+            *
         **        **
           **    **
             *  *
        +----------+
        | evaluate |
        +----------+
```

#### Setup the plots

Set the plots axes with the following commands. This is only done once.

```sh
# Set the axes for the `precision_recall_curve`
dvc plots modify evaluation/plots/prc.json -x recall -y precision

# Set the axes for the `roc_curve`
dvc plots modify evaluation/plots/sklearn/roc.json -x fpr -y tpr

# Set the axes for the `confusion_matrix`
dvc plots modify evaluation/plots/sklearn/confusion_matrix.json -x actual -y predicted -t confusion
```

#### Push the changes to DVC and Git.


```sh
# Upload the experiment data and cache to the remote bucket
dvc push

# Add all the files
git add .

# Commit the changes
git commit -m "Set the baseline model metrics and parameters"

# Push the changes
git push
```

{% callout type="note" %}
This is necessary so the next commands can display a difference between the current workspace and the `HEAD` of the Git repository.
{% /callout %}

#### A new experiment

Create a new experiment with the following parameters.


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

Run the experiment.

```sh
# Run the experiment. DVC will automatically run all required stages
dvc repro
```

#### Compare the two iterations.

```sh
# Compare the parameters' difference
dvc params diff
```

```
Path         Param                   HEAD    workspace
params.yaml  featurize.max_features  100     200
params.yaml  featurize.ngrams        1       2
```

```sh
# Compare the metrics' difference
dvc metrics diff
```

```
Path                     Metric    HEAD     workspace    Change
evaluation/metrics.json  avg_prec  0.89668  0.9202       0.02353
evaluation/metrics.json  roc_auc   0.92729  0.94096      0.01368
```

```sh
# Display the plots for the `precision_recall_curve` and the `roc_curve` - the output file can be visualized in a browser
dvc plots diff
```

{% callout type="note" %}
Remember? We did set the parameters, metrics and plots in the previous chapter: [Chapter 4: Reproduce the experiment with DVC](/the-guide/chapter-4-reproduce-the-experiment-with-dvc).
{% /callout %}

#### Push the changes to DVC and Git.


```sh
# Upload the experiment data and cache to the remote bucket
dvc push

# Add all the files
git add .

# Commit the changes
git commit -m "I did improve the model performance"

# Push the changes
git push
```

Congrats! You now have a simple way to compare the models with the used parameters and metrics.

## Check the results

Want to see what the result at the end of this chapter should look like? Have a look at the Git repository directory here: [step-5-track-model-evolutions-with-dvc](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/step-5-track-model-evolutions-with-dvc).

## State of the MLOps process

- ✅ The codebase can be shared among the developers. The codebase can be improved collaboratively;
- ✅ The dataset can be shared among the developers and is placed in the right directory in order to run the experiment;
- ✅ The steps used to create the model are documented and can be re-executed;
- ✅ The changes done to a model can be visualized with parameters, metrics and plots to identify differences between iterations;
- ❌ There is no guarantee that the experiment can be executed on another machine;
- ❌ The model might have required artifacts that can be forgotten or omitted when saving/loading the model for future usage. There is no easy way to use the model outside of the experiment context.

## Next & Previous chapters

- **Previous**: [Chapter 4: Reproduce the experiment with DVC](/the-guide/chapter-4-reproduce-the-experiment-with-dvc)
- **Next**: [Chapter 6: Orchestrate the workflow with a CI/CD pipeline](/the-guide/chapter-6-orchestrate-the-workflow-with-a-cicd-pipeline)
