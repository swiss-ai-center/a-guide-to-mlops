# Jupyter Notebook

This branch is only intended to keep a backup of the Jupyter Notebook used in the guide. It is only intended to simulate the traditional approach to store and share code among the team.

The Jupyter Notebook prepares, trains and evaluates a model from the dataset.

## Note

The Jupyter Notebook has been purposely left with an exception at the start. This is to represent the fact that the notebook is not intended to be run as a script and shared on a repository. It is only intended to be used as a guide to prepare the code and then move it to a Python script.

## Usage

1. Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Run the Jupyter Notebook:

```bash
jupyter-lab notebook.ipynb
```

## Update dependencies

In case the dependencies need to be updated:

* create a new virtual environment
* install the base dependencies
* generate the versioned package list

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install jupyterlab tensorflow matplotlib pyyaml
pip freeze --local --all > requirements.txt
```

## References

- Grad Cam with Keras: https://keras.io/examples/vision/grad_cam/