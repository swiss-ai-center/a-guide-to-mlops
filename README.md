# Code

This branch contains the source code in order to prepare, train and evaluate a model from the dataset. The dataset can be found in the `data` branch.

## Installation

You can install the required packages with poetry:

```bash
poetry install
```

## Usage

The code is divided in 4 scripts:
- `python3 src/prepare.py <raw-dataset-folder> <prepared-dataset-folder>`: prepare the dataset for training
- `python3 src/train.py <prepared-dataset-folder> <model-folder>`: train the model
- `python3 src/evaluate.py <model-folder> <prepared-dataset-folder>`: evaluate the model
- `python3 src/explain.py <model-folder> <raw-dataset-folder>`: explain the model
