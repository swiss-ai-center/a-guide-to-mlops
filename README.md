# A guide to MLOps

A simple yet complete guide to MLOps tools and practices - from a conventional
way to a modern approach of working with ML projects. Website available at
<https://mlops.swiss-ai-center.ch>.

## Overview

The repository is organized into several branches, each fulfilling a specific
role:

* `main`: the guide that is continuously deployed
* `dataset`: the dataset generator used to create the dataset for the experiment
* `data`: the dataset used to train and evaluate the model
* `extra-data`: the supplementary dataset used for inference and labeling before
  retraining the model
* `freeze`: a backup of the validated dependencies list which can be used as a
  fallback in case of breakage in the transitive dependencies tree.

Temporary branches may also exist for ongoing issues and improvements to the
guide.

## Development

### Local development with Python

To improve the documentation locally, run [Zensical](https://zensical.org/) with
the following commands:

#### With standard Python tools

```sh
# Create the virtual environment
python3.13 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the Python dependencies
pip install --requirement requirements-freeze.txt

# Run Zensical
zensical serve
```

You can now access the local development server at <http://localhost:8000>.

If you make changes to the documentation, the web page should reload.

#### With uv

If you prefer to use [uv](https://docs.astral.sh/uv/) instead of the standard
Python tools, run the following commands:

```sh
# Create the virtual environment
uv venv --python 3.13

# Activate the virtual environment
source .venv/bin/activate

# Install the Python dependencies
uv pip install --requirement requirements-freeze.txt

# Run Zensical
zensical serve
```

You can now access the local development server at <http://localhost:8000>.

If you make changes to the documentation, the web page should reload.

#### With Docker Compose

If you prefer to use [Docker Compose](https://docs.docker.com/compose/) instead
of the standard Python tools, run the following commands:

```sh
# Build the Docker container
docker compose build

# Start the Docker container
docker compose up serve
```

You can now access the local development server at <http://localhost:8000>.

If you make changes to the documentation, the web page should reload.

### Format the documentation

To format the Markdown documentation, run
[mdwrap](https://github.com/swiss-ai-center/mdwrap) with the following commands:

#### With standard Python tools

```sh
# Create the virtual environment
python3.13 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the Python dependencies
pip install --requirement requirements-freeze.txt

# Run mdwrap
mdwrap --fmt docs
```

#### With uv

If you prefer to use [uv](https://docs.astral.sh/uv/) instead of the standard
Python tools, run the following commands:

```sh
# Create the virtual environment
uv venv --python 3.13

# Activate the virtual environment
source .venv/bin/activate

# Install the Python dependencies
uv pip install --requirement requirements-freeze.txt

# Run mdwrap
mdwrap --fmt docs
```

#### With Docker Compose

If you prefer to use [Docker Compose](https://docs.docker.com/compose/) instead
of the standard Python tools, run the following commands:

```sh
# Build the Docker container
docker compose build

# Start the Docker container
docker compose up format
```
