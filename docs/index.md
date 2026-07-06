---
template: home.html
title: MLOps Guide — Complete Tutorial on Machine Learning Operations
description: Complete MLOps tutorial covering tools and best practices for deploying ML models in production
hide:
  - navigation
  - toc
home:
  hero:
    badge:
      text: Hands-on tutorial
    title: A Guide to MLOps
    subtitle: |
      Classify celestial bodies with MLOps best practices:
      a journey through local training, the cloud, serving, monitoring, labeling, and retraining.
    cta:
      text: Chart the course
      icon: lucide/compass
      anchor: "#story-start"
  chapters:
    - id: about
      label: Ground control
      prefix: Prologue
      title: Meet the
      title_highlight: Crew
      body: |
        We are the
        <a href="https://www.swiss-ai-center.ch/" class="crew-link" target="_blank" rel="noopener">Swiss AI Center</a>
        team. This guide is a practical path from notebook experiments to production,
        built for engineers and small teams. We selected tools that minimize friction for
        established workflows, with a focus on SMEs.
      actions:
        - type: primary
          text: Next stop
          icon: lucide/chevron-down
          anchor: "#section-intro"
        - type: secondary
          text: Presentation
          icon: lucide/monitor
          url: "https://mlops.swiss-ai-center.ch/presentation/"
        - type: pdf
          text: PDF
          icon: lucide/file-text
          url: "https://mlops.swiss-ai-center.ch/presentation/a-guide-to-mlops-presentation.pdf"
    - id: intro
      label: Mission briefing
      prefix: Introduction
      title: Why this
      title_highlight: "guide?"
      planet: moon
      body: |
        A step-by-step path from a notebook experiment to a reproducible, monitored,
        continuously-improved ML system. You will use the same tools as in production:
        DVC, Git, GitHub Actions, CML, Docker, BentoML, Fluent Bit, Evidently AI, and Label Studio.
      actions:
        - type: primary
          text: Next stop
          icon: lucide/chevron-down
          anchor: "#section-part-1"
        - type: secondary
          text: Philosophy
          icon: lucide/lightbulb
          path: philosophy/
    - id: part-1
      label: Lift-off
      prefix: Part 1
      title: Local training &
      title_highlight: model evaluation
      planet: earth
      body: |
        Move from a notebook to clean, versioned Python scripts. Build a reproducible
        prepare-train-evaluate pipeline on your own machine, and use Git and DVC to track
        data, parameters, metrics, and plots as the model evolves.
      actions:
        - type: primary
          text: Next stop
          icon: lucide/chevron-down
          anchor: "#section-part-2"
        - type: secondary
          text: Train locally
          icon: lucide/flask-conical
          path: part-1-local-training-and-evaluation/introduction/
    - id: part-2
      label: Escape velocity
      prefix: Part 2
      title: Move the model to the
      title_highlight: cloud
      planet: mars
      body: |
        Push the experiment to GitHub, store data in an S3 bucket with DVC, and set up a
        CI/CD pipeline that reproduces the run on every push. Use CML to publish parameter,
        metric, and plot comparisons directly in pull requests for team review.
      actions:
        - type: primary
          text: Next stop
          icon: lucide/chevron-down
          anchor: "#section-part-3"
        - type: secondary
          text: Go cloud
          icon: lucide/cloud
          path: part-2-move-to-the-cloud/introduction/
    - id: part-3
      label: In orbit
      prefix: Part 3
      title: Serve &
      title_highlight: deploy
      planet: saturn
      body: |
        Package the model with BentoML, expose a FastAPI endpoint, and containerize it
        with Docker. Push the image to a registry, wire builds and deployments into your
        CI/CD pipeline, and roll the model out on Kubernetes with self-hosted runners for
        specialized training pods.
      actions:
        - type: primary
          text: Next stop
          icon: lucide/chevron-down
          anchor: "#section-part-4"
        - type: secondary
          text: Deploy
          icon: lucide/server
          path: part-3-serve-and-deploy/introduction/
    - id: part-4
      label: Sensor array
      prefix: Part 4
      title: Monitor &
      title_highlight: maintain
      planet: comet
      body: |
        Stream prediction logs to S3 with Fluent Bit and deploy an Evidently AI dashboard
        on Kubernetes to compare live data against the training reference. Open drift reports
        as GitHub issues so the team can decide whether to retrain or roll back by redeploying
        a previous container image tracked in Git and DVC.
      actions:
        - type: primary
          text: Next stop
          icon: lucide/chevron-down
          anchor: "#section-part-5"
        - type: secondary
          text: Observe
          icon: lucide/activity
          path: part-4-monitor-and-maintain/introduction/
    - id: part-5
      label: Deep space loop
      prefix: Part 5
      title: Label data &
      title_highlight: retrain
      planet: haumea
      body: |
        Close the feedback loop with Label Studio. Let the model suggest labels through
        the FastAPI endpoint, review and correct edge cases, then merge the refined
        annotations and retrain with DVC. A better model makes the next round of labeling
        faster and more accurate.
      actions:
        - type: primary
          text: Next stop
          icon: lucide/chevron-down
          anchor: "#section-reentry"
        - type: secondary
          text: Retrain
          icon: lucide/tags
          path: part-5-label-data-and-retrain/introduction/
    - id: reentry
      label: Reentry
      prefix: Conclusion
      title: Clean up &
      title_highlight: conclude
      planet: capsule
      reentry: true
      body: |
        Delete cloud resources, remove the GitHub repository and access tokens, and wipe
        the local environment. A proper cleanup avoids unexpected costs and is the final
        stage of a successful mission.
      actions:
        - type: primary
          text: Launch pad
          icon: lucide/chevron-down
          anchor: "#story-finale"
        - type: secondary
          text: Clean up
          icon: lucide/brush
          path: clean-up/
  finale:
    title: Ready for
    title_highlight: launch?
    subtitle: |
      The guide is open source and designed to be followed hands-on.
      Pick a part, open your terminal, and ship a complete ML system.
    cta:
      text: Launch mission
      icon: lucide/rocket
      path: syllabus/
---
