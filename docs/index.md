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
        Ground control, reporting for duty. We are the
        <a href="https://www.swiss-ai-center.ch/" class="crew-link" target="_blank" rel="noopener">Swiss AI Center</a>
        crew, building a practical flight plan from machine-learning experiments to production.
        We selected tools that minimize friction for established workflows and teams, with a focus on SMEs.
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
        Building a model is only the beginning. This guide is a step-by-step flight plan
        from a notebook experiment to a reproducible, monitored, and continuously-improved ML system.
        We use real tools — DVC, CML, Docker, BentoML, Evidently AI, and Label Studio —
        so you can follow along with real code.
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
        Start on solid ground. Move from a Jupyter notebook experiment to clean
        Python scripts, then version your data and code with Git and DVC. Build a
        reproducible prepare-train-evaluate pipeline on your own machine, and use
        DVC to track parameters, metrics, and plots as your model evolves.
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
        When your local machine is no longer enough, move the experiment to the
        cloud. Push your code to GitHub, store data in an S3 bucket with DVC, and
        set up a CI/CD pipeline that reproduces the experiment on every push. Then
        use CML to publish comparisons of parameters, metrics, and plots in pull
        requests so the team can review every change.
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
        A trained model creates value only when it serves predictions. Package it
        with BentoML and expose a local FastAPI endpoint, then containerize it with
        Docker and push the image to a registry. Wire builds and deployments into
        your CI/CD pipeline, roll the model out on Kubernetes, and scale training
        with self-hosted runners that spin up specialized pods on demand.
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
        A model in production needs watching. Stream prediction logs to S3, deploy
        an Evidently AI dashboard on Kubernetes to compare live data against your
        training reference, and open drift reports as GitHub issues when data drifts.
        Use those signals to trigger retraining workflows or roll back to a previous
        model version by redeploying its container image, with Git and DVC as the
        reproducible source of truth.
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
        Production data changes. Close the feedback loop with Label Studio: let
        your model suggest labels through the FastAPI endpoint, review and correct
        edge cases, then merge the refined annotations and retrain with DVC. A
        better model makes the next round of labeling faster and more accurate.
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
        Finish the journey by cleaning up everything you created. Delete cloud
        resources, remove the GitHub repository and access tokens, wipe your local
        environment, and review what you built. A proper cleanup avoids unexpected
        costs. A safe landing is the final stage of a successful mission.
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
      Pick a chapter, launch your terminal, and start shipping ML systems.
    cta:
      text: Start the journey
      icon: lucide/rocket
      path: syllabus/
---
