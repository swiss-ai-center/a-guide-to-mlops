# Base image
FROM python:3.13

# Working directory
WORKDIR /workspaces/a-guide-to-mlops

# Copy the dependencies
COPY requirements-freeze.txt .

# Install Python dependencies
RUN pip install -r requirements-freeze.txt
