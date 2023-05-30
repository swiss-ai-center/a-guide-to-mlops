# A guide to MLOps

We are a team of software engineers and data scientists at the [Centre Suisse d'Intelligence Artificiel à destination des PMEs (CSIA-PME)](https://swiss-ai-center.ch/){:target="\_blank"} who are passionate about Machine Learning (ML) and DevOps.

In this context, we have been working on the redaction of this guide to help you take your ML projects from experiment to production with ease.

We did try to find and use the tools that cause the less friction in established workflows and teams.

During this guide, you will setup a project that you will manage from a traditional approach to a modern MLOps approach designed to improve team collaboration and reproducibility.

The guide is written in a way that you can follow it step by step. It has been written using many different sources that will be mentioned in each step of the process. It is a mix between a tutorial and a course.

The guide is split into 6 parts:

- [Introduction](./introduction/index.md) - Learn about MLOps and the tools used in this guide.
- [Part 1 - Local training and model evaluation](./part-1-local-training-and-model-evaluation/index.md) - Learn how to train a model locally and evaluate it using DVC.
    - [Chapter 1 - Run a simple ML experiment with Jupyter Notebook](./part-1-local-training-and-model-evaluation/chapter-1-run-a-simple-ml-experiment-with-jupyter-notebook/index.md)
    - [Chapter 2 - Adapt and move the Jupyter Notebook to Python scripts](./part-1-local-training-and-model-evaluation/chapter-2-adapt-and-move-the-jupyter-notebook-to-python-scripts/index.md)
    - [Chapter 3 - Initialize Git and DVC for local training](./part-1-local-training-and-model-evaluation/chapter-3-initialize-git-and-dvc-for-local-training/index.md)
    - [Chapter 4 - Reproduce the ML experiment with DVC](./part-1-local-training-and-model-evaluation/chapter-4-reproduce-the-ml-experiment-with-dvc/index.md)
    - [Chapter 5 - Track model evolution with DVC](./part-1-local-training-and-model-evaluation/chapter-5-track-model-evolution-with-dvc/index.md)
- [Part 2 - Collaborate online in the cloud](./part-2-collaborate-online-in-the-cloud/index.md) - Learn how to collaborate online using Git, a CI/CD pipeline and CML.
    - [Chapter 6 - Move the ML experiment data to the cloud](./part-2-move-to-the-cloud/chapter-6-move-the-ml-experiment-data-to-the-cloud/index.md)
    - [Chapter 7 - Move the ML experiment code to the cloud](./part-2-move-to-the-cloud/chapter-7-move-the-ml-experiment-code-to-the-cloud/index.md)
    - [Chapter 8 - Reproduce the ML experiment in a CI/CD pipeline](./part-2-move-to-the-cloud/chapter-8-reproduce-the-ml-experiment-in-a-cicd-pipeline/index.md)
    - [Chapter 9 - Track model evolution in the CI/CD pipeline with CML](./part-2-move-to-the-cloud/chapter-9-track-model-evolution-in-the-cicd-pipeline-with-cml/index.md)
- [Part 3 - Serve and deploy the model online](./part-3-serve-and-deploy-the-model-online/index.md) - Learn how to serve and deploy the model online using MLEM and CML.
    - [Chapter 10 - Save and load the model with MLEM](./part-3-serve-and-deploy-the-model-online/chapter-10-save-and-load-the-model-with-mlem/index.md)
    - [Chapter 11 - Serve the model locally with MLEM](./part-3-serve-and-deploy-the-model-online/chapter-11-serve-the-model-locally-with-mlem/index.md)
    - [Chapter 12 - Deploy and access the model on Kubernetes with MLEM](./part-3-serve-and-deploy-the-model-online/chapter-12-deploy-and-access-the-model-on-kubernetes-with-mlem/index.md)
    - [Chapter 13 - Train the model on a Kubernetes pod with CML](./part-3-serve-and-deploy-the-model-online/chapter-13-train-the-model-on-a-kubernetes-pod-with-cml/index.md)
- [Part 4 - Labeling new data and retrain the model](./part-4-labeling-new-data-and-retrain-the-model/index.md) - Learn how to label new data and retrain the model using Label Studio.
    - [Chapter 14 - Setup Label Studio](./part-4-labeling-the-data-and-retrain/chapter-14-setup-label-studio/index.md)
    - [Chapter 15 - Import existing data to Label Studio](./part-4-labeling-the-data-and-retrain/chapter-15-import-existing-data-to-label-studio/index.md)
    - [Chapter 16 - Label new data with Label Studio](./part-4-labeling-the-data-and-retrain/chapter-16-label-new-data-with-label-studio/index.md)
    - [Chapter 17 - Retrain the model from new data with DVC Sync](./part-4-labeling-the-data-and-retrain/chapter-17-retrain-the-model-from-new-data-with-dvc-sync/index.md)
    - [Chapter 18 - Link the model to Label Studio and get predictions](./part-4-labeling-the-data-and-retrain/chapter-18-link-the-model-to-label-studio-and-get-predictions/index.md)
      
- [Conclusion](./conclusion/index.md) - Conclusion and summary of what you have done and what is left to be done.

This guide is available on [GitHub](https://github.com/csia-pme/a-guide-to-mlops). Feel free to star us or open an issue if you have any problems. :)
