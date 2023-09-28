# Infrastructure

## Introduction

This is the infrastructure used for the A guide to MLOps project. The
instructions are meant to be used on a publicely available virtual machine. At
the moment, the virtual machine (VM) is hosted by the HEIG-VD.

## Setup

The VM has been setup using the following commands.

### Update the system

```sh
# Update the available packages
sudo apt update

# Update the packages to their latest versions
sudo apt --yes full-upgrade

# Remove unused packages
sudo apt --yes autoremove --purge
```

### Install Docker

```sh
# Install required packages to add the Docke APT repository
sudo apt install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Create the keyrings directory
sudo mkdir --parent /etc/apt/keyrings

# Add the Docker GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add the Docker APT repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update the packages
sudo apt update

# Install Docker and its Compose plugin
sudo apt install --yes docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add the current user to the `docker` group
sudo usermod --append --groups docker $USER

# Enable and start the Docker service
sudo systemctl enable docker
sudo systemctl start docker
```

### Install git

```sh
# Install git
sudo apt install git
```

### Create a new user

```sh
# Create a new user `a-guide-to-mlops`
sudo useradd -m a-guide-to-mlops

# Setup the user's `a-guide-to-mlops` password
sudo passwd a-guide-to-mlops

# Add the `a-guide-to-mlops` user to the `docker` and `ssh` groups
sudo usermod -a -G docker,ssh a-guide-to-mlops

# Reboot to apply all updates
sudo reboot now
```

### Clone the repository

```sh
# Clone the infrastructure repository
git clone https://github.com/swiss-ai-center/a-guide-to-mlops.git
```

## Configure and start the applications

Each application has its own directory with its configuration. A detailed
documentation is available in each directory.

You might want to edit the `.env` and `*.env` files to change the FQDNs and the
application's configuration based on your needs.

Each application has its Docker Compose configuration, allowing to manage the
application individually.

```sh
# Start Traefik
docker compose --project-directory ./a-guide-to-mlops/infrastructure/traefik up --detach

# Start MinIO
docker compose --project-directory ./a-guide-to-mlops/infrastructure/minio up --detach

# Start Label Studio
docker compose --project-directory ./a-guide-to-mlops/infrastructure/label-studio up --detach
```
