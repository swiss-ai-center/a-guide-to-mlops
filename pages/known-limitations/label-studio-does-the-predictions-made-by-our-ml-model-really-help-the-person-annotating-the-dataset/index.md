---
title: "Label Studio: Does the predictions made by our ML model really help the person annotating the dataset"
---

# {% $markdoc.frontmatter.title %}

## Does the predictions made by our ML model really help the person annotating the dataset

## Observations

Label Studio can be configured to get predictions from a ML backend. These predictions can help the person annotating the dataset.

## Implications

As the model helps the person annotating the dataset in order to improve this very specific model, we have concerns about the certainty of the process. It is not impossible that the expert is too influenced by the predictions of the model (by automatism of the process, by excessive confidence in it) and that this leads to a degradation of the performance of the model compared to an absence of annotation assistance.

## Ideas considered

Make an experiment consisted of two groups of people that have to annotate a dataset to improve the performance of the model. One group has to annotate the dataset with the help of the model's predictions and the other without the help of the model's predictions. See the group that improves the model's performance the best.
