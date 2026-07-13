# Chapter 1.7 - Visualize live metrics with DVClive and TensorBoard

## Introduction

In the previous chapter, you ran several DVC experiments and compared their
final metrics. That is useful, but final metrics do not show the whole story.
You also want to see how loss and accuracy evolve during training, so you can
spot overfitting, instability, or slow convergence early.

[DVClive](https://dvc.org/doc/dvclive) logs metrics during training, and
[TensorBoard](https://github.com/tensorflow/tensorboard) visualizes them in a
browser. Both are lightweight and fit the guide’s composable approach: DVClive
writes logs to local files, and TensorBoard reads those files. No separate
tracking server is required.

In this chapter, you will learn how to:

1. Add `dvclive` and `tensorboard` to your dependencies
2. Modify `src/train.py` to log metrics with DVClive
3. Run an experiment and view its metrics in TensorBoard
4. Compare multiple experiments in the same TensorBoard dashboard
5. Keep DVClive logs out of Git

Let's get started!

## Steps

### Add the dependencies

Add `dvclive` and `tensorboard` to your `requirements.txt` file:

```txt title="requirements.txt" hl_lines="6-7"
matplotlib==3.10.9
scikit-learn==1.9.0
tensorflow==2.21.0
pyyaml==6.0.3
dvc==3.67.1
dvclive==3.48.1
tensorboard==2.21.0
```

Check the differences with Git to validate the changes:

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff requirements.txt
```

The output should be similar to this:

```diff
diff --git a/requirements.txt b/requirements.txt
index 116c388..9f2a1b3 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -4,3 +4,5 @@ tensorflow==2.21.0
 pyyaml==6.0.3
 dvc==3.67.1
+dvclive==3.48.1
+tensorboard==2.21.0
```

Install the dependencies and update the freeze file:

=== ":simple-python: Using pip"

    ```sh title="Execute the following command(s) in a terminal"
    # Install the dependencies
    pip install -r requirements.txt

    # Freeze the dependencies
    pip freeze --local --all > requirements-freeze.txt
    ```

=== ":simple-uv: Using uv"

    ```sh title="Execute the following command(s) in a terminal"
    # Install the dependencies
    uv pip install -r requirements.txt

    # Freeze the dependencies
    uv pip freeze > requirements-freeze.txt
    ```

### Modify the training script

Open `src/train.py` and update it to log metrics with DVClive. The easiest way
is to train one epoch at a time and log the results after each epoch.

Replace the `model.fit(...)` call in `src/train.py` with the following loop:

```py title="src/train.py" hl_lines="1 5 38-52"
from dvclive import Live
import numpy as np
import sys
from pathlib import Path
from typing import Tuple

import tensorflow as tf
import yaml

from utils.seed import set_seed


def get_model(
    image_shape: Tuple[int, int, int],
    conv_size: int,
    dense_size: int,
    output_classes: int,
) -> tf.keras.Model:
    """Create a simple CNN model"""
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Input(shape=image_shape),
            tf.keras.layers.Conv2D(conv_size, (3, 3), activation="relu"),
            tf.keras.layers.MaxPooling2D((3, 3)),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(dense_size, activation="relu"),
            tf.keras.layers.Dense(output_classes),
        ]
    )
    return model


def main() -> None:
    if len(sys.argv) != 3:
        print("Arguments error. Usage:\n")
        print("\tpython3 train.py <prepared-dataset-folder> <model-folder>\n")
        exit(1)

    # Load parameters
    params = yaml.safe_load(open("params.yaml"))
    prepare_params = params["prepare"]
    train_params = params["train"]

    prepared_dataset_folder = Path(sys.argv[1])
    model_folder = Path(sys.argv[2])

    image_size = prepare_params["image_size"]
    grayscale = prepare_params["grayscale"]
    image_shape = (*image_size, 1 if grayscale else 3)

    seed = train_params["seed"]
    lr = train_params["lr"]
    epochs = train_params["epochs"]
    conv_size = train_params["conv_size"]
    dense_size = train_params["dense_size"]
    output_classes = train_params["output_classes"]

    # Set seed for reproducibility
    set_seed(seed)

    # Load data
    ds_train = tf.data.Dataset.load(str(prepared_dataset_folder / "train"))
    ds_val = tf.data.Dataset.load(str(prepared_dataset_folder / "val"))

    # Define the model
    model = get_model(image_shape, conv_size, dense_size, output_classes)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(lr),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )
    model.summary()

    # Initialize DVClive
    live = Live(dir="dvclive")

    # Train the model epoch by epoch and log metrics
    for epoch in range(epochs):
        history = model.fit(
            ds_train,
            epochs=epoch + 1,
            initial_epoch=epoch,
            validation_data=ds_val,
            verbose=0,
        )
        live.log_metric("train/loss", history.history["loss"][-1], step=epoch)
        live.log_metric("train/acc", history.history["sparse_categorical_accuracy"][-1], step=epoch)
        live.log_metric("val/loss", history.history["val_loss"][-1], step=epoch)
        live.log_metric("val/acc", history.history["val_sparse_categorical_accuracy"][-1], step=epoch)
        live.next_step()

    # Save the model
    model_folder.mkdir(parents=True, exist_ok=True)
    model_path = model_folder.absolute() / "model.keras"
    model.save(model_path)

    # Save the model history
    np.save(model_folder.absolute() / "history.npy", model.history.history)

    print(f"\nModel saved at {model_folder.absolute()}")


if __name__ == "__main__":
    main()
```

!!! tip

    DVClive accepts any metric name. Using a slash like `train/loss` lets
    TensorBoard group related metrics in the UI.

Check the differences with Git to validate the changes:

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff src/train.py
```

### Run an experiment

Run a single experiment with DVClive logging enabled:

```sh title="Execute the following command(s) in a terminal"
# Run an experiment
dvc exp run -S train.epochs=10
```

DVClive writes logs to a `dvclive/` directory in your workspace. You can list
the contents:

```sh title="Execute the following command(s) in a terminal"
# List DVClive output
ls dvclive
```

The output should look similar to this:

```text
metrics.json  params.yaml  plots
```

### Launch TensorBoard

Start TensorBoard and point it at the `dvclive` directory:

```sh title="Execute the following command(s) in a terminal"
# Launch TensorBoard
tensorboard --logdir dvclive
```

Open the URL printed in the terminal (usually `http://localhost:6006/`). You
should see the training and validation metrics plotted against epochs.

!!! tip

    TensorBoard watches the log directory. If you leave it running and start a new
    experiment, the dashboard updates automatically.

### Run a second experiment and compare

Leave TensorBoard running and start a second experiment in another terminal:

```sh title="Execute the following command(s) in a terminal"
# Run another experiment with a different learning rate
dvc exp run -S train.lr=0.001 -S train.epochs=10
```

Switch back to the TensorBoard tab. The new experiment appears as a second curve
on the same plots, making it easy to compare learning rates visually.

### Ignore DVClive logs in Git

DVClive logs are only useful for live visualization. The authoritative metrics
and reproduction state are already tracked in `metrics.json`, `dvc.lock`, and
Git. Add `dvclive/` to `.gitignore`:

```sh title=".gitignore" hl_lines="9-10"
## Python
.venv/

# Byte-compiled / optimized / DLL files
__pycache__/

## DVC

# DVC live logs
dvclive/

# DVC plots
dvc_plots

# DVC will add new files after this line
/model
```

Check the differences with Git to validate the changes:

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff .gitignore
```

The output should be similar to this:

```diff
diff --git a/.gitignore b/.gitignore
index cbfa93b..8a2668e 100644
--- a/.gitignore
+++ b/.gitignore
@@ -6,5 +6,8 @@ __pycache__/

 ## DVC

+# DVC live logs
+dvclive/
+
 # DVC plots
 dvc_plots
```

### Check the changes

Check the changes with Git to ensure that all the necessary files are tracked:

```sh title="Execute the following command(s) in a terminal"
# Add all the files
git add .

# Check the changes
git status
```

The output should look similar to this:

```text
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   .gitignore
        modified:   requirements-freeze.txt
        modified:   requirements.txt
        modified:   src/train.py
```

### Commit the changes

Commit the changes to the local Git repository:

```sh title="Execute the following command(s) in a terminal"
# Commit the changes
git commit -m "Add DVClive and TensorBoard for live metric visualization"
```

This chapter is done, you can check the summary.

## Summary

Congratulations! You can now watch your experiments evolve in real time and
compare multiple runs in TensorBoard.

In this chapter, you have successfully:

1. Added `dvclive` and `tensorboard` to your dependencies
2. Modified `src/train.py` to log metrics per epoch
3. Launched TensorBoard and viewed live metrics
4. Compared two experiments in the same dashboard
5. Kept DVClive logs out of Git

You fixed some of the previous issues:

- [x] Training metrics can be visualized live during the experiment

!!! abstract "Take away"

    - **Live metrics reveal training dynamics**: Final metrics tell you whether
      a model improved; live curves tell you why. TensorBoard makes overfitting,
      instability, and slow convergence visible.
    - **DVClive is a file-based logger**: It writes metrics to local files, so
      it works offline and integrates with any storage backend. No tracking server is
      required.
    - **TensorBoard reads DVClive output directly**: Because DVClive uses the
      same summary format as TensorBoard, you can launch TensorBoard against the
      `dvclive/` directory without extra conversion.
    - **Visualization logs are ephemeral**: `dvclive/` is ignored by Git. The
      authoritative experiment record remains `metrics.json`, `dvc.lock`, and the Git
      history.

## State of the MLOps process

- [x] Notebook has been transformed into scripts for production
- [x] Codebase and dataset are versioned
- [x] Steps used to create the model are documented and can be reproduced
- [x] Changes done to a model can be visualized with parameters, metrics and
      plots to identify differences between iterations
- [x] Multiple experiments can be compared before choosing one to keep
- [x] Training metrics can be visualized live during the experiment

Continue to the conclusion to review what you have learned.

## Sources

Highly inspired by:

- [_DVClive_ - dvc.org](https://dvc.org/doc/dvclive)
- [_TensorBoard_ - tensorflow.org](https://www.tensorflow.org/tensorboard)
