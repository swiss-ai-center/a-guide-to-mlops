import json
import random
import sys
from pathlib import Path
from typing import Optional, Set

import numpy as np
import pandas as pd
import yaml
from sklearn.model_selection import train_test_split


def normalize_data(df: pd.DataFrame, columns: Set[str]) -> pd.DataFrame:
    """Normalize the data in the given columns to the range [0, 1]"""

    normalized_df = df.copy()
    for feature in columns:
        normalized_df[feature] = (df[feature] - df[feature].min()) / (
            df[feature].max() - df[feature].min()
        )
    return normalized_df


def shuffle_data(df: pd.DataFrame, seed: Optional[int] = None) -> pd.DataFrame:
    """Shuffle the data"""
    return df.sample(frac=1, random_state=seed).reset_index(drop=True)


def save_labels(df: pd.DataFrame, path: Path) -> None:
    """Save the dataframe columns to the given path"""

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(json.dumps(df.columns.tolist()))


def main() -> None:
    if len(sys.argv) != 3:
        print("Arguments error. Usage:\n")
        print("\tpython3 prepare.py <dataset-path> <prepared-dataset-folder>\n")
        exit(1)

    # Load parameters
    params = yaml.safe_load(open("params.yaml"))["prepare"]

    input_dataset_path = Path(sys.argv[1])
    prepared_dataset_folder = Path(sys.argv[2])
    seed = params["seed"]
    split = params["split"]

    # Set seed for reproducibility
    random.seed(seed)
    np.random.seed(seed)

    # Read data
    print("Preparing dataset...")
    df = pd.read_csv(input_dataset_path)
    df = normalize_data(df, columns=set(df.columns) - set(["Habitability"]))
    df = shuffle_data(df, seed=seed)

    # Split the dataset into features and labels
    X = df.drop(["Habitability"], axis=1).values
    y = df["Habitability"].values

    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=split, random_state=seed
    )

    print(f"Train set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")

    # Save the prepared dataset
    save_labels(df, prepared_dataset_folder / "labels.json")
    np.save(prepared_dataset_folder / "X_train.npy", X_train)
    np.save(prepared_dataset_folder / "X_test.npy", X_test)
    np.save(prepared_dataset_folder / "y_train.npy", y_train)
    np.save(prepared_dataset_folder / "y_test.npy", y_test)

    print(f"\nDataset saved at {prepared_dataset_folder.absolute()}")


if __name__ == "__main__":
    main()
