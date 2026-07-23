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
        --color-background: #f7f8fc;
        --color-foreground: #0a0a0a;
        --color-highlight: #d97706;
        --color-dimmed: #525252;
        --color-headings: #b45309;
        --color-card: #ffffff;
        --color-border: #d4d4d4;
    }
    section {
        background: var(--color-background);
        color: var(--color-foreground);
    }
    a:link, a:visited {
        color: var(--color-highlight);
    }
    strong {
        color: var(--color-highlight);
    }
    blockquote {
        font-style: italic;
        border-left: 4px solid var(--color-highlight);
        padding-left: 1rem;
        color: var(--color-dimmed);
    }
    table {
        width: 100%;
    }
    th {
        background: var(--color-card);
        color: var(--color-headings);
        border-bottom: 2px solid var(--color-border);
    }
    td {
        border-bottom: 1px solid var(--color-border);
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
        border: 1px solid var(--color-border);
        margin-top: 50px;
        margin-bottom: 50px;
    }
    footer {
        color: var(--color-dimmed);
        font-size: 0.5rem;
    }
    .four-columns {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 1rem;
    }
    .center {
        text-align: center;
    }
    .stars-bg {
        background-color: var(--color-background);
        background-image:
            radial-gradient(circle, var(--color-border) 1.5px, transparent 2px),
            radial-gradient(circle, var(--color-highlight) 1px, transparent 1.5px);
        background-size: 120px 120px, 180px 180px;
        background-position: 0 0, 60px 60px;
    }
    /* Tighten split-background layouts: Gaia's 70px section padding wastes
       space beside background images, so reduce the inner padding on the
       content side and align the background image toward the content. */
    section[data-marpit-advanced-background="content"][data-marpit-advanced-background-split="right"] {
        padding-right: 30px !important;
    }
    section[data-marpit-advanced-background="content"][data-marpit-advanced-background-split="left"] {
        padding-left: 30px !important;
    }
    section[data-marpit-advanced-background="background"][data-marpit-advanced-background-split="right"] > div[data-marpit-advanced-background-container] > figure {
        background-position: left center !important;
    }
    section[data-marpit-advanced-background="background"][data-marpit-advanced-background-split="left"] > div[data-marpit-advanced-background-container] > figure {
        background-position: right center !important;
    }
headingDivider: 4
-->

[license]: https://github.com/swiss-ai-center/a-guide-to-mlops/blob/main/LICENSE
[website]: https://mlops.swiss-ai-center.ch
[website-qrcode]:
    https://quickchart.io/qr?format=png&ecLevel=Q&size=400&margin=1&text=https://mlops.swiss-ai-center.ch
[github]: https://github.com/swiss-ai-center/a-guide-to-mlops

# A guide to MLOps

<!--
_class: lead stars-bg
_paginate: false
-->

**Swiss AI Center**

<small>Bertil Chapuis · Ludovic Delafontaine · Rémy Marquis · Leonard Cseres</small>

<small>[Website][website] · [GitHub][github]</small>

![bg right:35% w:70%](./images/portals/hero-rocket.svg)

## The promise -> empowerment promise

<!-- _class: lead -->

<!-- Speaker note: This is the empowerment promise. -->

By the end of this workshop, you will know how to move an ordinary ML project
from a messy **Jupyter notebook** to a **reproducible, cloud-deployed, monitored ML
system**.

## About us

<!--
_paginate: false
-->

**Swiss AI Center:** accelerates AI adoption in SMEs digital transition.
**HEIG-VD:** tools to manage ML experiments from code to production.

<div class="four-columns">

<div class="center">

**Bertil<br>Chapuis**<br>
<small>Professor</small>

![w:180](./images/bertil-chapuis.png)

</div>
<div class="center">

**Ludovic<br>Delafontaine**<br>
<small>Lecturer</small>

![w:180](./images/ludovic-delafontaine.png)

</div>
<div class="center">

**Rémy<br>Marquis**<br>
<small>aR&D Associate</small>

![w:180](./images/remy-marquis.png)

</div>
<div class="center">

**Leonard<br>Cseres**<br>
<small>Assistant</small>

![w:180](./images/leonard-cseres.png)

</div>
</div>

<!--
Speaker notes:

Five HES from the HES-SO (HEIG-VD, HEIA-FR, HE-Arc, HEVS and HEPIA) work on a
project called Swiss AI Center.

HEIG-VD is responsible for setting up tools to manage ML experiments from code
to production.
-->

## The trap -> problem

<!-- _class: lead -->

## LLM hype is everywhere

But most companies have **ordinary data problems**

- Data trapped in spreadsheets, logs, and sensors.
- Forecasts built on fragile business systems.
- Classifiers trained on years of messy history.
- Anomaly detection on manufacturing or server metrics.

## ML code vs ML system

<!-- Speaker note: This is the surprise. -->

![bg right:35% w:90%](./images/ml_system.svg)

Only a **small fraction** of real-world ML systems is composed of the ML code.

The required surrounding infrastructure is vast and complex.

## Difficulties with ML projects

<!-- Speaker note: Pause after the question. -->

Have you ever heard or said any of these?

> I ran the experiment but didn't get the same results

> I tried to build the model on my machine but it doesn't work...

> The model worked fine before, but not anymore. Did the data change?

> Can I use your model with my mobile app/website?

<!--
Speaker notes — Bonus slide content:

Usual ML workflow:
- Each member of the team manages their own codebase, their own dataset and their
  own models.
- The reproducibility of the model creation is difficult and cannot be guaranteed
  over time.
- Improvements made to the model are hard to track.
- Models are hard to share and deploy in production.
- Model drift and degradation go unnoticed.

High flexibility for the team, but:
- hard to maintain,
- hard to reproduce in the future,
- time consuming.

We can do better.
-->

## Who faces these problems?

**Small teams** and **SMEs** without the dedicated MLOps teams that big tech
can afford.

-   **Data scientists** ready to leave ad-hoc notebooks and scripts behind
-   **Software engineers** extending DevOps practices to ML

## The fence -> boundary

<!-- _class: lead -->

<!-- Speaker note: This is the fence. -->

**This is not:**

-   a heavy all-in-one MLOps platform
-   a course on machine learning theory

**This is:**

-   a lightweight, composable stack
-   for small teams moving from notebook to production
-   one step at a time

## The path -> solution

<!-- _class: lead -->

<!-- Speaker note: This is the path from notebook to production. -->

## A solution

**MLOps**

➡️ Draw inspiration from Software and DevOps best practices

➡️ Adapting these practices to the world of machine learning

➡️ Improve the management and quality of machine learning projects

![bg right:40% 110%](./images/mlops-venn-diagram.svg)

## Our proposal

**A hands-on guide**

🛠️ A reproducible planet/moon classifier workflow

🚀 Deployed and monitored on the cloud

📖 Transferable to your own experiment and context

![bg right:40% 90%](./images/a-guide-to-mlops.png)

## The guide -> hands-on mission

<!-- _class: lead -->

<!-- Speaker note: This is the story. -->

## Welcome to the team

You just joined a team of data scientists and ML engineers.

Their mission: build a model that visually identifies planets or moons from
images.

Their problem: the model lives in a Jupyter Notebook, and they cannot ship it.

**Your mission: help them improve the model and deploy it to the cloud.**

### The big picture

![bg](./images/the-big-picture.svg)

## 1. Track experiments with DVC

![bg right:55% w:95%](./images/a-guide-to-mlops.png)

Every run is versioned and reproducible.

<!--
Speaker notes — Bonus slide content:

Codebase — current situation:
- Each developer has their own codebase.
- Sharing the code with peers is difficult.

Codebase — what we improve:
- Allow each developer to improve a common codebase.
- Quickly benefit from the work of others.

Data — current situation:
- The dataset must be manually downloaded and put in the right place.
- Different datasets are being used at the same time.
- Datasets are hard to improve.

Data — what we improve:
- Allow the usage of a common and up-to-date dataset.
- Efficiently share new revisions to train the model.
- Datasets can be stored anywhere.

Reproduce — current situation:
- Steps to create the model can be complex.
- Intermediate commands should not be skipped.
- Hyperparameters are hard to track from one run to another.

Reproduce — what we improve:
- Document the steps to reproduce the experiment.
- Ensure it can be run anytime in the future.
- DVC can improve time efficiency.
-->

## 2. Review results with CML

![bg right:55% w:95%](./images/a-guide-to-mlops.png)

Metrics and plots arrive directly in the pull request.

<!--
Speaker notes — Bonus slide content:

Tracking — current situation:
- Changes to a model are difficult to track.
- Visualizing the differences is hard.
- Cannot guarantee the changes are beneficial.

Tracking — what we improve:
- Have a visual way to identify the consequences of the changes made to a model.
- Errors and anomalies are easily identified.
-->

## 3. Serve and deploy the model

![bg right:55% w:95%](./images/a-guide-to-mlops.png)

The model becomes an API that any application can call.

<!--
Speaker notes — Bonus slide content:

Serving and publishing — current situation:
- The model is hard to use outside the experiment context.
- The model is hard to deploy in production.
- The model is hard to share with others.

Serving and publishing — what we improve:
- The model can be used outside the experiment context.
- The model can be deployed in production.
- The model can be shared with others.

Deployment — current situation:
- An experiment can run on one machine but can fail on another.
- Models must be prepared to be run outside their experiment context.
- Exposing the model to the outside world is hard.

Deployment — what we improve:
- Run the experiment in a clean state to ensure it works everywhere.
- Package the model with all its dependencies.
- The model can be used over the Internet by other applications.
- Automate the process.
-->

## 4. Monitor and maintain the model

![bg right:55% w:95%](./images/a-guide-to-mlops.png)

Observe the model predictions for data drift.

<!--
Speaker notes — Bonus slide content:

Monitoring — current situation:
- The model's behavior can drift over time.
- Degradation in performance is hard to detect.
- Issues are often discovered too late, after users are impacted.

Monitoring — what we improve:
- Track model performance and data drift continuously.
- Detect anomalies and regressions early.
- Alert the team when the model needs attention.
-->

## 5. Label and retrain

![bg right:55% w:95%](./images/a-guide-to-mlops.png)

Add data with AI assistance and improve iteratively.

<!--
Speaker notes — Bonus slide content:

Labeling — current situation:
- Model code and parameters are optimized.
- Model performance is only as good as the quality of the current data.
- We need new data to improve the model's performance.

Labeling — what we improve:
- Label new data to further improve the model's performance.
- Use new data to retrain and improve the model.
- Make use of AI inference to speed up the labeling process.
-->

## Our principles

<!-- Speaker note: Deliver on the opening promise. -->

**Version-controlled.** Track code, data, and experiments together.

**Composable.** Use the best open-source tool for each job.

**Incremental.** Adopt one practice at a time.

**Pragmatic.** Reproducibility first, then automation, deployment, monitoring, and feedback loops.

## What you need

**Knowledge:** Basic Python and terminal use

**OS:** macOS, Linux, or Windows with WSL2

**Accounts:** GitHub, Google Cloud with valid credit card

**Tools:** Python 3.13, pip or uv, git, unzip, Docker, editor

![bg right:40% 70%](./images/python-logo.svg)

## Access the guide

-   Open [mlops.swiss-ai-center.ch][website]
-   Contributions and stars on [GitHub][github]
-   Built iteratively from your feedback

![bg right:40% w:60%][website-qrcode]
