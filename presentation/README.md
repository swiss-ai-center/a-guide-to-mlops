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
footer: '**Swiss AI Center** - A guide to MLOps 2024 - CC BY-SA 4.0'
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
[license]:
  https://github.com/swiss-ai-center/a-guide-to-mlops/blob/main/LICENSE
[website]:
  https://mlops.swiss-ai-center.ch
[website-qrcode]:
  https://quickchart.io/qr?format=png&ecLevel=Q&size=400&margin=1&text=https://mlops.swiss-ai-center.ch

[github]:
  https://github.com/swiss-ai-center/a-guide-to-mlops

# A guide to MLOps

<!--
_class: lead
_paginate: false
-->

[Website][website] · [GitHub][github]

<small>Swiss AI Center contributors</small>

<small>This work is licensed under the [CC BY-SA 4.0][license] license.</small>

![bg opacity:0.5][illustration]

## Introduction

<!-- _class: lead -->

## Swiss AI Center

**Five HES from the HES-SO** (HEIG-VD, HEIA-FR, HE-Arc, HEVS and HEPIA) work on a project called **Centre Suisse d’Intelligence Artificiel à destination des PMEs (CSIA-PME)**, also known as the **Swiss AI Center**.

The Swiss AI Center’s mission is to **accelerate the adoption of artificial intelligence in the digital transition of Swiss SMEs**.

**HEIG-VD** is responsible for **setting up tools to manage ML experiments from code to production**.

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

[Mail](mailto:bertil.chapuis@heig-vd.ch) · [LinkedIn](https://www.linkedin.com/in/bertilchapuis/)

</div>
<div class="center">

**Ludovic  
Delafontaine**  
<small>aR&D Associate</small>

![w:200](./images/ludovic-delafontaine.png)

[Mail](mailto:ludovic.delafontaine@heig-vd.ch) · [LinkedIn](https://www.linkedin.com/in/ludelafo/)

</div>
<div class="center">

**Rémy  
Marquis**  
<small>aR&D Associate</small>

![w:200](./images/remy-marquis.png)

[Mail](mailto:remy.marquis@heig-vd.ch) · [LinkedIn](https://www.linkedin.com/in/remymarquis/)

</div>
<div class="center">

**Leonard  
Cseres**  
<small>Assistant</small>

![w:200](./images/leonard-cseres.png)

[Mail](mailto:leonard.cseres@heig-vd.ch) · [LinkedIn](https://www.linkedin.com/in/leonardcsrs/)

</div>

<div>

## Difficulties with ML projects

**Get out of the context of the experience**

> I ran the experiment but didn’t get the same results, can you check my way of running the experiment?

<hr>

**Make sure you can build the model at all times**

> I tried to build the model on my machine but it doesn’t work... Are you sure it builds on yours?

---

**Monitor the evolution of the model over time**

> I’m not sure my changes really help the model’s performances… I hope it still works in production.

<hr>

**Move to production quickly, efficiently and in a semi-automated way**

> Is your model available in production? Can I use it with my mobile app/website? How can I do so?

## Small and medium-sized enterprises (SMEs) face the same problems

<!-- _class: lead -->

## A solution

**MLOps**

➡️ Draw inspiration from Software and DevOps best practices

➡️ Adapting these practices to the world of machine learning

➡️ Improve the management and quality of machine learning projects

![bg right:40% 110%](./images/mlops-venn-diagram.svg)

## Our proposal

**A guide to MLOps**

🛠️ Switch from a Jupyter Notebook to production using state-of-the-art MLOps tools

🚀 Go from experience to production on the Cloud

📖 Use the best practices for ML

![bg right:40% 90%](./images/a-guide-to-mlops.png)

## A guide to MLOps

<!-- _class: lead -->

A quick presentation of the guide

## _"Welcome to the team!"_

You just have joined a team of data scientists and machine learning (ML) engineers (_welcome!_).

The team is working on a model capable of visually identifying planets or moons within our solar system from images in a Jupyter Notebook.

The team is facing difficulties to move the model to production.

Your mission is to help the team to improve the model and deploy it to the cloud using MLOps best practices.

---

![bg w:90%](./images/guide-demo-01.png)
![bg w:90%](./images/guide-demo-02.png)

---

![bg w:90%](./images/guide-demo-03.png)
![bg w:90%](./images/guide-demo-04.png)

---

![bg w:90%](./images/guide-demo-05.png)
![bg w:90%](./images/guide-demo-06.png)

---

![bg w:90%](./images/guide-demo-07.png)
![bg w:90%](./images/guide-demo-08.png)

---

![bg w:90%](./images/guide-demo-09.png)
![bg w:90%](./images/guide-demo-10.png)

---

![bg w:90%](./images/guide-demo-11.png)
![bg w:90%](./images/guide-demo-12.png)

---

![bg w:90%](./images/guide-demo-13.png)
![bg w:90%](./images/guide-demo-14.png)

---

![bg w:90%](./images/guide-demo-15.png)
![bg w:90%](./images/guide-demo-16.png)

---

![bg w:90%](./images/guide-demo-17.png)
![bg w:90%](./images/guide-demo-18.png)

### The big picture

![bg w:90%](./images/the-big-picture.png)

## Target audience

🤖 You regularly work with machine learning projects

📊 You want to improve processes to ensure quality

🏗️ You want to consolidate your current infrastructure

☁️ You want to move to the Cloud

![bg right:40% 80%](./images/target-audiance.svg)

## Prerequisites

♿ Accessible to everyone!

🧠 Basic knowledge of Python and terminal is sufficient

💳 A valid credit card for cloud deployment

🤝 You will be accompanied throughout the guide!

![bg right:40% 70%](./images/python-logo.svg)

## Access the guide

👉 Access the guide at
[mlops.swiss-ai-center.ch][website].

💪 Feel free to open an issue on [GitHub][github] if you encounter any difficulties or want to contribute.

🙏 Leave us a star if you like the guide!

![bg right:40% w:60%][website-qrcode]

## Sources

- MLOps Venn diagram by Cmbreuel on [Wikipedia](https://commons.wikimedia.org/wiki/File:ML_Ops_Venn_Diagram.svg)
- Robot illustation by [OpenClipart-Vectors](https://pixabay.com/users/openclipart-vectors-30363/) on [Pixabay](https://pixabay.com/vectors/cartoon-comic-dance-happy-joy-1295224/)
- Python logo by [Python Software Foundation](https://www.python.org/community/logos/) on [Wikipedia](https://commons.wikimedia.org/wiki/File:Python-logo-notext.svg)

## Bonus slides

<!-- _class: lead -->

### Usual ML workflow

Each member of the team manages their own codebase, their own dataset and their own models.

The reproducibility of the model creation is difficult and cannot be guaranteed over time.

Improvements made to the model are hard to track.

Models are hard to share and deploy in production.

### High flexibility for the team...

<!-- _class: lead -->

...but hard to maintain.

...hard to reproduce in the future.

...time consuming.

**We can do better.**

### Codebase

**Current situation**

- Each developer has its own codebase
- Sharing the code with peers is difficult

![bg right:40%](.)

---

**What are we trying to improve**

- Allow each developer to improve a common codebase
- Quickly benefit of the work from others

![bg right:40%](.)

### Data

**Current situation**

- The dataset must be manually downloaded and put in the right place
- Different datasets are in used at the same time
- Datasets are hard to improve

![bg right:40%](.)

---

**What are we trying to improve**

- Allow the usage of a common and up-to-date dataset
- Efficiently share new revisions to train the model
- Datasets can be stored anywhere

![bg right:40%](.)

### Reproduce

**Current situation**

- Steps to create the model can be complex
- Intermediate commands should not be skipped
- Hyperparameters are hard to track from one run to another

![bg right:40%](.)

---

**What are we trying to improve**

- Document the  steps to reproduce the experiment
- Ensure it can be ran anytime in the future
- DVC can improve time efficiency

![bg right:40%](.)

### Tracking

### Serving and publishing

### Deployment

### Storage

### Orchestration