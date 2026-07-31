# Setup

This page helps you prepare your machine before starting the guide, whether you
use :fontawesome-brands-windows: Windows with
[Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/)
(WSL 2), a native :simple-linux: Linux (Ubuntu) installation or :simple-apple:
macOS.

!!! note

    Unless stated otherwise, all commands on this page are meant to be run in your
    terminal (the WSL terminal on Windows). Only the WSL 2 installation itself is
    done from Windows PowerShell.

## Windows only

The following steps prepare a :fontawesome-brands-windows: Windows machine with
WSL 2. Skip this section if you already use a native :simple-linux: Linux
installation or :simple-apple: macOS.

### Terminal

Install
[Windows Terminal](https://learn.microsoft.com/en-us/windows/terminal/install)
from the Microsoft Store for a modern terminal experience.

### WSL 2

From a PowerShell with administrator rights:

```powershell
# Update WSL
wsl --update

# List the distributions available online
wsl --list --online

# Install Ubuntu (check the exact name in the list above, e.g. Ubuntu-26.04)
wsl --install Ubuntu-26.04

# Check the installed distributions and their WSL version
wsl -l -v
```

On the first launch, Ubuntu asks you to create a username and password. This
account has `sudo` rights inside the Linux environment.

## System update

=== ":simple-linux: :simple-ubuntu: Linux (Ubuntu)"

    Inside the Linux terminal:

    ```sh
    # Update the package lists
    sudo apt update

    # Upgrade the installed packages
    sudo apt upgrade
    ```

=== ":simple-apple: macOS"

    !!! note

        No specific macOS version is required for this guide. If you wish to update your
        system, use **System Settings → General → Software Update**, keeping in mind
        this can take a while.

    Install [Homebrew](https://brew.sh/) if it is not already installed. It is used
    in the following sections:

    ```sh
    # Install Homebrew
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

## Python

The guide requires Python 3.13.

=== ":simple-linux: :simple-ubuntu: Linux (Ubuntu)"

    Install Python 3.13 with the package manager, and `unzip` which is used in the
    guide to extract archives:

    ```sh
    # Install Python 3.13, venv support and unzip
    sudo apt install python3.13 python3.13-venv unzip
    ```

    !!! tip "Why Python 3.13?"

        Recent Ubuntu releases ship a newer Python version (3.14) by default, but this
        guide explicitly requires Python 3.13 for framework compatibility. If
        `python3.13` is not packaged for your Ubuntu release, use the
        [deadsnakes PPA](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa):

        ```sh
        # Install add-apt-repository if needed
        sudo apt install software-properties-common

        # Add the deadsnakes PPA and update the package lists
        sudo add-apt-repository ppa:deadsnakes/ppa -y
        sudo apt update

        # Install Python 3.13 and venv support
        sudo apt install python3.13 python3.13-venv
        ```

=== ":simple-apple: macOS"

    ```sh
    # Install Python 3.13
    brew install python@3.13
    ```

    `unzip`, used in the guide to extract archives, is already included with macOS.

=== ":simple-linux: :simple-apple: Using uv"

    Install [:simple-uv: uv](https://docs.astral.sh/uv/), which can also install and
    manage Python versions by itself:

    ```sh
    # Install uv
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Make uv available in the current shell
    source $HOME/.local/bin/env
    ```

    Python 3.13 is then installed automatically when creating a virtual environment
    with `uv venv --python 3.13`.

## Git

=== ":simple-linux: :simple-ubuntu: Linux (Ubuntu)"

    ```sh
    # Install Git
    sudo apt install git
    ```

=== ":simple-apple: macOS"

    ```sh
    # Install Git
    brew install git
    ```

Then configure your identity:

```sh
# Configure your identity (replace with your own information)
git config --global user.email "your@email"
git config --global user.name "Your Name"

# Configure line endings
git config --global core.autocrlf input
```

!!! tip "For WSL 2 users"

    On native Windows, Git is usually configured with `core.autocrlf true` to
    convert line endings between Windows files (CRLF) and the repository (LF).
    Inside WSL, Git is a Linux program with its own configuration, and files are
    checked out and used by Linux tools, so `input` is the correct setting there.

## Docker

Docker is used later in the guide to package and serve the model.

=== ":fontawesome-brands-windows: :simple-apple: :simple-linux: Using Docker Desktop"

    Install [Docker Desktop](https://www.docker.com/products/docker-desktop/),
    available for :fontawesome-brands-windows: Windows, :simple-apple: macOS and
    :simple-linux: Linux.

    On Windows, Docker Desktop uses the WSL 2 backend and integrates with your
    Ubuntu distribution. Make sure the integration is enabled in
    **Settings → Resources → WSL Integration**.

=== ":simple-ubuntu: Using Docker CLI (Linux only)"

    On :simple-linux: Linux, install the Docker engine and CLI directly in the Linux
    environment:

    ```sh
    # Install Docker and the Buildx plugin
    sudo apt install docker.io docker-buildx

    # Check that the Docker service is running
    sudo systemctl status docker

    # Add your user to the docker group (created automatically by the package)
    sudo usermod -aG docker $USER
    ```

    Log out and back in (or run `su - $USER` to start a fresh shell), then check
    with `groups` that `docker` appears in the list.

    !!! tip "For WSL 2 users"

        If `systemctl` reports that systemd is not running, start the Docker service
        manually with `sudo service docker start`.

## Kubernetes tools

The deployment chapters require `kubectl` and the `gke-gcloud-auth-plugin`
authentication plugin. Both are installed later in the guide with the
[Google Cloud CLI](./part-3-serve-and-deploy/chapter-35-deploy-and-access-the-model-on-kubernetes.md):

```sh
# Install kubectl and the GKE authentication plugin with gcloud
gcloud components install kubectl gke-gcloud-auth-plugin
```

If `kubectl` fails with an error about a missing client-go credential plugin,
the `gke-gcloud-auth-plugin` is not installed. Alternatively, on Ubuntu both are
available as packages once the Google Cloud apt repository is configured:

```sh
# Install the GKE authentication plugin with apt
sudo apt install kubectl google-cloud-cli-gke-gcloud-auth-plugin
```
