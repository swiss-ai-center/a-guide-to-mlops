---
title: "Step 5: Track model evolutions with DVC"
---

# {% $markdoc.frontmatter.title %}

## Summary

{% callout type="note" %}
Highly inspired by the [_Get Started: Metrics, Parameters, and Plots_ - dvc.org](https://dvc.org/doc/start/data-management/metrics-parameters-plots) guide.
{% /callout %}

The purpose of this step is to visualize the improvements/changes made to a model between multiple iterations.

## Instructions

{% callout type="warning" %}
This guide has been written for macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use a decent terminal ([GitBash](https://gitforwindows.org/) for instance) or a Windows Subsystem for Linux (WSL) for optimal results.
{% /callout %}

Update the `.gitignore` file.

```sh
## Custom experiment

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

Visualize the pipeline.

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

Set the plots axes with the following commands. This is only done once.

```sh
# Set the axes for the `precision_recall_curve`
dvc plots modify evaluation/plots/prc.json -x recall -y precision

# Set the axes for the `roc_curve`
dvc plots modify evaluation/plots/sklearn/roc.json -x fpr -y tpr

# Set the axes for the `confusion_matrix`
dvc plots modify evaluation/plots/sklearn/confusion_matrix.json -x actual -y predicted -t confusion
```

Update the parameters to run the experiment in the `params.yaml` file.

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
# Run the experiment. DVC will automatically run all required steps
dvc repro
```

Compare the two iterations.

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
Path             Metric    HEAD     workspace    Change
evaluation.json  avg_prec  0.89668  0.95815      0.06148
evaluation.json  roc_auc   0.92729  0.9701       0.04281
```

```sh
# Display the plots for the `precision_recall_curve` and the `roc_curve` - the output file can be visualized in a browser
dvc plots diff
```

{% callout type="note" %}
Remember? We did set the parameters, metrics and plots in the previous step: [Step 4: Reproduce the experiment with DVC](/the-guide/step-4-reproduce-the-experiment-with-dvc).
{% /callout %}

Push the changes to DVC and git.

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

We now have a simple way to compare the models with the used parameters and metrics.

{% callout type="note" %}
Want to see what the result of this step should look like? Have a look at the Git repository directory here: [step-5-track-model-evolutions-with-dvc](https://github.com/csia-pme/a-guide-to-mlops/tree/main/pages/the-guide/step-5-track-model-evolutions-with-dvc)
{% /callout %}

## State of the MLOps process

## Next & Previous steps

- **Previous**: [Step 4: Reproduce the experiment with DVC](/the-guide/step-4-reproduce-the-experiment-with-dvc)
- **Next**: [Step 6: Orchestrate the workflow with a CI/CD pipeline](/the-guide/step-6-orchestrate-the-workflow-with-a-cicd-pipeline)
