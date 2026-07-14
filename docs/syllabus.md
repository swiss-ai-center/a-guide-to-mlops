# Syllabus

What you will learn.

This hands-on tutorial walks through the full MLOps lifecycle: from a local
Jupyter notebook experiment to a reproducible pipeline, then to automated
collaboration in the cloud, and finally to a deployed, monitored, and
retrainable system.

The five parts are:

- Introduction - Learn about the [concept](./concept.md) behind MLOps, the
  [philosophy](./philosophy.md), and the [tools](./tools.md) used throughout.
- [Part 1 - Local training and evaluation](./part-1-local-training-and-evaluation/introduction.md) -
  Learn how to train a model locally and evaluate it using DVC.
    - [Chapter 1.1 - Run a simple ML experiment with Jupyter Notebook](./part-1-local-training-and-evaluation/chapter-11-run-a-simple-ml-experiment-with-jupyter-notebook.md)
    - [Chapter 1.2 - Adapt and move the Jupyter Notebook to Python scripts](./part-1-local-training-and-evaluation/chapter-12-adapt-and-move-the-jupyter-notebook-to-python-scripts.md)
    - [Chapter 1.3 - Initialize Git and DVC for local training](./part-1-local-training-and-evaluation/chapter-13-initialize-git-and-dvc-for-local-training.md)
    - [Chapter 1.4 - Reproduce the ML experiment with DVC](./part-1-local-training-and-evaluation/chapter-14-reproduce-the-ml-experiment-with-dvc.md)
    - [Chapter 1.5 - Track model evolution with DVC](./part-1-local-training-and-evaluation/chapter-15-track-model-evolution-with-dvc.md)
- [Part 2 - Move to the cloud](./part-2-move-to-the-cloud/introduction.md) -
  Learn how to collaborate online using Git, a CI/CD pipeline and CML.
    - [Chapter 2.1 - Move the ML experiment data to the cloud](./part-2-move-to-the-cloud/chapter-21-move-the-ml-experiment-code-to-the-cloud.md)
    - [Chapter 2.2 - Move the ML experiment code to the cloud](./part-2-move-to-the-cloud/chapter-22-move-the-ml-experiment-data-to-the-cloud.md)
    - [Chapter 2.3 - Reproduce the ML experiment in a CI/CD pipeline](./part-2-move-to-the-cloud/chapter-23-reproduce-the-ml-experiment-in-a-cicd-pipeline.md)
    - [Chapter 2.4 - Track model evolution in the CI/CD pipeline with CML](./part-2-move-to-the-cloud/chapter-24-track-model-evolution-in-the-cicd-pipeline-with-cml.md)
    - [Chapter 2.5 - Work efficiently and collaboratively with Git](./part-2-move-to-the-cloud/chapter-25-work-efficiently-and-collaboratively-with-git.md)
- [Part 3 - Serve and deploy](./part-3-serve-and-deploy/introduction.md) - Learn
  how to serve and deploy the model using BentoML and Docker.
    - [Chapter 3.1 - Save and load the model with BentoML](./part-3-serve-and-deploy/chapter-31-save-and-load-the-model-with-bentoml.md)
    - [Chapter 3.2 - Serve the model locally with BentoML](./part-3-serve-and-deploy/chapter-32-serve-the-model-locally-with-bentoml.md)
    - [Chapter 3.3 - Build and publish the model with BentoML and Docker locally](./part-3-serve-and-deploy/chapter-33-build-and-publish-the-model-with-bentoml-and-docker-locally.md)
    - [Chapter 3.4 - Build and publish the model with BentoML and Docker in the CI/CD pipeline](./part-3-serve-and-deploy/chapter-34-build-and-publish-the-model-with-bentoml-and-docker-with-the-cicd-pipeline.md)
    - [Chapter 3.5 - Deploy and access the model on Kubernetes](./part-3-serve-and-deploy/chapter-35-deploy-and-access-the-model-on-kubernetes.md)
    - [Chapter 3.6 - Continuous deployment of the model with the CI/CD pipeline](./part-3-serve-and-deploy/chapter-36-continuous-deployment-of-the-model-with-the-cicd-pipeline.md)
    - [Chapter 3.7 - Use a self-hosted runner for the CI/CD pipeline](./part-3-serve-and-deploy/chapter-37-use-a-self-hosted-runner-for-the-cicd-pipeline.md)
    - [Chapter 3.8 - Train the model on a Kubernetes pod](./part-3-serve-and-deploy/chapter-38-train-the-model-on-a-kubernetes-pod.md)
- [Part 4 - Monitor and maintain](./part-4-monitor-and-maintain/introduction.md) -
  Learn how to keep a model healthy in production using Evidently AI.
    - [Chapter 4.1 - Log predictions and features locally](./part-4-monitor-and-maintain/chapter-41-log-predictions-and-features-locally.md)
    - [Chapter 4.2 - Detect drift locally with Evidently AI](./part-4-monitor-and-maintain/chapter-42-detect-drift-locally-with-evidently-ai.md)
    - [Chapter 4.3 - Deploy and access the monitoring on Kubernetes](./part-4-monitor-and-maintain/chapter-43-deploy-and-access-the-monitoring-on-kubernetes.md)
    - [Chapter 4.4 - Trigger drift alerts with the CI/CD workflow](./part-4-monitor-and-maintain/chapter-44-trigger-drift-alerts-with-the-cicd-workflow.md)
    - [Chapter 4.5 - Review drift alerts and decide on action](./part-4-monitor-and-maintain/chapter-45-review-drift-alerts-and-decide-on-action.md)
- [Part 5 - Label data and retrain](./part-5-label-data-and-retrain/introduction.md) -
  Learn how to label new data and retrain the model using Label Studio.
    - [Chapter 5.1 - Set up Label Studio](./part-5-label-data-and-retrain/chapter-51-set-up-label-studio.md)
    - [Chapter 5.2 - Label new data with Label Studio](./part-5-label-data-and-retrain/chapter-52-label-new-data-with-label-studio.md)
    - [Chapter 5.3 - Link the model to Label Studio](./part-5-label-data-and-retrain/chapter-53-link-the-model-to-label-studio.md)
    - [Chapter 5.4 - Retrain the model from new data with DVC](./part-5-label-data-and-retrain/chapter-54-retrain-the-model-from-new-data-with-dvc.md)
- [Conclusion](./conclusion.md) - Summary of what you have done and what is left
  to be done.
