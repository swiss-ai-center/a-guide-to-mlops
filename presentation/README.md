---
marp: true
---

<!--
theme: gaia
size: 16:9
paginate: true
author: Swiss AI Center contributors
title: 'A guide to MLOps - Presentation'
description: 'Presentation of the MLOps guide'
url: https://mlops.swiss-ai-center.ch/presentation/
footer: '**Swiss AI Center** - A guide to MLOps 2026 - CC BY-SA 4.0'
style: |
    :root {
        --color-background: #080809;
        --color-foreground: #bcbec2;
        --color-highlight: #4051b5;
        --color-dimmed: #bcbec2;
        --color-headings: #4051b5;
    }
    blockquote {
        font-style: italic;
    }
    table {
        width: 100%;
    }
    th:first-child {
        width: 15%;
    }
    h1, h2, h3, h4, h5, h6 {
        color: var(--color-headings);
    }
    h2, h3, h4, h5, h6 {
        text-transform: uppercase;
        font-size: 1.5rem;
    }
    h1 a:link, h2 a:link, h3 a:link, h4 a:link, h5 a:link, h6 a:link {
        text-decoration: none;
    }
    hr {
        border: 1px solid var(--color-foreground);
        margin-top: 50px;
        margin-bottom: 50px
    }
    .four-columns {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 1rem;
    }
    .center {
        text-align: center;
    }
headingDivider: 4
-->

[illustration]: ./images/cover.png
[license]: https://github.com/swiss-ai-center/a-guide-to-mlops/blob/main/LICENSE
[website]: https://mlops.swiss-ai-center.ch
[website-qrcode]:
    https://quickchart.io/qr?format=png&ecLevel=Q&size=400&margin=1&text=https://mlops.swiss-ai-center.ch
[github]: https://github.com/swiss-ai-center/a-guide-to-mlops

# A guide to MLOps

<!--
_class: lead
_paginate: false
-->

[Website][website] · [GitHub][github]

<small>Swiss AI Center contributors</small>

<small>This work is licensed under the [CC BY-SA 4.0][license] license.</small>

![bg opacity:0.5][illustration]

## What you will learn

<!--
_class: lead
_paginate: false
-->

By the end of this session, you will know how to take a Jupyter Notebook and deploy it to production — with reproducible code, versioned data, and automated pipelines.

## About us

<!-- _class: lead -->

<div class="four-columns">

<div class="center">

**Bertil Chapuis**
<small>Professor</small>

![w:150](./images/bertil-chapuis.png)

</div>
<div class="center">

**Ludovic Delafontaine**
<small>aR&D Associate</small>

![w:150](./images/ludovic-delafontaine.png)

</div>
<div class="center">

**Rémy Marquis**
<small>aR&D Associate</small>

![w:150](./images/remy-marquis.png)

</div>
<div class="center">

**Leonard Cseres**
<small>Assistant</small>

![w:150](./images/leonard-cseres.png)

</div>
</div>

<small>Swiss AI Center · HEIG-VD · HEIA-FR · HE-Arc · HEVS · HEPIA</small>

## The scenario

**"Welcome to the team!"**

You just joined a team of data scientists and ML engineers.

They have a Jupyter Notebook that visually identifies planets and moons from images. It works on one laptop. Sometimes.

Your mission: turn this experiment into a production-ready, reproducible system.

## The mess

Each team member has their own codebase, their own dataset, and their own models.

Reproducibility is a fantasy. Improvements are impossible to track. Deploying the model? Even harder.

**We can do better.**

## Why this is hard

Only a small fraction of real-world ML systems is composed of the ML code.

The required surrounding infrastructure is vast and complex.

![bg right:39% 100%](./images/ml_system.svg)

## What this is — and what it is not

**This is** a hands-on path from notebook to production using open-source tools.

**This is not** a deep learning course, a Kubernetes certification, or a platform sales pitch.

## The big picture

![bg](./images/the-big-picture.svg)

## Step 1: Version the code

<!-- _class: lead -->

## Code

**The pain**

- Each developer has their own codebase
- Sharing code with peers is difficult

**The fix**

- A single, shared codebase
- Everyone benefits from improvements immediately

![bg right:40% w:60%](./images/git-logo.svg)

## Step 2: Version the data

<!-- _class: lead -->

## Data

**The pain**

- The dataset must be manually downloaded and placed correctly
- Different datasets are used at the same time
- Datasets are hard to improve

**The fix**

- A common, up-to-date dataset for everyone
- Efficiently share new revisions to train the model
- Store datasets anywhere

![bg right:40% w:60%](./images/dvc-logo.svg)

## Step 3: Reproduce experiments

<!-- _class: lead -->

## Reproduce

**The pain**

- Steps to create the model are complex
- Intermediate commands get skipped
- Hyperparameters are hard to track from one run to another

**The fix**

- Document the steps to reproduce the experiment
- Ensure it can be run anytime in the future
- Let the pipeline tool handle the rest

![bg right:40% w:60%](./images/dvc-logo.svg)

## Step 4: Track changes

<!-- _class: lead -->

## Track

**The pain**

- Changes to a model are difficult to track
- Visualizing differences is hard
- You cannot guarantee the changes are beneficial

**The fix**

- A visual way to see the consequences of every change
- Errors and anomalies are easy to spot

![bg right:40% w:40% vertical](./images/dvc-logo.svg)
![bg right:40% w:40% vertical](./images/cml-logo.svg)

## Step 5: Serve the model

<!-- _class: lead -->

## Serve

**The pain**

- The model is hard to use outside the experiment context
- The model is hard to deploy in production
- The model is hard to share with others

**The fix**

- Use the model outside the notebook
- Deploy it in production
- Share it with other teams

![bg right:40% w:40% vertical](./images/bentoml-logo.svg)
![bg right:40% w:40% vertical](./images/docker-logo.svg)

## Step 6: Deploy to production

<!-- _class: lead -->

## Deploy

**The pain**

- An experiment runs on one machine but fails on another
- Models must be prepared to run outside their experiment context
- Exposing the model to the outside world is hard

**The fix**

- Run the experiment in a clean state so it works everywhere
- Package the model with all its dependencies
- Expose the model over the Internet
- Automate the entire process

![bg right:40% w:60%](./images/kubernetes-logo.svg)

## Step 7: Label new data

<!-- _class: lead -->

## Label

**The pain**

- Model code and parameters are already optimized
- Performance is only as good as the current data quality
- You need new data to improve further

**The fix**

- Label new data to improve the model's performance
- Use new data to retrain
- Use AI inference to speed up the labeling process

![bg right:40% w:60%](./images/label-studio-logo.svg)

## What you can do now

<!--
_class: lead
_paginate: false
-->

You can take a Jupyter Notebook and deploy it to production — reproducibly.

## Who is this for

🤖 You regularly work with machine learning projects

📊 You want to improve processes to ensure quality

🏗️ You want to consolidate your current infrastructure

☁️ You want to move to the Cloud

![bg right:40% 80%](./images/target-audiance.svg)

## Prerequisites

♿ Accessible to everyone

🧠 Basic knowledge of Python and the terminal is sufficient

💳 A valid credit card for cloud deployment

🤝 You will be accompanied throughout the guide

![bg right:40% 70%](./images/python-logo.svg)

## Technical checks

Before we start:

💻 macOS, Linux, or Windows with WSL2

📝 Editor and Terminal (VS Code recommended)

🛠️ Python 3.13, pip, git, unzip, docker

☁️ GitHub account, Google Cloud account

## Access the guide

👉 [mlops.swiss-ai-center.ch][website]

💬 Open an issue on [GitHub][github] if you get stuck.

⭐ Leave us a star if this helps.

![bg right:40% w:60%][website-qrcode]

## Go from experiment to production

<!--
_class: lead
_paginate: false
-->

That is MLOps. 🚀

## Sources

- MLOps Venn diagram by Cmbreuel on [Wikipedia](https://commons.wikimedia.org/wiki/File:ML_Ops_Venn_Diagram.svg)
- ML system diagram by [D. Sculley et. al. NIPS 2015: Hidden technical debt in Machine learning systems](https://dl.acm.org/doi/10.5555/2969442.2969519)
- Robot illustration by [OpenClipart-Vectors](https://pixabay.com/users/openclipart-vectors-30363/) on [Pixabay](https://pixabay.com/vectors/cartoon-comic-dance-happy-joy-1295224/)
