# Chapter 1.6 - Run and compare experiments with DVC

## Introduction

In the previous chapter, you compared two iterations of your experiment by
editing `params.yaml` and running `dvc repro`. That works, but every parameter
try becomes a new commit on your branch. When you are exploring, most of those
commits are dead ends.

[:simple-dvc: DVC experiments](https://dvc.org/doc/start/experiments) solve this
problem. They let you run a parameter variation without changing your working
files or committing to Git. The experiment is still version-controlled, but it
lives in a temporary DVC ref until you decide to promote it.

In this chapter, you will learn how to:

1. Run a single experiment override with `dvc exp run -S`
2. List experiments with `dvc exp show`
3. Run multiple experiments to compare approaches
4. Compare experiments with `dvc exp diff`
5. Promote the best experiment to a Git branch
6. Clean up discarded experiments

Let's get started!

## Steps

### Run a single experiment override

Update the number of epochs temporarily without editing `params.yaml`:

```sh title="Execute the following command(s) in a terminal"
# Run an experiment with 10 epochs instead of the value in params.yaml
dvc exp run -S train.epochs=10
```

The `-S` flag (short for `--set-param`) overrides a parameter for this run only.
DVC records the override, runs the pipeline, and saves the result as an
experiment.

When the command finishes, your `params.yaml` still contains the original value,
but DVC knows this run used `train.epochs=10`.

### List experiments

Use `dvc exp show` to see the experiments associated with the current commit:

```sh title="Execute the following command(s) in a terminal"
# Show all experiments on the current branch
dvc exp show
```

The output should look similar to this:

```text
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ Experiment                ┃ Created  ┃ epochs  ┃ lr     ┃ f1_score ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ workspace                 │ -        │ 5       │ 0.0001 │ 0.44005  │
│ main                      │ 04:20 PM │ 5       │ 0.0001 │ 0.44005  │
│ └── exp-abc12             │ 04:35 PM │ 10      │ 0.0001 │ 0.64049  │
└───────────────────────────┴──────────┴─────────┴────────┴──────────┘
```

The table shows:

- `workspace` — the current state of your working directory.
- `main` — the last commit on your branch.
- `exp-abc12` — the experiment you just ran, with its parameter override and
  resulting metric.

### Run multiple experiments

Experimentation usually means trying more than one value. Run three different
learning rates:

```sh title="Execute the following command(s) in a terminal"
# Try a smaller learning rate
dvc exp run -S train.lr=0.0001

# Try the current learning rate with more epochs
dvc exp run -S train.lr=0.001 -S train.epochs=10

# Try a larger learning rate
dvc exp run -S train.lr=0.01
```

Each command creates a new experiment. They all share the same parent commit,
but each has its own parameter set and metrics.

!!! tip "Running experiments programmatically"

    If you want to try more values, queue experiments in a loop and let DVC run them
    all:

    ```sh title="Execute the following command(s) in a terminal"
    # Queue experiments, then run them all
    for lr in 0.0001 0.001 0.01; do
        dvc exp run --queue -S train.lr=$lr
    done
    dvc exp run --run-all
    ```

    DVC manages the queue and can run experiments in parallel with the `--jobs`
    option.

List them again:

```sh title="Execute the following command(s) in a terminal"
# Show all experiments
dvc exp show
```

The output should now contain several experiment rows:

```text
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━┓
┃ Experiment                ┃ Created  ┃ epochs  ┃ lr     ┃ f1_score ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━┩
│ workspace                 │ -        │ 5       │ 0.0001 │ 0.44005  │
│ main                      │ 04:20 PM │ 5       │ 0.0001 │ 0.44005  │
│ ├── exp-abc12             │ 04:35 PM │ 10      │ 0.0001 │ 0.64049  │
│ ├── exp-def34             │ 04:40 PM │ 5       │ 0.0001 │ 0.64512  │
│ ├── exp-ghi56             │ 04:45 PM │ 10      │ 0.001  │ 0.68234  │
│ └── exp-jkl78             │ 04:50 PM │ 5       │ 0.01   │ 0.51234  │
└────────────────────────────────────────────────────────────────────┘
```

### Compare experiments

Pick the experiment with the best metric and compare it to another one. For
example, if `exp-ghi56` looks best, compare it to the baseline `main`:

```sh title="Execute the following command(s) in a terminal"
# Compare an experiment to the parent commit
dvc exp diff exp-ghi56
```

The output should look similar to this:

```text
Path         Param         HEAD    exp-ghi56    Change
params.yaml  train.epochs  5       10           5
params.yaml  train.lr      0.0001  0.001        0.0009

Path                     Metric     HEAD     exp-ghi56    Change
evaluation/metrics.json  f1_score   0.44005  0.68234      0.24229
```

You can also compare two experiments directly:

```sh title="Execute the following command(s) in a terminal"
# Compare two experiments
dvc exp diff exp-abc12 exp-ghi56
```

### Promote the best experiment

Once you have identified the best experiment, promote it to a normal Git branch
so it can be reviewed, merged, or pushed:

```sh title="Execute the following command(s) in a terminal"
# Create a branch from the best experiment
dvc exp branch exp-ghi56 tune-lr

# Switch to the new branch
git checkout tune-lr
```

Check the changes:

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff main params.yaml
```

The output should look similar to this:

```diff
diff --git a/params.yaml b/params.yaml
index 5bb698e..a6ff45 100644
--- a/params.yaml
+++ b/params.yaml
@@ -7,7 +7,7 @@ prepare:
 train:
   seed: 77
-  lr: 0.0001
+  lr: 0.001
-  epochs: 5
+  epochs: 10
   conv_size: 32
   dense_size: 64
   output_classes: 11
```

The new branch contains the exact parameter values that produced the best
experiment, along with the updated `dvc.lock` and `metrics.json`.

### Clean up discarded experiments

The other experiments are still stored as DVC refs. They are useful during
exploration but can be removed once you have promoted the winner:

```sh title="Execute the following command(s) in a terminal"
# Remove experiments you no longer need
dvc exp remove exp-abc12 exp-def34 exp-jkl78
```

!!! warning

    Removing an experiment deletes its ref and cached outputs. Only remove
    experiments you are sure you no longer need.

### Check the changes

Check the changes with Git to ensure all necessary files are tracked:

```sh title="Execute the following command(s) in a terminal"
# Add all the files
git add .

# Check the changes
git status
```

The output should look similar to this:

```text
On branch tune-lr
Changes to be committed:
  (use "git restore --staged <file>"... to unstage)
        modified:   dvc.lock
        modified:   evaluation/metrics.json
        modified:   params.yaml
```

### Commit the changes

Commit the promoted experiment to the new branch:

```sh title="Execute the following command(s) in a terminal"
# Commit the changes
git commit -m "Promote best LR experiment"
```

This chapter is done, you can check the summary.

## Summary

Congratulations! You now have a lightweight way to explore parameter changes
without committing every attempt.

In this chapter, you have successfully:

1. Run a single experiment override with `dvc exp run -S`
2. Listed experiments with `dvc exp show`
3. Run multiple experiments with different parameters
4. Compared experiments with `dvc exp diff`
5. Promoted the best experiment to a Git branch
6. Cleaned up discarded experiments

You fixed some of the previous issues:

- [x] Multiple experiments can be compared before choosing one to keep

!!! abstract "Take away"

    - **Experiments are temporary by design**: DVC experiments let you try
      parameter values quickly. Only the experiments you promote become Git branches,
      so your repository stays clean.
    - **Comparison is the goal**: `dvc exp show` and `dvc exp diff` turn
      parameter tuning into a data-driven decision. You choose the best experiment
      based on metrics, not guesswork.
    - **Promotion preserves reproducibility**: When you promote an experiment
      with `dvc exp branch`, you get a normal Git branch that contains the exact code,
      parameters, and lock file needed to reproduce the result.
    - **Cleanup is part of the workflow**: Removing discarded experiments keeps
      the DVC cache and experiment list manageable.

## State of the MLOps process

- [x] Notebook has been transformed into scripts for production
- [x] Codebase and dataset are versioned
- [x] Steps used to create the model are documented and can be reproduced
- [x] Changes done to a model can be visualized with parameters, metrics and
      plots to identify differences between iterations
- [x] Multiple experiments can be compared before choosing one to keep
- [ ] Training metrics cannot be visualized live during the experiment

Continue to
[Chapter 1.7 - Visualize live metrics with DVClive and TensorBoard](./chapter-17-visualize-live-metrics-with-dvclive-and-tensorboard.md)
to add live dashboards to your experiments.

## Sources

Highly inspired by:

- [_Get Started: Experiments_ - dvc.org](https://dvc.org/doc/start/experiments)
