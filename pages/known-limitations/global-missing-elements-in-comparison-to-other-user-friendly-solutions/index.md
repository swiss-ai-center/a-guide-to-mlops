---
title: "Global: Missing elements in comparison to other user-friendly solutions"
---

# {% $markdoc.frontmatter.title %}

This section tries to highlight the missing elements the current solution misses to become as user-friendly as solutions such as [Lobe](https://www.lobe.ai/).

## Observations

As mentioned above, Label Studio seems to be the limiting factor to be able to have a full life-cycle machine learning experiment platform as it cannot easily retrain the model with new labelized data.

Tools and projects must be manually configured in order to set up a new machine learning environment for a team.

## Implications

Not a smooth and user-friendly experience.

## Ideas considered

Use Terraform to configure VCS to:

- Create new organizations and projects with all the required configuration to run the pipeline

Use Ansible to configure hosts to host:

- A Kubernetes cluster
- MinIO service
- Label Studio and its dependencies
- The model with MLEM
