# Code

This branch contains the source code in order to prepare, train and evaluate a model from the dataset. The dataset can be found in the `data` branch.

## Installation

You can install the required packages with poetry:

```bash
poetry install
```

## Usage

The code is divided in 3 scripts:
- `python3 prepare.py <dataset-path> <prepared-dataset-folder>`: prepare the dataset for training
- `python3 train.py <prepared-dataset-folder> <model-folder>`: train the model
- `python3 evaluate.py <model-folder> <prepared-dataset-folder>`: evaluate the model