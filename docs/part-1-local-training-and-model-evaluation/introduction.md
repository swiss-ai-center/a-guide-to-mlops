---
title: "Part 1 - Introduction"
---

# Introduction

Learn how to train a model locally and evaluate it using
[:simple-dvc: DVC](../tools.md).

## Environment

This guide has been written with :simple-apple: macOS and :simple-linux: Linux
operating systems in mind. If you use :fontawesome-brands-windows: Windows, you
might encounter issues. Please use the
[Windows Subsystem for Linux](https://learn.microsoft.com/en-us/windows/wsl/)
(WSL 2) for optimal results.

## Requirements

The following requirements are necessary to follow this part:

- An IDE. We recommend to use
  [:material-microsoft-visual-studio-code: Visual Studio Code](https://code.visualstudio.com/)
  to follow this guide.
- [:simple-python: Python 3.13](https://www.python.org/downloads/)
- [:simple-python: pip](https://pip.pypa.io/)
- [:simple-git: Git](https://git-scm.com/)
- [unzip](https://linux.die.net/man/1/unzip)

??? danger "Using Conda, Anaconda, Poetry, or similar? Read this!"

    **Why we avoid most helper tools**

    Conda, Anaconda, Poetry, and similar tools add abstraction layers that make
    debugging significantly harder when things go wrong. Their complexity introduces
    intricate failure modes that require substantial time and expertise to diagnose,
    often outweighing any convenience they provide.

    This guide is tested and validated with vanilla Python only. If you still want
    to use Conda/Anaconda/Poetry/etc., be aware that you might encounter issues we
    cannot help you debug.

??? info "Our approach to Python tools"

    **Why we use standard Python**

    This guide uses `pip` and `venv` as its default tools because they are part of
    the Python standard ecosystem, maintained by the Python Packaging Authority
    (PyPA) under the Python Software Foundation. They evolve slowly, but they are
    stable, universally available, and above all easy to debug when issues arise,
    which is a critical property for a tutorial.

    **Why `uv` is the exception**

    You might wonder why we warn against helper tools yet still show `uv` throughout
    this guide. [uv](https://docs.astral.sh/uv/) is a notable exception because it
    is extremely fast, adheres to the relevant [PEPs](https://peps.python.org/)
    (Python Enhancement Proposals, the community's standardization documents), and
    its `uv pip` interface is a drop-in replacement for `pip`. It also fills a
    genuine gap in the standard toolchain: it can install and manage Python versions
    themselves (`uv python install`), not just packages within an existing
    interpreter. For this reason, optional `uv` command alternatives are shown
    throughout the guide.

    Keep in mind, however, that `uv` is developed by a private company (Astral, now
    part of OpenAI). While it is open source and production ready today, its
    long-term roadmap could shift. Standard `pip` + `venv` will always remain the
    safe, portable baseline.

??? warning "For WSL2 users"

    Ensure you are working in the Linux filesystem, not the mounted Windows
    filesystem.

    Run `cd ~` to navigate to your Linux home directory. Avoid working in `/mnt/*`
    paths, as cross-filesystem operations cause severe performance bottlenecks when
    installing packages with pip.
