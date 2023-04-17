FROM python:3.11

# Add mkdocs dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    gcc \
    g++ \
    libcairo2 \
    libfreetype6 \
    libffi-dev \
    libjpeg-tools \
    libpng-dev \
    zlib1g

# Configure Poetry (see https://stackoverflow.com/questions/72465421/how-to-use-poetry-with-docker)
ENV POETRY_VERSION=1.4.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
ENV PYTHONUNBUFFERED=1
RUN python3 -m ensurepip
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Install Python dependencies
WORKDIR /workspaces/a-guide-to-mlops
COPY poetry.lock .
COPY pyproject.toml .

RUN poetry install
