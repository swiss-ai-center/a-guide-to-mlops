---
title: "Introduction"
---

# {% $markdoc.frontmatter.title %}

## Welcome

Welcome! We are glad that you are here. :)

This guide will help you through incremental steps from a traditional approach of managing ML projects to a modern ML Ops approach designed to improve team collaboration and reproducibility.

For the rest of the guide, an _experiment_ is a machine learning project.

We chose the term _experiment_ to address the experimental nature of the machine learning field before finding a suitable model.

## Disclaimer

This guide has been written for macOS and Linux operating systems in mind. If you use Windows, you might encounter issues. Please use a decent terminal ([GitBash](https://gitforwindows.org/) for instance) or a Windows Subsystem for Linux (WSL) for optimal results.

This guide assumes that the steps to be performed are done in a working directory independently of it.

The tools and approach must be adapted to your specific use-case and experiments as well.

## Requirements

The following tools must be installed to follow this guide.

- [Python 3](https://www.python.org/downloads/);
- [Git](https://git-scm.com/);
- Standard *nix utilities such as wget, unzip, etc.

// TODO mettre a plat tout les utilitaires, insister que ils doivent les installer (avec brew ou apt-get) éventuellement leur donner les commandes avec --version pour vérifier.

## Tips

If the Git repository is cloned locally, you can use the following command to compare two directories.

```sh
# Compare step 1 and step 2
git diff --no-index \
    pages/the-guide/step-1-run-a-simple-ml-experiment \
    pages/the-guide/step-2-share-your-ml-experiment-code-with-git
```

## Next step

- **Next**: [Step 1: Run a simple ML experiment](/the-guide/step-1-run-a-simple-ml-experiment)
