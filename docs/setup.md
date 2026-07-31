# Setup

This page helps you prepare your machine before starting the guide, whether you
use :fontawesome-brands-windows: Windows with
[Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/)
(WSL 2), a native :simple-linux: Linux (Ubuntu) installation or :simple-apple:
macOS.

## Windows only

The following steps prepare a :fontawesome-brands-windows: Windows machine with
WSL 2. Skip this section if you already use a native :simple-linux: Linux
installation or :simple-apple: macOS.

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

The guide requires Python 3.13 for framework compatibility, even though recent
systems ship a newer version by default.

=== ":simple-linux: :simple-ubuntu: Linux (Ubuntu)"

    Install Python 3.13 with the package manager, and `unzip` which is used in the
    guide to extract archives:

    ```sh
    # Install Python 3.13, venv support and unzip
    sudo apt install python3.13 python3.13-venv unzip
    ```

    !!! tip "Python 3.13 not available?"

        If `python3.13` is not packaged for your Ubuntu release, use the
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

    Alternatively to the system package manager, install
    [:simple-uv: uv](https://docs.astral.sh/uv/) and use it to install Python 3.13:

    ```sh
    # Install uv
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Make uv available in the current shell
    source $HOME/.local/bin/env

    # Install Python 3.13
    uv python install 3.13
    ```

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

    Then check the following settings:

    - :fontawesome-brands-windows: **Windows (including WSL 2)**: install the
      Windows version of Docker Desktop, not the Linux version inside WSL. Then make
      sure the WSL integration is enabled in
      **Settings → Resources → WSL Integration** so Docker Desktop integrates with
      your Ubuntu distribution.
    - :simple-apple: **macOS**: in case of troubles when building Docker images
      on Apple Silicon, consider disabling
      **Use Rosetta for x86_64/amd64 emulation on Apple Silicon** in
      **Settings → General**. The guide builds Docker images for the `linux/amd64`
      architecture, and the build can fail under Rosetta emulation.

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
