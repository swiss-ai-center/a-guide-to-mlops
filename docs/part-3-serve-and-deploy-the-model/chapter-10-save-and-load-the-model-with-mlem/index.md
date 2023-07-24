# Chapter 10: Save and load the model with MLEM

??? info "You want to take over from this chapter? Collapse this section and follow the instructions below."

    _Work in progress._

    [//]: # "TODO"

## Introduction

The purpose of this chapter is to serve and use the model for usage outside of
the experiment context with the help of [MLEM](../../tools), a powerful tool
designed for easy packaging, deployment, and serving of Machine Learning models.

By transforming your model into a specialized MLEM model, it is possible to
capture the essential metadata information that can then be used to load the
model for future usage, unlocking true potential in facilitating seamless and
efficient model deployment.

In this chapter, you will learn how to:

1. Install MLEM
2. Initialize and configure MLEM
3. Update and run the experiment to use MLEM to save and load the model

## Steps

### Install MLEM

Add the `mlem` package to install MLEM support.

```txt title="requirements.txt" hl_lines="5"
tensorflow==2.12.0
matplotlib==3.7.1
pyyaml==6.0
dvc[gs]==3.2.2
mlem==0.4.13
```

Install the package and update the freeze file.

```sh title="Execute the following command(s) in a terminal"
# Install the requirements
pip install --requirement requirements.txt

# Freeze the requirements
pip freeze --local --all > requirements-freeze.txt
```

Check the differences with Git to validate the changes.

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff requirements.txt
```

The output should be similar to this.

```diff
diff --git a/requirements.txt b/requirements.txt
index 8ccc2df..fcdd460 100644
--- a/requirements.txt
+++ b/requirements.txt
@@ -2,3 +2,4 @@ tensorflow==2.12.0
 matplotlib==3.7.1
 pyyaml==6.0
 dvc[gs]==3.2.2
+mlem==0.4.13
```

### Initialize and configure MLEM.

```sh title="Execute the following command(s) in a terminal"
# Initialize MLEM
mlem init

# Set MLEM to use DVC
mlem config set core.storage.type dvc

# Add MLEM metafiles to dvcignore
echo "/**/?*.mlem" >> .dvcignore
```

The effect of the `mlem init` command is to create a `.mlem.yaml` file in the
working directory. This file contains the configuration of MLEM.

### Update the experiment

To make the most of MLEM's capabilities, you must start by converting your model
into the specialized MLEM format, which allows for the capture of essential
model metadata beyond traditional model-saving practices. This pivotal step is
crucial for harnessing the comprehensive features and advantages offered by
MLEM.

#### Update `src/train.py`

Update the `src/train.py` file to save the model with MLEM.

!!! info

    MLEM can save model artifacts as well such as TFIDF vectorizer, etc.

    When loading a model using MLEM, it will automatically load the artifacts if
    they are present, so you don't have to worry about it.

    This is not covered in this guide as the model does not use any artifacts but
    can be really useful in some cases.

```py title="src/train.py" hl_lines="1 9 66-68 89-125"
import json
import sys
from pathlib import Path
from typing import Tuple

import numpy as np
import tensorflow as tf
import yaml
from mlem.api import save

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
            tf.keras.layers.Conv2D(
                conv_size, (3, 3), activation="relu", input_shape=image_shape
            ),
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
    prepare_params = yaml.safe_load(open("params.yaml"))["prepare"]
    train_params = yaml.safe_load(open("params.yaml"))["train"]

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
    ds_test = tf.data.Dataset.load(str(prepared_dataset_folder / "test"))

    labels = None
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
        validation_data=ds_test,
    )

    # Save the model
    model_folder.mkdir(parents=True, exist_ok=True)

    def preprocess(x):
        # convert bytes to tensor
        x = tf.io.decode_image(x, channels=1 if grayscale else 3)
        x = tf.image.resize(x, image_size)
        x = tf.cast(x, tf.float32)
        x = x / 255.0
        # add batch dimension
        x = tf.expand_dims(x, axis=0)
        return x

    def postprocess(x):
        return {
            "probabilities": {
                labels[i]: prob
                for i, prob in enumerate(tf.nn.softmax(x).numpy()[0].tolist())
            },
            "prediction": labels[tf.argmax(x, axis=-1).numpy()[0]],
        }

    def get_sample_data():
        x = np.ones((128, 128, 3), dtype=np.uint8)
        x *= 255
        # convert array to png bytes
        x = tf.io.encode_png(x)
        # tensor to bytes
        x = x.numpy()
        return x

    save(
        model,
        str(model_folder),
        preprocess=preprocess,
        # Convert output to probabilities
        postprocess=postprocess,
        # encode array to png bytes
        sample_data=get_sample_data(),
    )

    # Save the model history
    np.save(model_folder / "history.npy", model.history.history)

    print(f"\nModel saved at {model_folder.absolute()}")


if __name__ == "__main__":
    main()
```

MLEM can save the model with a `preprocessing`, `postprocessing` and
`sample_data` functions.

These functions are used to save the model with the necessary information to
load it later.

- `preprocess` is used to preprocess the input data before feeding it to the
  model.
- `postprocess` is used to postprocess the output of the model.
- `sample_data` is used to save a sample of data that can be used to test the
  model after loading it.

These functions will be used later to generate the API documentation and to test
the model through the REST API.

Check the differences with Git to better understand the changes.

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff src/train.py
```

The output should be similar to this.

```diff
diff --git a/src/train.py b/src/train.py
index ab7724a..fe35a9b 100644
--- a/src/train.py
+++ b/src/train.py
@@ -1,3 +1,4 @@
+import json
 import sys
 from pathlib import Path
 from typing import Tuple
@@ -5,6 +6,7 @@ from typing import Tuple
 import numpy as np
 import tensorflow as tf
 import yaml
+from mlem.api import save

 from utils.seed import set_seed

@@ -61,6 +63,10 @@ def main() -> None:
     ds_train = tf.data.Dataset.load(str(prepared_dataset_folder / "train"))
     ds_test = tf.data.Dataset.load(str(prepared_dataset_folder / "test"))

+    labels = None
+    with open(prepared_dataset_folder / "labels.json") as f:
+        labels = json.load(f)
+
     # Define the model
     model = get_model(image_shape, conv_size, dense_size, output_classes)
     model.compile(
@@ -79,7 +85,45 @@ def main() -> None:

     # Save the model
     model_folder.mkdir(parents=True, exist_ok=True)
-    model.save(str(model_folder))
+
+    def preprocess(x):
+        # convert bytes to tensor
+        x = tf.io.decode_image(x, channels=1 if grayscale else 3)
+        x = tf.image.resize(x, image_size)
+        x = tf.cast(x, tf.float32)
+        x = x / 255.0
+        # add batch dimension
+        x = tf.expand_dims(x, axis=0)
+        return x
+
+    def postprocess(x):
+        return {
+            "probabilities": {
+                labels[i]: prob
+                for i, prob in enumerate(tf.nn.softmax(x).numpy()[0].tolist())
+            },
+            "prediction": labels[tf.argmax(x, axis=-1).numpy()[0]],
+        }
+
+    def get_sample_data():
+        x = np.ones((128, 128, 3), dtype=np.uint8)
+        x *= 255
+        # convert array to png bytes
+        x = tf.io.encode_png(x)
+        # tensor to bytes
+        x = x.numpy()
+        return x
+
+    save(
+        model,
+        str(model_folder),
+        preprocess=preprocess,
+        # Convert output to probabilities
+        postprocess=postprocess,
+        # encode array to png bytes
+        sample_data=get_sample_data(),
+    )
+
     # Save the model history
     np.save(model_folder / "history.npy", model.history.history)
```

#### Update `src/evaluate.py`

Update the `src/evaluate.py` file to load the model from MLEM.

```py title="src/evaluate.py" hl_lines="9 133"
import json
import sys
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from mlem.api import load


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
    model: tf.keras.Model, ds_test: tf.data.Dataset, labels: List[str]
) -> plt.Figure:
    """Plot a preview of the predictions"""
    fig = plt.figure(figsize=(10, 5), tight_layout=True)
    for images, label_idxs in ds_test.take(1):
        preds = model.predict(images)
        for i in range(10):
            plt.subplot(2, 5, i + 1)
            img = (images[i].numpy() * 255).astype("uint8")
            # Convert image to rgb if grayscale
            if img.shape[-1] == 1:
                img = np.squeeze(img, axis=-1)
                img = np.stack((img,) * 3, axis=-1)
            true_label = labels[label_idxs[i].numpy()]
            pred_label = labels[np.argmax(preds[i])]
            # Add red border if the prediction is wrong else add green border
            img = np.pad(img, pad_width=((1, 1), (1, 1), (0, 0)))
            if true_label != pred_label:
                img[0, :, 0] = 255  # Top border
                img[-1, :, 0] = 255  # Bottom border
                img[:, 0, 0] = 255  # Left border
                img[:, -1, 0] = 255  # Right border
            else:
                img[0, :, 1] = 255
                img[-1, :, 1] = 255
                img[:, 0, 1] = 255
                img[:, -1, 1] = 255

            plt.imshow(img)
            plt.title(f"True: {true_label}\n" f"Pred: {pred_label}")
            plt.axis("off")

    return fig


def get_confusion_matrix_plot(
    model: tf.keras.Model, ds_test: tf.data.Dataset, labels: List[str]
) -> plt.Figure:
    """Plot the confusion matrix"""
    fig = plt.figure(figsize=(6, 6), tight_layout=True)
    preds = model.predict(ds_test)

    conf_matrix = tf.math.confusion_matrix(
        labels=tf.concat([y for _, y in ds_test], axis=0),
        predictions=tf.argmax(preds, axis=1),
        num_classes=len(labels),
    )

    # Plot the confusion matrix
    conf_matrix = conf_matrix / tf.reduce_sum(conf_matrix, axis=1)
    plt.imshow(conf_matrix, cmap="Blues")

    # Plot cell values
    for i in range(len(labels)):
        for j in range(len(labels)):
            value = conf_matrix[i, j].numpy()
            if value == 0:
                color = "lightgray"
            elif value > 0.5:
                color = "white"
            else:
                color = "black"
            plt.text(
                j,
                i,
                f"{value:.2f}",
                ha="center",
                va="center",
                color=color,
                fontsize=8,
            )

    plt.colorbar()
    plt.xticks(range(len(labels)), labels, rotation=90)
    plt.yticks(range(len(labels)), labels)
    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.title("Confusion matrix")

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
    ds_test = tf.data.Dataset.load(str(prepared_dataset_folder / "test"))
    labels = None
    with open(prepared_dataset_folder / "labels.json") as f:
        labels = json.load(f)

    # Load model
    model = load(model_folder)
    model_history = np.load(model_folder / "history.npy", allow_pickle=True).item()

    # Log metrics
    val_loss, val_acc = model.evaluate(ds_test)
    print(f"Validation loss: {val_loss:.2f}")
    print(f"Validation accuracy: {val_acc * 100:.2f}%")
    with open(evaluation_folder / "metrics.json", "w") as f:
        json.dump({"val_loss": val_loss, "val_acc": val_acc}, f)

    # Save training history plot
    fig = get_training_plot(model_history)
    fig.savefig(evaluation_folder / plots_folder / "training_history.png")

    # Save predictions preview plot
    fig = get_pred_preview_plot(model, ds_test, labels)
    fig.savefig(evaluation_folder / plots_folder / "pred_preview.png")

    # Save confusion matrix plot
    fig = get_confusion_matrix_plot(model, ds_test, labels)
    fig.savefig(evaluation_folder / plots_folder / "confusion_matrix.png")

    print(
        f"\nEvaluation metrics and plot files saved at {evaluation_folder.absolute()}"
    )


if __name__ == "__main__":
    main()
```

Check the differences with Git to better understand the changes.

```sh title="Execute the following command(s) in a terminal"
# Show the differences with Git
git diff src/evaluate.py
```

The output should be similar to this.

```diff
diff --git a/src/evaluate.py b/src/evaluate.py
index aa36089..cc9b5a5 100644
--- a/src/evaluate.py
+++ b/src/evaluate.py
@@ -6,6 +6,7 @@ from typing import List
 import matplotlib.pyplot as plt
 import numpy as np
 import tensorflow as tf
+from mlem.api import load


 def get_training_plot(model_history: dict) -> plt.Figure:
@@ -107,7 +108,7 @@ def main() -> None:
         labels = json.load(f)

     # Load model
-    model = tf.keras.models.load_model(model_folder)
+    model = load(model_folder)
     model_history = np.load(model_folder / "history.npy", allow_pickle=True).item()

     # Log metrics
```

!!! info

    When a MLEM model is loaded with `mlem.api.load`, loads the model as it was
    saved without the preprocessing and postprocessing functions.

### Run the experiment

```sh title="Execute the following command(s) in a terminal"
# Run the experiment. DVC will automatically run all required stages
dvc repro
```

The experiment now uses MLEM to save and load the model. DVC stores the model
and its metadata.

### Check the changes

Check the changes with Git to ensure that all the necessary files are tracked.

```sh title="Execute the following command(s) in a terminal"
# Add all the files
git add .

# Check the changes
git status
```

The output should look like this.

```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
    modified:   .dvcignore
    new file:   .mlem.yaml
    modified:   dvc.lock
    new file:   model.mlem
    modified:   requirements-freeze.txt
    modified:   requirements.txt
    modified:   src/evaluate.py
    modified:   src/train.py
```

### Commit the changes to DVC and Git

Commit the changes to DVC and Git.

```sh title="Execute the following command(s) in a terminal"
# Upload the experiment data and cache to the remote bucket
dvc push

# Commit the changes
git commit -m "MLEM can save and load the model"

# Push the changes
git push
```

## Summary

In this chapter, you have successfully:

1. Installed MLEM
2. Initialized and configuring MLEM
3. Updated and ran the experiment to use MLEM to save and load the model

You did fix some of the previous issues:

- [x] Model can be saved and loaded with all required artifacts for future usage

You can now safely continue to the next chapter.

## State of the MLOps process

- [x] Notebook has been transformed into scripts for production
- [x] Codebase and dataset are versioned
- [x] Steps used to create the model are documented and can be re-executed
- [x] Changes done to a model can be visualized with parameters, metrics and
      plots to identify differences between iterations
- [x] Dataset can be shared among the developers and is placed in the right
      directory in order to run the experiment
- [x] Codebase can be shared and improved by multiple developers
- [x] Experiment can be executed on a clean machine with the help of a CI/CD
      pipeline
- [x] Changes to model can be thoroughly reviewed and discussed before
      integrating them into the codebase
- [x] Model can be saved and loaded with all required artifacts for future usage
- [ ] Model cannot be easily used from outside of the experiment context
- [ ] Model is not accessible on the Internet and cannot be used anywhere
- [ ] Model cannot be trained on hardware other than the local machine

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by:

* [_Get Started_ - mlem.ai](https://mlem.ai/doc/get-started)
* [_Saving models_ - mlem.ai](https://mlem.ai/doc/get-started/saving)
* [_Working with Data_ - mlem.ai](https://mlem.ai/doc/user-guide/data)
* [_`mlem.api.save()`_ - mlem.ai](https://mlem.ai/doc/api-reference/save)
* [_`mlem.api.load()`_ - mlem.ai](https://mlem.ai/doc/api-reference/load)
