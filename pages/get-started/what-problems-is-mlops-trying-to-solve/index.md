---
title: "What problems is MLOps trying to solve?"
---

# {% $markdoc.frontmatter.title %}

The problems described in this document are based of our own expericences with ML projects/experiments. They might not reflect all projects and/or teams but we tried to regroup the identified issues in major categories.


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


## The problems

### The codebase still needs to be downloaded and set up locally in order to run the experiment

When a new member of a ML teams

### The dataset still needs to be downloaded and placed in the right directory in order to run the experiment

### The steps used to create the model can be forgotten

### The changes done to a model cannot be visualized and improvements and/or deteriorations are hard to identify

### There is no guarantee that the experiment can be executed on another machine

### The model might have required artifacts that can be forgotten or omitted when saving/loading the model for future usage. There is no easy way to use the model outside of the experiment context

## Next

- [Why would MLOps be useful for me?](/get-started/why-would-mlops-be-useful-for-me)
- [The guide - Introduction](/the-guide/introduction)
