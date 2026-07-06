# Chapter 3.1 - Save and load the model with BentoML

## Introduction

The purpose of this chapter is to serve and use the model for usage outside of
the experiment context with the help of [:simple-bentoml: BentoML](../tools.md),
a tool designed for easy packaging, deployment, and serving of Machine Learning
models.

By transforming your model into a BentoML model artifact, it is possible to load
the model for future usage with all its dependencies. This will allow you to use
the model in a production environment, share it with others, and deploy it to a
cluster.

In this chapter, you will learn how to:

1. Install BentoML
2. Learn about BentoML's model store
3. Update and run the experiment to use BentoML to save and load the model to
   and from the model's store

The following diagram illustrates the control flow of the experiment at the end
of this chapter:

```mermaid
flowchart TB
    dot_dvc[(.dvc)] <-->|dvc pull
                         dvc push| s3_storage[(S3 Storage)]
    dot_git[(.git)] <-->|git pull
                         git push| gitGraph[Git Remote]
    workspaceGraph <-....-> dot_git
    data[data/raw]
    subgraph remoteGraph[REMOTE]
        s3_storage
        subgraph gitGraph[Git Remote]
            repository[(Repository)] --> action[Action]
            action --> |dvc pull
                        dvc repro
                        cml publish|request[PR]
            request --> repository[(Repository)]
        end
    end
    subgraph cacheGraph[CACHE]
        dot_dvc
        dot_git
    end
    subgraph workspaceGraph[WORKSPACE]
        data --> code[*.py]
        subgraph dvcGraph["dvc.yaml"]
            code
        end
        params[params.yaml] -.- code
        bento_model[classifier.bentomodel]
        bento_model <-.-> dot_dvc
        code --> |save_model
                  export_model|bento_model
        bento_model --> |import_model
                         load_model|code
    end
    style workspaceGraph opacity:0.4,color:#7f7f7f80
    style dvcGraph opacity:0.4,color:#7f7f7f80
    style cacheGraph opacity:0.4,color:#7f7f7f80
    style data opacity:0.4,color:#7f7f7f80
    style dot_git opacity:0.4,color:#7f7f7f80
    style dot_dvc opacity:0.4,color:#7f7f7f80
    style code opacity:0.4,color:#7f7f7f80
    style params opacity:0.4,color:#7f7f7f80
    style s3_storage opacity:0.4,color:#7f7f7f80
    style repository opacity:0.4,color:#7f7f7f80
    style action opacity:0.4,color:#7f7f7f80
    style request opacity:0.4,color:#7f7f7f80
    style remoteGraph opacity:0.4,color:#7f7f7f80
    style gitGraph opacity:0.4,color:#7f7f7f80
    linkStyle 0 opacity:0.4,color:#7f7f7f80
    linkStyle 1 opacity:0.4,color:#7f7f7f80
    linkStyle 2 opacity:0.4,color:#7f7f7f80
    linkStyle 3 opacity:0.4,color:#7f7f7f80
    linkStyle 4 opacity:0.4,color:#7f7f7f80
    linkStyle 5 opacity:0.4,color:#7f7f7f80
    linkStyle 6 opacity:0.4,color:#7f7f7f80
    linkStyle 7 opacity:0.4,color:#7f7f7f80
```

## Steps

### Install BentoML and dependencies

Add the `bentoml` package to install BentoML support. `pillow` is also added to
support image processing:

```txt title="requirements.txt" hl_lines="6-7"
matplotlib==3.10.9
scikit-learn==1.9.0
tensorflow==2.21.0
pyyaml==6.0.3
dvc[gs]==3.67.1
bentoml==1.4.39
pillow==12.2.0
```

Check the differences with Git to validate the changes:

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff requirements.txt
```

The output should be similar to this:

```diff
diff --git a/requirements.txt b/requirements.txt
index 5f775da..39ed63e 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -3,3 +3,5 @@ scikit-learn==1.9.0
 tensorflow==2.21.0
 pyyaml==6.0.3
 dvc[gs]==3.67.1
+bentoml==1.4.39
+pillow==12.2.0
```

Install the package and update the freeze file.

!!! warning

    Prior to running any pip commands, it is crucial to ensure the virtual
    environment is activated to avoid potential conflicts with system-wide Python
    packages.

    To check its status, simply run `which python`. If the virtual environment is
    active, the output will show the path to the virtual environment's Python
    executable. If it is not, you can activate it with `source .venv/bin/activate`.

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

### Update the experiment

To make the most of BentoML's capabilities, you must start by converting your
model into the specialized BentoML model artifact format with all its
dependencies.

BentoML offers a model store, which is a centralized repository for all your
models. This store is stored in a directory on your local machine at
`~/bentoml/`.

In order to share the model with others, the model must be exported in the
current working directory. It will then be uploaded to DVC and shared with
others.

#### Update `src/train.py`

Update the `src/train.py` file to save the model with BentoML:

```py title="src/train.py" hl_lines="1 9-10 67-69 88-125"
import json
import sys
from pathlib import Path
from typing import Tuple

import numpy as np
import tensorflow as tf
import yaml
import bentoml
from PIL.Image import Image

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

    with open(prepared_dataset_folder / "labels.json") as f:
        labels = json.load(f)

    # Define the model
    model = get_model(image_shape, conv_size, dense_size, output_classes)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(lr),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )
    model.summary()

    # Train the model
    model.fit(
        ds_train,
        epochs=epochs,
        validation_data=ds_val,
    )

    # Save the model
    model_folder.mkdir(parents=True, exist_ok=True)

    def preprocess(x: Image):
        # convert PIL image to tensor
        x = x.convert("L" if grayscale else "RGB")
        x = x.resize(image_size)
        x = np.array(x, dtype=np.float32) / 255.0
        # add channel dimension for grayscale
        if x.ndim == 2:
            x = np.expand_dims(x, axis=-1)
        # add batch dimension
        x = np.expand_dims(x, axis=0)
        return x

    def postprocess(x: Image):
        return {
            "prediction": labels[tf.argmax(x, axis=-1).numpy()[0]],
            "probabilities": {
                labels[i]: prob
                for i, prob in enumerate(tf.nn.softmax(x).numpy()[0].tolist())
            },
        }

    # Save the model using BentoML to its model store
    bentoml.keras.save_model(
        "celestial_bodies_classifier_model",
        model,
        include_optimizer=True,
        custom_objects={
            "preprocess": preprocess,
            "postprocess": postprocess,
        },
    )

    # Export the model from the model store to the local model folder
    bentoml.models.export_model(
        "celestial_bodies_classifier_model:latest",
        f"{model_folder.absolute()}/celestial_bodies_classifier_model.bentomodel",
    )

    # Save the model history
    np.save(model_folder.absolute() / "history.npy", model.history.history)

    print(f"\nModel saved at {model_folder.absolute()}")


if __name__ == "__main__":
    main()
```

BentoML can save the model with custom objects.

These custom objects can be used to save the model with arbitrary data that can
be used afterword when loading back the model. In this case, the following
objects are saved with the model:

- `preprocess` is used to preprocess the input data before feeding it to the
  model.
- `postprocess` is used to postprocess the output of the model.

These functions will be used later to transform the input and output data when
using the model through a HTTP REST API.

Check the differences with Git to better understand the changes:

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff src/train.py
```

The output should be similar to this:

```diff
diff --git a/src/train.py b/src/train.py
index efbb6a0..0bc4749 100644
--- a/src/train.py
+++ b/src/train.py
@@ -1,3 +1,4 @@
+import json
 import sys
 from pathlib import Path
 from typing import Tuple
@@ -5,6 +6,8 @@ from typing import Tuple
 import numpy as np
 import tensorflow as tf
 import yaml
+import bentoml
+from PIL.Image import Image

 from utils.seed import set_seed

@@ -61,6 +64,9 @@ def main() -> None:
     ds_train = tf.data.Dataset.load(str(prepared_dataset_folder / "train"))
     ds_val = tf.data.Dataset.load(str(prepared_dataset_folder / "val"))

+    with open(prepared_dataset_folder / "labels.json") as f:
+        labels = json.load(f)
+
     # Define the model
     model = get_model(image_shape, conv_size, dense_size, output_classes)
     model.compile(
@@ -79,8 +85,44 @@ def main() -> None:

     # Save the model
     model_folder.mkdir(parents=True, exist_ok=True)
-    model_path = model_folder.absolute() / "model.keras"
-    model.save(model_path)
+
+    def preprocess(x: Image):
+        # convert PIL image to tensor
+        x = x.convert("L" if grayscale else "RGB")
+        x = x.resize(image_size)
+        x = np.array(x, dtype=np.float32) / 255.0
+        # add channel dimension for grayscale
+        if x.ndim == 2:
+            x = np.expand_dims(x, axis=-1)
+        # add batch dimension
+        x = np.expand_dims(x, axis=0)
+        return x
+
+    def postprocess(x: Image):
+        return {
+            "prediction": labels[tf.argmax(x, axis=-1).numpy()[0]],
+            "probabilities": {
+                labels[i]: prob
+                for i, prob in enumerate(tf.nn.softmax(x).numpy()[0].tolist())
+            },
+        }
+
+    # Save the model using BentoML to its model store
+    bentoml.keras.save_model(
+        "celestial_bodies_classifier_model",
+        model,
+        include_optimizer=True,
+        custom_objects={
+            "preprocess": preprocess,
+            "postprocess": postprocess,
+        },
+    )
+
+    # Export the model from the model store to the local model folder
+    bentoml.models.export_model(
+        "celestial_bodies_classifier_model:latest",
+        f"{model_folder.absolute()}/celestial_bodies_classifier_model.bentomodel",
+    )

     # Save the model history
     np.save(model_folder.absolute() / "history.npy", model.history.history)
```

#### Update `src/evaluate.py`

Update the `src/evaluate.py` file to load the model from BentoML:

```py title="src/evaluate.py" hl_lines="15 106-113 115"
import json
import sys
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    f1_score,
    precision_score,
    recall_score,
)
import bentoml


def get_training_plot(model_history: dict) -> plt.Figure:
    """Plot the training and validation loss"""
    epochs = range(1, len(model_history["loss"]) + 1)

    fig = plt.figure(figsize=(10, 4))
    plt.plot(epochs, model_history["loss"], label="Training loss")
    plt.plot(epochs, model_history["val_loss"], label="Validation loss")
    plt.xticks(epochs)
    plt.title("Training and validation loss")
    plt.xlabel("Epochs")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)

    return fig


def get_pred_preview_plot(
    model: tf.keras.Model, ds_val: tf.data.Dataset, labels: List[str]
) -> plt.Figure:
    """Plot a preview of the predictions"""
    fig, axes = plt.subplots(2, 5, figsize=(10, 5), tight_layout=True)
    for images, label_idxs in ds_val.take(1):
        pred_idxs = np.argmax(model.predict(images, verbose=0), axis=1)
        for ax, image, true_idx, pred_idx in zip(
            axes.ravel(), images, label_idxs, pred_idxs
        ):
            true_label = labels[true_idx.numpy()]
            pred_label = labels[pred_idx]
            ax.imshow(image.numpy().squeeze(), cmap="gray")
            ax.set_title(f"True: {true_label}\nPred: {pred_label}")
            ax.set_xticks([])
            ax.set_yticks([])

            border_color = "lime" if true_idx.numpy() == pred_idx else "red"
            for spine in ax.spines.values():
                spine.set_edgecolor(border_color)
                spine.set_linewidth(4)

    return fig


def get_confusion_matrix_plot(
    y_true: np.ndarray, y_pred: np.ndarray, labels: List[str]
) -> plt.Figure:
    """Plot the confusion matrix"""
    fig, ax = plt.subplots(figsize=(6, 6), tight_layout=True)
    display = ConfusionMatrixDisplay.from_predictions(
        y_true,
        y_pred,
        display_labels=labels,
        normalize="true",
        cmap="Blues",
        values_format=".2f",
        ax=ax,
        colorbar=True,
    )

    for value, text in zip(display.confusion_matrix.ravel(), display.text_.ravel()):
        text.set_fontsize(7)
        if np.isclose(value, 0.0):
            text.set_color("lightgray")

    ax.set_xticklabels(labels, rotation=90)
    ax.set_title("Validation confusion matrix")

    return fig


def main() -> None:
    if len(sys.argv) != 3:
        print("Arguments error. Usage:\n")
        print("\tpython3 evaluate.py <model-folder> <prepared-dataset-folder>\n")
        exit(1)

    model_folder = Path(sys.argv[1])
    prepared_dataset_folder = Path(sys.argv[2])
    evaluation_folder = Path("evaluation")
    plots_folder = Path("plots")

    # Create folders
    (evaluation_folder / plots_folder).mkdir(parents=True, exist_ok=True)

    # Load files
    ds_val = tf.data.Dataset.load(str(prepared_dataset_folder / "val"))
    with open(prepared_dataset_folder / "labels.json") as f:
        labels = json.load(f)

    # Import the model to the model store from a local model folder
    try:
        bentoml.models.import_model(
            f"{model_folder.absolute()}/celestial_bodies_classifier_model.bentomodel"
        )
    except bentoml.exceptions.BentoMLException:
        print("Model already exists in the model store - skipping import.")

    # Load model
    model = bentoml.keras.load_model("celestial_bodies_classifier_model")
    model_history = np.load(
        model_folder.absolute() / "history.npy", allow_pickle=True
    ).item()

    # Log metrics
    val_loss, val_acc = model.evaluate(ds_val)
    preds = model.predict(ds_val)
    y_true = tf.concat([y for _, y in ds_val], axis=0).numpy()
    y_pred = np.argmax(preds, axis=1)

    metrics = {
        "val_loss": val_loss,
        "val_acc": val_acc,
        "precision": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall": recall_score(y_true, y_pred, average="macro", zero_division=0),
        "f1_score": f1_score(y_true, y_pred, average="macro", zero_division=0),
    }

    print(f"Validation loss: {metrics['val_loss']:.2f}")
    print(f"Validation accuracy: {metrics['val_acc'] * 100:.2f}%")
    print(f"Precision: {metrics['precision']:.2f}")
    print(f"Recall:    {metrics['recall']:.2f}")
    print(f"F1 score:  {metrics['f1_score']:.2f}")

    with open(evaluation_folder / "metrics.json", "w") as f:
        json.dump(metrics, f)

    # Save training history plot
    fig = get_training_plot(model_history)
    fig.savefig(evaluation_folder / plots_folder / "training_history.png")

    # Save predictions preview plot
    fig = get_pred_preview_plot(model, ds_val, labels)
    fig.savefig(evaluation_folder / plots_folder / "pred_preview.png")

    # Save confusion matrix plot
    fig = get_confusion_matrix_plot(y_true, y_pred, labels)
    fig.savefig(evaluation_folder / plots_folder / "confusion_matrix.png")

    print(
        f"\nEvaluation metrics and plot files saved at {evaluation_folder.absolute()}"
    )


if __name__ == "__main__":
    main()
```

Check the differences with Git to better understand the changes:

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff src/evaluate.py
```

The output should be similar to this:

```diff
diff --git a/src/evaluate.py b/src/evaluate.py
index 5e62d83..0a006a1 100644
--- a/src/evaluate.py
+++ b/src/evaluate.py
@@ -12,6 +12,7 @@ from sklearn.metrics import (
     precision_score,
     recall_score,
 )
+import bentoml


 def get_training_plot(model_history: dict) -> plt.Figure:
@@ -102,9 +103,16 @@ def main() -> None:
     with open(prepared_dataset_folder / "labels.json") as f:
         labels = json.load(f)

+    # Import the model to the model store from a local model folder
+    try:
+        bentoml.models.import_model(
+            f"{model_folder.absolute()}/celestial_bodies_classifier_model.bentomodel"
+        )
+    except bentoml.exceptions.BentoMLException:
+        print("Model already exists in the model store - skipping import.")
+
     # Load model
-    model_path = model_folder.absolute() / "model.keras"
-    model = tf.keras.models.load_model(model_path)
+    model = bentoml.keras.load_model("celestial_bodies_classifier_model")
     model_history = np.load(
         model_folder.absolute() / "history.npy", allow_pickle=True
     ).item()
```

### Run the experiment

```sh title="Execute the following command(s) in a terminal"
# Run the experiment. DVC will automatically run all required stages
dvc repro
```

The experiment now uses BentoML to save and load the model. The resulting model
is saved in the `model` folder and is automatically tracked by DVC. The model is
then uploaded to the remote storage bucket when pushing the changes to DVC as
well.

You can check the models stored in the model store with the following command:

```sh title="Execute the following command(s) in a terminal"
# List the models in the model store
bentoml models list
```

The output should look like this:

```text
 Tag                                                 Module         Size      Creation Time
 celestial_bodies_classifier_model:rcmpuas76oxdcn36  bentoml.keras  9.43 MiB  2026-06-04 10:58:19
```

### Check the changes

Check the changes with Git to ensure that all the necessary files are tracked:

```sh title="Execute the following command(s) in a terminal"
# Add all the files
git add .

# Check the changes
git status
```

The output should look like this:

```text
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
    modified:   dvc.lock
    modified:   requirements-freeze.txt
    modified:   requirements.txt
    modified:   src/evaluate.py
    modified:   src/train.py
```

### Commit the changes to DVC and Git

Commit the changes to DVC and Git:

```sh title="Execute the following command(s) in a terminal"
# Upload the experiment data, model and cache to the remote bucket
dvc push

# Commit the changes
git commit -m "Use BentoML to save and load the model"

# Push the changes
git push
```

## Summary

In this chapter, you have successfully:

1. Installed BentoML
2. Learned about BentoML's model store
3. Updated and ran the experiment to use BentoML to save and load the model to
   and from the model's store

You fixed some of the previous issues:

- [x] Model can be saved and loaded with all required artifacts for future usage

!!! abstract "Take away"

    - **BentoML transforms models into production-ready artifacts**: By saving
      models with BentoML, you package not just the weights but also
      preprocessing/postprocessing logic and metadata, ensuring all dependencies
      travel together and eliminating the "it works in training but fails in serving"
      problem.
    - **Custom objects enable end-to-end inference pipelines**: BentoML's ability to
      save custom preprocessing and postprocessing functions alongside the model means
      your serving layer automatically handles image resizing, normalization, and
      output formatting without duplicating code.
    - **The model store centralizes model management**: BentoML's local model store
      at `~/bentoml/` acts as a versioned registry where models can be saved, loaded,
      and exported, providing a single source of truth for model artifacts before
      they're shared via DVC or deployed.
    - **Export/import enables collaboration and CI/CD**: Exporting BentoML models to
      `.bentomodel` files allows them to be tracked by DVC, shared with team members,
      and imported in CI/CD pipelines, bridging the gap between local development and
      automated deployment.

## State of the MLOps process

- [x] Model can be saved and loaded with all required artifacts for future usage
- [ ] Model cannot be easily used from outside of the experiment context
- [ ] Model requires manual publication to the artifact registry
- [ ] Model is not accessible on the Internet and cannot be used anywhere
- [ ] Model requires manual deployment on the cluster
- [ ] Model cannot be trained on hardware other than the local machine
- [ ] Model cannot be trained on custom hardware for specific use-cases

Continue to the next chapters to address the remaining items.

## Sources

Highly inspired by:

- [_Quickstart_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/get-started/quickstart.html)
- [_Keras_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/reference/frameworks/keras.html)
- [_Model Store_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/guides/model-store.html)
- [_Bento and model APIs_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/reference/stores.html)
- [_BentoML SDK_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/reference/sdk.html)
- [_BentoML CLI_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/reference/cli.html)
