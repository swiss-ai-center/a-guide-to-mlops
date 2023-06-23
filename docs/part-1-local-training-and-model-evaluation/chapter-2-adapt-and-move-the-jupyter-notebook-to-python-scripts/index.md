# Chapter 2: Adapt and move the Jupyter Notebook to Python scripts

??? info "You want to take over from this chapter? Collapse this section and follow the instructions below."

    !!! warning

        It might be easier to start from the previous chapter(s). Only follow this section if you are confortable with the content of the previous chapter(s).

    Get the required files for this chapter.

    ```sh title="Execute the following command(s) in a terminal"
    # Clone the repository
    git clone \
        --no-checkout \
        --depth=1 \
        --filter=tree:0 \
        https://github.com/csia-pme/a-guide-to-mlops.git

    # Move to the cloned repository
    cd a-guide-to-mlops

    # Get the files for this chapter
    git sparse-checkout set --no-cone docs/the-guide/chapter-1-run-a-simple-ml-experiment

    # Clone the files locally
    git checkout

    # Move back to the root directory
    cd ..

    # Copy the chapter files to the working directory
    cp -r a-guide-to-mlops/docs/the-guide/chapter-1-run-a-simple-ml-experiment/* .

    # Delete the cloned repository
    rm -rf a-guide-to-mlops
    ```

    Set up the environment.

    TODO FOR EACH CHAPTER

## Introduction

Jupyter Notebooks provide an interactive environment where code can be executed
and results can be visualized. They combine code, text explanations,
visualizations, and media in a single document, making it a flexible tool to
document a ML experiment.

However, they have severe limitations, such as challenges with reproducibility,
scalability, experiment tracking, and standardization. Integrating Jupyter
Notebooks into Python scripts suitable for running ML experiments in a more
modular and reproducible manner can help address these shortcomings and enhance
the overall ML development process.

[pip](https://pip.pypa.io/) is the standard package manager for Python. It is
used to install and manage dependencies in a Python environment.

Yet, pip is not an ideal tool to manage Python dependencies. It is not
user-friendly and it is not suitable for reproducibility and collaboration.

If you have a look at the `requirements.txt` file, you might notice the following issues:

- Which version of Python is required?
- Which version of the dependencies are required?
- Which dependencies are main dependencies and which are dependencies of dependencies?
- Where to install the dependencies (on my system, in a virtual environment)?
- How to ensure reproducibility?

This is why you will use [Poetry](https://python-poetry.org/) to manage Python dependencies.

Poetry is another tool to manage Python dependencies, but it is a more robust and
user-friendly alternative to pip. It is also more suitable for reproducibility
and collaboration by creating a lock file that can be used to recreate the *exact*
same environment on another machine.

For example, freezing the version of a dependency in a `requirements.txt` file is
not enough to ensure reproducibility. The `requirements.txt` file only specifies
the version of the dependency at the time of installation. If dependencies of the
dependency are updated, the version of the dependency might change without you
knowing it. This is why Poetry creates a lock file that contains the exact
version of all the dependencies and their dependencies.

In this chapter, you will learn how to:

1. Set up a standardized Python environment using [Poetry](https://python-poetry.org/)
2. Adapt the content of the Jupyter Notebook into Python scripts
3. Launch the experiment locally

The following diagram illustrates control flow of the experiment at the end of
this chapter:

```mermaid
flowchart
    subgraph localGraph[LOCAL]
        data[data/raw] --> prepare
        prepare[prepare.py] --> train
        train[train.py] --> evaluate
        evaluate[evaluate.py] --> explain
        explain[explain.py]
        params[params.yaml] -.- prepare
        params -.- train
    end
    style data opacity:0.4,color:#7f7f7f80
```

Let's get started!

## Steps

### Set up a new project directory

For the rest of the guide, you will work in a new directory. This will allow you to use the Jupyter Notebook directory as a reference.

Start by ensuring you have left the virtual environment created in the previous chapter.

```sh title="Execute the following command(s) in a terminal"
# Deactivate the virtual environment
deactivate
```

Next, exit from the current directory and create a new one.

```sh title="Execute the following command(s) in a terminal"
cd .. && mkdir a-guide-to-mlops && cd a-guide-to-mlops
```

### Set up the dataset

You will use the same dataset as in the previous chapter. Copy the `data` folder from the previous chapter to your new directory.

```sh title="Execute the following command(s) in a terminal"
# Copy the data folder from the previous chapter
cp -r ../a-guide-to-mlops-jupyter-notebook/data .
```

### Move from pip to Poetry

Initialize Poetry at the root of the directory.

```sh title="Execute the following command(s) in a terminal"
poetry init --no-interaction
```

This will create the `pyproject.toml` file that should look like this:

```toml title="pyproject.toml"
[tool.poetry]
name = "a-guide-to-mlops"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "a_guide_to_mlops"}]

[tool.poetry.dependencies]
python = ">=3.8,<3.12"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

Ensure to adjust the python version string manually from `^3.11` to `>=3.8,<3.12`.

TODO: This last step is needed to avoid a failure of dependency resolution
Check if this can be avboided or automated somehow.

Open a Poetry shell. This will automatically create and activate a virtual environment.

```sh title="Execute the following command(s) in a terminal"
# Open a Poetry shell in a new virtual environment
poetry shell
```

Install all the dependencies in the virtual environment.

```sh title="Execute the following command(s) in a terminal"
poetry add "matplotlib==3.7.1" "tensorflow==2.12.0" "pyyaml==6.0"
```

This will install the dependencies in the virtual environment and update the `pyproject.toml` file. You should have something like this:

```toml title="pyproject.toml"
[tool.poetry]
name = "a-guide-to-mlops"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]
readme = "README.md"
packages = [{include = "a_guide_to_mlops"}]

[tool.poetry.dependencies]
python = ">=3.8,<3.12"
matplotlib = "^3.7.1"
tensorflow = "^2.12.0"
pyyaml = "^6.0"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

A second `poetry.lock` file is also created. This file contains the exact version of all the dependencies and their dependencies.

```toml title="poetry.lock"
# This file is automatically @generated by Poetry 1.5.1 and should not be changed by hand.

[[package]]
name = "absl-py"
version = "1.4.0"
description = "Abseil Python Common Libraries, see https://github.com/abseil/abseil-py."
optional = false
python-versions = ">=3.6"
files = [
{file = "absl-py-1.4.0.tar.gz", hash = "sha256:d2c244d01048ba476e7c080bd2c6df5e141d211de80223460d5b3b8a2a58433d"},
{file = "absl_py-1.4.0-py3-none-any.whl", hash = "sha256:0d3fe606adfa4f7db64792dd4c7aee4ee0c38ab75dfd353b7a83ed3e957fcb47"},
]

[[package]]
name = "astunparse"
version = "1.6.3"
description = "An AST unparser for Python"
optional = false
python-versions = "*"
files = [
{file = "astunparse-1.6.3-py2.py3-none-any.whl", hash = "sha256:c2652417f2c8b5bb325c885ae329bdf3f86424075c4fd1a128674bc6fba4b8e8"},
{file = "astunparse-1.6.3.tar.gz", hash = "sha256:5ad93a8456f0d084c3456d059fd9a92cce667963232cbf763eac3bc5b7940872"},
]

[package.dependencies]
six = ">=1.6.1,<2.0"
wheel = ">=0.23.0,<1.0"

[[package]]
# ... and so on
```

Now that Poetry is set up, managing packages and virtual environments is easier:

* To access the virtual environment, simply type `poetry shell` to open a Poetry
shell in the virtual environment.

* To install dependencies, simply type `poetry add <dependency>` to
install a dependency in the virtual environment, which will also update the
`pyproject.toml` and `poetry.lock` files.

* To install all the dependencies listed in the `pyproject.toml` file when
accessing the virtual environment, you can also simply type `poetry install`.

* To exit the poetry shell once access to the virtual environment is no longer
needed, simply type `exit`.

Dependencies are clearly listed in the `pyproject.toml` file and the `poetry.lock`
file ensures reproducibility.

### Split the Jupyter Notebook into scripts

You will split the Jupyter Notebook in a codebase made of separate Python scripts with
well defined role. These scripts will be able to be called on the command line,
making it ideal for automation tasks.

The following table describes the files that you will create in this codebase.

| **File**                | **Description**                                   | **Input**                                       | **Output**                                                    |
| ----------------------- | ------------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------- |
| `params.yaml`           | The parameters to run the ML experiment           | -                                               | -                                                             |
| `src/prepare.py`        | Prepare the dataset to run the ML experiment      | The dataset to prepare in `data/raw` directory  | The prepared data in `data/prepared` directory                |
| `src/train.py`          | Train the ML model                                | The prepared dataset                            | The model trained with the dataset                            |
| `src/evaluate.py`       | Evaluate the ML model using scikit-learn          | The model to evaluate                           | The results of the model evaluation in `evaluation` directory |
| `src/explain.py`        | Explain the ML model                              | The model to explain                            | The results of the model explanation                          |
| `src/utils/seed.py`     | Util function to fix the seed                     | -                                               | -                                                             |

#### Move the parameters to its own file

Let's split the parameters to run the ML experiment with in a distinct file.

```yaml title="params.yaml"
prepare:
  seed: 77
  split: 0.2
  image_size: [32, 32]
  grayscale: True

train:
  seed: 77
  lr: 0.0001
  epochs: 5
  conv_size: 32
  dense_size: 64
  output_classes: 11
```

#### Move the preparation step to its own file

The `src/prepare.py` script will prepare the dataset.

```py title="src/prepare.py"
import json
import sys
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import tensorflow as tf
import yaml

from utils.seed import set_seed


def get_preview_plot(ds: tf.data.Dataset, labels: List[str]) -> plt.Figure:
    """Plot a preview of the prepared dataset"""
    fig = plt.figure(figsize=(10, 5), tight_layout=True)
    for images, label_idxs in ds.take(1):
        for i in range(10):
            plt.subplot(2, 5, i + 1)
            plt.imshow(images[i].numpy().astype("uint8"), cmap="gray")
            plt.title(labels[label_idxs[i].numpy()])
            plt.axis("off")

    return fig


def main() -> None:
    if len(sys.argv) != 3:
        print("Arguments error. Usage:\n")
        print("\tpython3 prepare.py <raw-dataset-folder> <prepared-dataset-folder>\n")
        exit(1)

    # Load parameters
    prepare_params = yaml.safe_load(open("params.yaml"))["prepare"]

    raw_dataset_folder = Path(sys.argv[1])
    prepared_dataset_folder = Path(sys.argv[2])
    seed = prepare_params["seed"]
    split = prepare_params["split"]
    image_size = prepare_params["image_size"]
    grayscale = prepare_params["grayscale"]

    # Set seed for reproducibility
    set_seed(seed)

    # Read data
    ds_train, ds_test = tf.keras.utils.image_dataset_from_directory(
        raw_dataset_folder,
        labels="inferred",
        label_mode="int",
        color_mode="grayscale" if grayscale else "rgb",
        batch_size=32,
        image_size=image_size,
        shuffle=True,
        seed=seed,
        validation_split=split,
        subset="both",
    )
    labels = ds_train.class_names

    if not prepared_dataset_folder.exists():
        prepared_dataset_folder.mkdir(parents=True)

    # Save the preview plot
    preview_plot = get_preview_plot(ds_train, labels)
    preview_plot.savefig(prepared_dataset_folder / "preview.png")

    # Save the prepared dataset
    with open(prepared_dataset_folder / "labels.json", "w") as f:
        json.dump(labels, f)
    tf.data.Dataset.save(ds_train, str(prepared_dataset_folder / "train"))
    tf.data.Dataset.save(ds_test, str(prepared_dataset_folder / "test"))

    print(f"\nDataset saved at {prepared_dataset_folder.absolute()}")


if __name__ == "__main__":
    main()
```

#### Move the train step to its own file

The `src/train.py` script will train the ML model.

```py title="src/train.py"
import sys
from pathlib import Path
from typing import Tuple

import numpy as np
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
    model.save(str(model_folder))
    # Save the model history
    np.save(model_folder / "history.npy", model.history.history)

    print(f"\nModel saved at {model_folder.absolute()}")


if __name__ == "__main__":
    main()
```

#### Move the evaluate step to its own file

The `src/evaluate.py` script will evaluate the ML model using DVC.

```py title="src/evaluate.py"
import json
import sys
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


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
            img = images[i].numpy().astype("uint8")
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

    conf_matrix = conf_matrix / tf.reduce_sum(conf_matrix, axis=1)
    plt.imshow(conf_matrix)
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
    model = tf.keras.models.load_model(model_folder)
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

#### Move the explain step to its own file

The `src/explain.py` script will explain the ML model using GRAD-CAM.

```py title="src/explain.py"
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf


def make_gradcam_heatmap(img: np.ndarray, grad_model: tf.keras.Model) -> np.ndarray:
    """
    Generate Grad-CAM heatmap from image

    Learn more about Grad-CAM here: https://keras.io/examples/vision/grad_cam/
    """
    # Resize and convert the image
    img = np.expand_dims(img, axis=0)
    input_w = grad_model.input_shape[1]
    input_h = grad_model.input_shape[2]
    img = tf.image.resize(img, (input_w, input_h))
    grayscale = grad_model.input_shape[3] == 1
    if grayscale:
        img = tf.image.rgb_to_grayscale(img)

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img)
        pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)

    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()


def get_gradcam_plot(model: tf.keras.Model, data_folder: Path) -> plt.Figure:
    """Plot the Grad-CAM heatmap"""
    last_conv_layer = list(filter(lambda x: "conv" in x.name, model.layers))[-1]
    grad_model = tf.keras.models.Model(
        model.inputs, [last_conv_layer.output, model.output]
    )

    classes = sorted(filter(lambda p: p.is_dir(), data_folder.glob("*")))

    fig = plt.figure(figsize=(11, 16), tight_layout=True)
    for i, class_path in enumerate(classes):
        img_path = list(sorted(class_path.glob("*")))[0]
        img_fn = img_path.name
        img = tf.keras.preprocessing.image.load_img(img_path)
        img = tf.keras.preprocessing.image.img_to_array(img)

        heatmap = make_gradcam_heatmap(img, grad_model)
        heatmap = np.uint8(255 * heatmap)

        # Create an image with RGB colorized heatmap
        jet = plt.get_cmap("jet")
        jet_colors = jet(np.arange(256))[:, :3]
        jet_heatmap = jet_colors[heatmap]

        jet_heatmap = tf.keras.utils.array_to_img(jet_heatmap)
        jet_heatmap = jet_heatmap.resize((img.shape[1], img.shape[0]))
        jet_heatmap = tf.keras.utils.img_to_array(jet_heatmap)

        plt.subplot(6, 4, i * 2 + 1)
        plt.imshow(img / 255)
        plt.axis("off")
        plt.title(img_fn)

        plt.subplot(6, 4, i * 2 + 2)
        plt.imshow(jet_heatmap / 255)
        plt.axis("off")
        plt.title(img_fn + " (Grad-CAM)")

    return fig


def main() -> None:
    if len(sys.argv) != 3:
        print("Arguments error. Usage:\n")
        print("\tpython3 evaluate.py <model-folder> <raw-dataset-folder>\n")
        exit(1)

    model_folder = Path(sys.argv[1])
    raw_dataset_folder = Path(sys.argv[2])
    evaluation_folder = Path("evaluation")
    plots_folder = Path("plots")

    # Load model
    model = tf.keras.models.load_model(model_folder)

    # Create folders
    (evaluation_folder / plots_folder).mkdir(parents=True, exist_ok=True)

    # Save Grad-CAM plot
    fig = get_gradcam_plot(model, raw_dataset_folder)
    fig.savefig(evaluation_folder / plots_folder / "grad_cam.png")

    print(f"\nExplain files saved at {evaluation_folder.absolute()}")


if __name__ == "__main__":
    main()
```

#### Create the seed helper function

Finally, add the small `src/utils/seed.py` script to handle the fixing of the
seed parameters. This ensure the results are reproducible.

```py title="src/utils/seed.py"
import os
import random

import numpy as np
import tensorflow as tf


def set_seed(seed: int) -> None:
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    np.random.seed(seed)

    os.environ["TF_DETERMINISTIC_OPS"] = "1"
    os.environ["TF_CUDNN_DETERMINISTIC"] = "1"

    tf.random.set_seed(seed)
    tf.config.threading.set_inter_op_parallelism_threads(1)
    tf.config.threading.set_intra_op_parallelism_threads(1)
```

### Make usage of the scripts in the Jupyter Notebook

TODO: Update the notebook to use the scripts and the parameters file as well in a hybrid approach: Notebook to visualize the data and results and scripts to run the experiment.

### Check the results

Your working directory should now look like this:

```yaml hl_lines="5-8 9-11"
.
├── data
│   ├── raw
│   │   └── ...
│   └── README.md
├── src # (1)!
│   ├── evaluate.py
│   ├── explain.py
│   ├── prepare.py
│   ├── train.py
│   └── utils
│       └── seed.py
├── params.yaml # (2)!
├── poetry.lock # (3)!
└── pyproject.toml # (4)!
```

1. This, and all its sub-directory, is new.
2. This is new.
3. This is new.
4. This is new.

### Run the experiment

Awesome! You now have everything you need to run the experiment: the codebase and
the dataset are in place, the new virtual environment is set up, and you are ready to run the experiment for the first
time.

You can now follow these steps to reproduce the experiment.

```sh title="Execute the following command(s) in a terminal"
# Prepare the dataset
python3 src/prepare.py data/raw data/prepared

# Train the model with the train dataset and save it
python3 src/train.py data/prepared model

# Evaluate the model performances
python3 src/evaluate.py model data/prepared

# Explain the model
python3 src/explain.py model data/raw
```

### Check the results

Your working directory should now be similar to this:

```yaml hl_lines="3-8 11-16 21"
.
├── data
│   ├── prepared # (1)!
│   │   └── ...
│   ├── raw
│   │   └── ...
│   └── README.md
├── evaluation # (2)!
│   ├── plots
│   │   ├── confusion_matrix.png
│   │   ├── pred_preview.png
│   │   ├── grad_cam.png
│   │   └── training_history.png
│   └── metrics.json
├── src
│   ├── evaluate.py
│   ├── explain.py
│   ├── prepare.py
│   ├── train.py
│   └── utils
│       └── seed.py
├── model # (4)!
│   └── ...
├── params.yaml
├── poetry.lock
└── pyproject.toml
```

1. This, and all its sub-directory, is new.
2. This, and all its sub-directory, is new.
3. This is new.
4. This is new.

Here, the following should be noted:

- the `prepare.py` script created the `data/prepared` directory and divided the
dataset into a training set and a test set
- the `train.py` script created the `model` directory and trained the model with
the prepared data.
- the `evaluate.py` script created the `evaluation` directory and generated some
plots and metrics to evaluate the model
- the `explain.py` script generated a GRAD-CAM heatmap to explain the model

Take some time to get familiar with the scripts and the results.

## Summary

Congratulations! You have successfully reproduced the experiment on your machine,
this time using a modular approach that can be put into production.

In this chapter, you have:

1. Set up a standardized Python environment using Poetry
2. Adapted the content of the Jupyter Notebook into Python scripts
3. Launched the experiment locally

However, you may have identified the following areas for improvement:

- ❌ Codebase is not versioned
- ❌ Dataset still needs manual download and placement
- ❌ Steps to run the experiment were not documented
- ❌ Codebase is not easily sharable
- ❌ Dataset is not easily sharable

In the next chapters, you will enhance the workflow to fix those issues.

You can now safely continue to the next chapter.

## State of the MLOps process

- ✅ Notebook has been transformed into scripts for production
- ❌ Codebase and dataset are not versioned
- ❌ Model steps rely on verbal communication and may be undocumented
- ❌ Changes to model are not easily visualized
- ❌ Dataset requires manual download and placement
- ❌ Codebase requires manual download and setup
- ❌ Experiment may not be reproducible on other machines
- ❌ Changes to model are not thoroughly reviewed and discussed before integration
- ❌ Model may have required artifacts that are forgotten or omitted in saved/loaded state
- ❌ Model cannot be easily used from outside of the experiment context

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by:

* the [_Get Started: Data Pipelines_ -
dvc.org](https://dvc.org/doc/start/data-management/data-pipelines) guide.
* [_How to get stable results with TensorFlow, setting random seed_ -
stackoverflow.com](https://stackoverflow.com/questions/36288235/how-to-get-stable-results-with-tensorflow-setting-random-seed)
