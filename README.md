# Jupyter Notebook

This branch is only intended to keep a backup of the Jupyter Notebook used in the guide. It is only intended to simulate the traditional approach to store and share code among the team.

The Jupyter Notebook prepares, trains and evaluates a model from the dataset.

## Note

The Jupyter Notebook has been purposely left with an exception at the start. This is to represent the fact that the notebook is not intended to be run as a script and shared on a repository. It is only intended to be used as a guide to prepare the code and then move it to a Python script.

## Usage

### With standard Python tools

Create a virtual environment, install the dependencies and run the Jupyter
Notebook with the following commands:

```bash
# Create the virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the Python dependencies
pip install -r requirements.txt

# Run the Jupyter Notebook
jupyter-lab notebook.ipynb
```

### With uv

If you prefer to use [uv](https://docs.astral.sh/uv/) instead of the standard
Python tools, run the following commands:

```bash
# Create the virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install the Python dependencies
uv pip install -r requirements.txt

# Run the Jupyter Notebook
jupyter-lab notebook.ipynb
```

## Update dependencies

In case the dependencies need to be updated, create a new virtual environment,
install the base dependencies and generate the versioned package list.

### With standard Python tools

```bash
# Create the virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the base dependencies
pip install jupyterlab tensorflow matplotlib pyyaml

# Generate the versioned package list
pip freeze --local --all > requirements.txt
```

### With uv

If you prefer to use [uv](https://docs.astral.sh/uv/) instead of the standard
Python tools, run the following commands:

```bash
# Create the virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate

# Install the base dependencies
uv pip install jupyterlab tensorflow matplotlib pyyaml

# Generate the versioned package list
uv pip freeze > requirements.txt
```

## References

- Grad Cam with Keras: https://keras.io/examples/vision/grad_cam/