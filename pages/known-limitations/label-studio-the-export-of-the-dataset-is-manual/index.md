---
title: "Label Studio: The export of the dataset is manual"
---

# {% $markdoc.frontmatter.title %}

## Observations

When a dataset is improved through Label Studio, the dataset must be manually exported to the ML experiment workspace, manually update DVC and manually update the data metadata with Git.

## Implications

This is directly related to the limitations stated above where the data cannot evolve without updating the related metadata files with Git.

## Ideas considered

Extend Label Studio in order to allow a DVC + Git exportation. This implies Label Studio must have access to the Git repository and the permissions to update it. The dataset is exported, committed and pushed to DVC and Git.
