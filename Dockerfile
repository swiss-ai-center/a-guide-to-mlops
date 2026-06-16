# Base image
FROM python:3.13

# Working directory
WORKDIR /workspaces/a-guide-to-mlops

# Copy the dependencies
COPY requirements.txt .
COPY requirements-freeze.txt .

# Install Python dependencies
RUN pip install \
    --requirement requirements.txt \
    --requirement requirements-freeze.txt
