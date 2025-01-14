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
footer: '**Swiss AI Center** - A guide to MLOps 2025 - CC BY-SA 4.0'
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

## About us

<!-- _class: lead -->

## Swiss AI Center

**Five HES from the HES-SO** (HEIG-VD, HEIA-FR, HE-Arc, HEVS and HEPIA) work on
a project called **Centre Suisse d’Intelligence Artificiel à destination des
PMEs (CSIA-PME)**, also known as the **Swiss AI Center**.

The Swiss AI Center’s mission is to **accelerate the adoption of artificial
intelligence in the digital transition of Swiss SMEs**.

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

[Mail](mailto:bertil.chapuis@heig-vd.ch) ·
[LinkedIn](https://www.linkedin.com/in/bertilchapuis/)

</div>
<div class="center">

**Ludovic
Delafontaine**
<small>aR&D Associate</small>

![w:200](./images/ludovic-delafontaine.png)

[Mail](mailto:ludovic.delafontaine@heig-vd.ch) ·
[LinkedIn](https://www.linkedin.com/in/ludelafo/)

</div>
<div class="center">

**Rémy
Marquis**
<small>aR&D Associate</small>

![w:200](./images/remy-marquis.png)

[Mail](mailto:remy.marquis@heig-vd.ch) ·
[LinkedIn](https://www.linkedin.com/in/remymarquis/)

</div>
<div class="center">

**Leonard
Cseres**
<small>Assistant</small>

![w:200](./images/leonard-cseres.png)

[Mail](mailto:leonard.cseres@heig-vd.ch) ·
[LinkedIn](https://www.linkedin.com/in/leonardcsrs/)

</div>
</div>
