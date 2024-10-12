---
title: "Part 4 - Conclusion"
---

# Conclusion

Congratulations! You have successfully completed the fourth part of the guide.
In this part, you learned how to annotate the data using Label Studio using AI
assisted labeling. You finally retrained the model using the newly labeled data.

As you work with your data and model, you may find that certain labels need
refinement or that additional data points require annotation. You can
continuously improve the quality of your labeled dataset, to improve your model
accuracy and effectiveness over time. Based on the model performance feedback,
you can revisite and update the annotations to create a broader and more robust
training set that better meets the needs of your project.

This concludes the guide. We hope you enjoyed it and learned a lot. If you have
any questions or feedback, please feel free to reach out to us on
[GitHub](https://github.com/swiss-ai-center/a-guide-to-mlops).

The final part of the guide will cover cleaning up the resources and
environments you have generated. We strongly recommend to go through the
[Clean up](../clean-up.md) section to ensure the proper removal of the resources
and environments you have generated.

The following diagram illustrates the bricks you set up at the end of this part:

```mermaid
flowchart TB
    extra_data -->|upload| labelStudioTasks
    labelStudioTasks -->|label| labelStudioAnnotations
    bento_model -->|load| fastapi
    labelStudioTasks -->|POST /predict| fastapi
    fastapi --> labelStudioPredictions
    labelStudioPredictions -->|submit| labelStudioAnnotations
    labelStudioAnnotations -->|download| extra_data_annotations
    extra_data_annotations --> |load| parse_annotations
    parse_annotations -->|copy| data_raw
    data_raw -->|dvc repro| bento_model

    subgraph workspaceGraph[WORKSPACE]
        extra_data[extra-data/extra_data]
        extra_data_annotations[extra-data/extra_data/annotations.json]
        bento_model[model/classifier.bentomodel]
        fastapi[src/serve_label_studio.py]
        parse_annotations[scripts/parse_annotations.py]
        data_raw[data/raw]
    end

    subgraph labelStudioGraph[LABEL STUDIO]
        labelStudioTasks[Tasks]
        labelStudioAnnotations[Annotations]
        labelStudioPredictions[Predictions]
    end
```
