---
title: "A guide to MLOps"
---

# {% $markdoc.frontmatter.title %}

## Introduction & Problematic

This guide will help you through incremental steps from a traditional approach of managing ML projects to a modern ML Ops approach designed to improve team collaboration and reproductibility.

It will try to address the following issues that are common to most ML projects:

- The codebase must be downloaded and set up locally in order to run the experiment (what happens if another member of the team updates the codebase?).
- The dataset must be downloaded and placed in the right directory in order to run the experiment (what if another member of the team uses a newer version of the dataset than us?).
- The steps used to create the model can be forgotten (what happens if I forget to prepare the dataset when I get a newer version of the dataset before training?).
- It is hard to see if changes made to the codebase actually improve the model's performance (what if my changes degrade the performance of my model instead of improving it?).
- It is hard to work as a team (how can we collaborate effectively on the same problem to solve?).
- It is hard to share the model with others (I now have a model, how can others use it?).
- How to improve our datasets individually or as a team (what if I would like to annotate the dataset in order to improve the model's performance?).
- Link the model to get interactive predictions in our annotation process (for complexe datasets, can the model help me to annotate the datasets and see where the current model has flows?).
- Retrain the model with our improvements (I now have improved my dataset and code, can I easily retrain the model to a better version?).

In this context and for the rest of the guide, an _experiment_ is a ML learning project.

We chose the term _experiment_ to address the experimental nature of the machine learning field before finding a suitable model.

It has been written using many different sources that will be mentioned in each step of the process.

## Get started

Not sure where to start? Check the following links to get started!

- [What is MLOps?](/get-started/what-is-mlops)
- [What problems is MLOps trying to solve?](/get-started/what-problems-is-mlops-trying-to-solve)
- [Why would MLOps be useful for me?](/get-started/why-would-mlops-be-useful-for-me)
- [Start the guide](#the-guide)

## The guide

- [Step 1: Run a simple ML experiment](/the-guide/step-1-run-a-simple-ml-experiment)
- [Step 2: Share your ML experiment code with Git](/the-guide/step-2-share-your-ml-experiment-code-with-git)
- [Step 3: Share your ML experiment data with DVC](/the-guide/step-3-share-your-ml-experiment-data-with-dvc)
- [Step 4: Reproduce the experiment with DVC](/the-guide/step-4-reproduce-the-experiment-with-dvc)
- [Step 5: Track model evolutions with DVC](/the-guide/step-5-track-model-evolutions-with-dvc)
- [Step 6: Orchestrate the workflow with a CI/CD pipeline](/the-guide/step-6-orchestrate-the-workflow-with-a-cicd-pipeline)
- [Step 7: Visualize model evolutions with CML](/the-guide/step-7-visualize-model-evolutions-with-cml)
- [Step 8: Share and deploy model with MLEM](/the-guide/step-8-share-and-deploy-model-with-mlem)

## Label Studio

- [Introduction](/label-studio/introduction)
- [Create a Label Studio project](/label-studio/create-a-label-studio-project)
- [Convert and import existing data to Label Studio](/label-studio/convert-and-import-existing-data-to-label-studio)
- [Annotate new data with Label Studio](/label-studio/annotate-new-data-with-label-studio)
- [Export data from Label Studio](/label-studio/export-data-from-label-studio)

## Advanced concepts

- [Deploy MinIO](/advanced-concepts/deploy-minio)
- [Deploy Label Studio](/advanced-concepts/deploy-label-studio)
- [Link your ML model with Label Studio](/advanced-concepts/link-your-ml-model-with-label-studio)
- [Train the model on a Kubernetes cluster with CML](/advanced-concept)
