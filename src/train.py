import pickle
import random
import sys
from pathlib import Path

import numpy as np
import yaml
from sklearn.ensemble import RandomForestClassifier


def main() -> None:
    if len(sys.argv) != 3:
        print("Arguments error. Usage:\n")
        print("\tpython train.py prepared-dataset-folder model-path\n")
        exit(1)

    # Load parameters
    params = yaml.safe_load(open("params.yaml"))["train"]

    prepared_dataset_folder = Path(sys.argv[1])
    model_path = Path(sys.argv[2])
    seed = params["seed"]
    n_est = params["n_est"]
    max_depth = params["max_depth"]
    min_split = params["min_split"]

    # Set seed for reproducibility
    random.seed(seed)
    np.random.seed(seed)

    # Load data
    X_train = np.load(prepared_dataset_folder / "X_train.npy")
    y_train = np.load(prepared_dataset_folder / "y_train.npy")

    # Train the model
    print("Training model...")
    clf = RandomForestClassifier(
        n_estimators=n_est,
        max_depth=max_depth,
        min_samples_split=min_split,
        random_state=seed,
    )
    clf.fit(X_train, y_train)

    # Save the model
    model_path.parent.mkdir(parents=True, exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(clf, f)

    print(f"Model saved at {model_path.absolute()}")


if __name__ == "__main__":
    main()
