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
