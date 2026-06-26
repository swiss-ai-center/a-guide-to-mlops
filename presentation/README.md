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

**Bertil Chapuis · Ludovic Delafontaine · Rémy Marquis · Leonard Cseres**

Swiss AI Center contributors

[Website][website] · [GitHub][github]

![bg right:35% w:70%](../docs/assets/images/hero-rocket.svg)

---

## By the end of this talk

<!-- _class: lead -->

You will know **how to move an ordinary ML project from a Jupyter Notebook to
production on the cloud** using a small, composable set of MLOps practices.

![bg right:35% w:70%](../docs/assets/images/hero-rocket.svg)

## About us

<!-- _class: lead -->

## Swiss AI Center

**Five HES from the HES-SO** (HEIG-VD, HEIA-FR, HE-Arc, HEVS and HEPIA) work on
a project called **Swiss AI Center**.

Its mission is to **accelerate the adoption of artificial intelligence in the
digital transition of Swiss SMEs**.

**HEIG-VD** is responsible for **setting up tools to manage ML experiments from
code to production**.

## Our team

<!--
_paginate: false
-->

<div class="four-columns">

<div class="center">

**Bertil
Chapuis**
<small>Professor</small>

![w:200](./images/bertil-chapuis.png)

[Mail](mailto:bertil.chapuis@heig-vd.ch)

</div>
<div class="center">

**Ludovic
Delafontaine**
<small>Lecturer</small>

![w:200](./images/ludovic-delafontaine.png)

[Mail](mailto:ludovic.delafontaine@heig-vd.ch)

</div>
<div class="center">

**Rémy
Marquis**
<small>aR&D Associate</small>

![w:200](./images/remy-marquis.png)

[Mail](mailto:remy.marquis@heig-vd.ch)

</div>
<div class="center">

**Leonard
Cseres**
<small>Assistant</small>

![w:200](./images/leonard-cseres.png)

[Mail](mailto:leonard.cseres@heig-vd.ch)

</div>
</div>

## Introduction

<!-- _class: lead -->

## LLMs and agentic AI are everywhere

But not here.

**Most companies have ordinary data problems**

- Data trapped in spreadsheets, logs, and sensors.
- Forecasts built on fragile business systems.
- Classifiers trained on years of messy history.
- Anomaly detection on manufacturing or server metrics.

## ML code vs ML system

![bg right:39% 100%](../docs/assets/images/ml_system.svg)

Only a small fraction of real-world ML systems is composed of the ML code.

The required surrounding infrastructure is vast and complex.

## Difficulties with ML projects

**Reproducibility**

> I ran the experiment but didn’t get the same results.

**Buildability**

> It builds on my machine — does it build on yours?

---

**Performance tracking**

> I hope my changes help… and that it still works in production.

**Deployment**

> Can I use your model from my app? How?

## Who faces these problems?

<!-- _class: lead -->

Big labs get the headlines. **Small teams get the same headaches.**

## A solution

**MLOps**

Borrow proven Software and DevOps practices and adapt them to machine learning.

![bg right:40% 110%](./images/mlops-venn-diagram.svg)

## Our proposal

**From notebook to production — one practice at a time**

🛠️ Version-controlled, composable, incremental MLOps

📖 A practical guide for small teams, not a heavy platform

![bg right:40% 90%](./images/a-guide-to-mlops.png)

## Our approach

**Version-controlled.** Track code, data, and experiments together.

**Composable.** Use the best open-source tool for each job.

**Incremental.** Adopt one practice at a time.

**Pragmatic.** Reproducibility first, then automation, deployment, monitoring,
and feedback loops.

---

## What is this not?

<!-- _class: lead -->

This guide is **not** a heavy, all-in-one MLOps platform.

It is a **lightweight, composable path** for small teams who already use Git and
want to go from notebook to production one step at a time.

## A guide to MLOps

<!-- _class: lead -->

A quick presentation of the guide

### _"Welcome to the team!"_

You just have joined a team of data scientists and machine learning (ML)
engineers (_welcome!_).

The team is working on a model capable of visually identifying planets or moons
within our solar system from images in a Jupyter Notebook.

The team is facing difficulties to move the model to production.

Your mission is to help the team to improve the model and deploy it to the cloud
using MLOps best practices.

### The big picture

![bg](./images/the-big-picture.svg)

---

![bg w:90%](./images/guide-demo-01.png) ![bg w:90%](./images/guide-demo-02.png)

---

![bg w:90%](./images/guide-demo-03.png) ![bg w:90%](./images/guide-demo-04.png)

---

![bg w:90%](./images/guide-demo-05.png) ![bg w:90%](./images/guide-demo-06.png)

---

![bg w:90%](./images/guide-demo-07.png) ![bg w:90%](./images/guide-demo-08.png)

---

![bg w:90%](./images/guide-demo-09.png) ![bg w:90%](./images/guide-demo-10.png)

---

![bg w:90%](./images/guide-demo-11.png) ![bg w:90%](./images/guide-demo-12.png)

---

![bg w:90%](./images/guide-demo-13.png) ![bg w:90%](./images/guide-demo-14.png)

---

![bg w:90%](./images/guide-demo-15.png) ![bg w:90%](./images/guide-demo-16.png)

---

![bg w:90%](./images/guide-demo-17.png) ![bg w:90%](./images/guide-demo-18.png)

## Target audience

For **small teams and SMEs** who want to move ML from notebooks to production without a heavy, monolithic platform.

If you use Git and want practical, incremental steps, this is for you.

![bg right:40% 80%](../docs/assets/images/rocket-to-planet.svg)

## What you need

**Knowledge:** Basic Python and terminal use.

**Hardware/OS:** macOS, Linux, or Windows with WSL2.

**Accounts:** GitHub and Google Cloud.

**Tools:** Python 3.13, pip, git, unzip, Docker, VS Code recommended.

![bg right:40% 70%](./images/python-logo.svg)

## Access the guide

👉 Access the guide at [mlops.swiss-ai-center.ch][website].

💪 Feel free to open an issue on [GitHub][github] if you encounter any
difficulties or want to contribute.

🙏 Leave us a star if you like the guide!

![bg right:40% w:60%][website-qrcode]

## Your next step

<!-- _class: lead -->

**Pick one practice** from the guide and try it on your own notebook this week.

Start small. Version control first. Then reproduce. Then deploy.

[mlops.swiss-ai-center.ch][website]

## Clean up

Now that you have completed the guide, it is important to properly manage and
remove the resources and environments you have created.

This is necessary to avoid:

* unnecessary incurring costs
* potential security concerns

## Feedback

Your feedback helps us improve! 🙏

💬 Share your thoughts on what worked well and what could be better.

🐛 Report issues or suggest improvements on [GitHub][github].

⭐ Leave us a star if you found this guide helpful!

🤝 Your input directly shapes future versions of this workshop.

## Bonus slides

<!-- _class: lead -->

### Usual ML workflow

- Each developer has their own code, data, and models.
- Experiments are hard to reproduce and improvements are hard to track.
- Models are hard to deploy; drift goes unnoticed.

### We can do better

<!-- _class: lead -->

**One practice at a time.**

### Codebase

**Problem:** Siloed code, hard to share.

**Practice:** One shared, version-controlled codebase.

![bg right:40% w:60%](./images/git-logo.svg)

### Data

**Problem:** Datasets live on individual machines.

**Practice:** Version data like code and share revisions centrally.

![bg right:40% w:60%](./images/dvc-logo.svg)

### Reproduce

**Problem:** Manual steps and hidden hyperparameters.

**Practice:** Document and automate the full experiment pipeline.

![bg right:40% w:60%](./images/dvc-logo.svg)

### Track

**Problem:** Hard to see which change helped or hurt.

**Practice:** Visual metrics and automated experiment reports.

![bg right:40% w:40% vertical](./images/dvc-logo.svg)
![bg right:40% w:40% vertical](./images/cml-logo.svg)

### Serve

**Problem:** The model is trapped in the notebook.

**Practice:** Package and expose it through an API.

![bg right:40% w:40% vertical](./images/bentoml-logo.svg)
![bg right:40% w:40% vertical](./images/docker-logo.svg)

### Deploy

**Problem:** Works on my machine; no clean way to ship.

**Practice:** Containerize and deploy to the cloud automatically.

![bg right:40% w:60%](./images/kubernetes-logo.svg)

### Monitor

**Problem:** Drift and degradation are discovered too late.

**Practice:** Continuous performance and data-drift checks.

![bg right:40% w:60%](./images/evidently.svg)

### Label

**Problem:** Model quality plateaus on stale data.

**Practice:** Label new data and retrain on a schedule.

![bg right:40% w:60%](./images/label-studio-logo.svg)

## Sources

-   MLOps Venn diagram by Cmbreuel on
    [Wikipedia](https://commons.wikimedia.org/wiki/File:ML_Ops_Venn_Diagram.svg)
-   ML system diagram by [D. Sculley et. al. NIPS 2015: Hidden technical debt in Machine learning systems](https://dl.acm.org/doi/10.5555/2969442.2969519)

---

## Contributions

**From notebook to production — one practice at a time**

You now know how to:

1. **Version** code, data, and experiments together.
2. **Reproduce** any experiment at any time.
3. **Track** model evolution and catch drift early.
4. **Deploy** a model to the cloud and serve it over the Internet.
5. **Close the loop** with new labels and retraining.

![bg right:35% w:60%](../docs/assets/images/launchpad.svg)
