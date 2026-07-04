# Notebook

This branch backs up the Jupyter Notebook used in the guide. It simulates the traditional approach of storing and sharing code directly in a notebook.

> The notebook is intentionally left with an exception at the start: it is not meant to be run as a script or shared as production code, but as a stepping stone toward a proper Python script.

## Usage

### With pip

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-freeze.txt
jupyter-lab notebook.ipynb
```

### With uv

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements-freeze.txt
jupyter-lab notebook.ipynb
```

## Update dependencies

To refresh the pinned dependencies, install the base requirements and regenerate the lock file.

### With pip

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip freeze --local --all > requirements-freeze.txt
```

### With uv

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv pip freeze > requirements-freeze.txt
```
