---
title: "Conclusion"
---

# {% $markdoc.frontmatter.title %}

Congratulations! You did it! You were able to convert a ML experiment with a traditional approach to a well-defined, well-documented workflow that can scale and serve a model to the outside world! Let's take the time to make a summary of what you have done.

## Summary of what you have done

### The codebase can be shared among the developers

Thanks to Git, the codebase can be shared and improved collectively among the developers.

### The dataset can be shared among the developers

Thanks to DVC, the dataset can be shared and improved collectively among the developers.

### The model can be reproduced

Thanks to DVC, the steps to create the model are documented and can be executed in order to reproduce the model.

### The experiment can be executed on a clean machine

Thanks to the CI/CD pipeline, the experiment can be executed on a clean machine. Erasing the "but it works on my machine" issue.

### The changes done to a model can be tracked

Thanks to DVC and CML, the changes done to a model can be tracked, discussed and visualized before merging them.

### The model can be used outside of the experiment context

Thanks to MLEM, the model can be served and be used outside of the experiment context.

## What is left to be done?

Distribution and deployment of the model is out of scope for this guide. However, MLEM greatly helps for this aspect. Check out the [_Building models_ - mlem.ai](https://mlem.ai/doc/user-guide/building) and [_Deploying models_ - mlem.ai](https://mlem.ai/doc/user-guide/deploying) guides for more details.

## End of your journey

Thank you for staying with us! We hope you had a great time following this guide. We have advanced concepts and labelization topics that might interest you. Check out the left sidebar for more content regarding MLOps! Please contact us on [GitHub](https://github.com/csia-pme/a-guide-to-mlops) if you have any issues. :)

## Previous step

- **Previous**: [Step 8: Serve the model with MLEM](/the-guide/step-8-serve-the-model-with-mlem)
