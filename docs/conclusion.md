# Conclusion

**Congratulations on completing the entire guide!**

You did it! You were able to convert a ML experiment with a traditional approach
to a well-defined, well-documented workflow that can scale and serve a model to
the outside world! You also learned how to improve the performance of your model
with additional and high-quality data in an iterative manner.

Let's take the time to make a summary of what you have done.

## Summary of what you have done

- [x] The codebase can be shared among the developers

Thanks to Git, the codebase can be shared and improved collectively among the
developers.

- [x] The dataset can be shared among the developers

Thanks to DVC, the dataset can be shared and improved collectively among the
developers.

- [x] The model can be reproduced

Thanks to DVC, the steps to create the model are documented and can be executed
in order to reproduce the model.

- [x] The experiment can be executed on a clean machine

Thanks to the CI/CD pipeline, the experiment can be executed on a clean machine.
Erasing the "but it works on my machine" issue.

- [x]  The changes done to a model can be tracked

Thanks to DVC and CML, the changes done to a model can be tracked, discussed and
visualized before merging them.

- [x] The model can be used outside of the experiment context

Thanks to BentoML, the model can be served and be used outside of the experiment
context.

- [x] The model can be deployed and accessed on Kubernetes

Thanks to BentoML, the model can be deployed and be accessed on a Kubernetes
server.

- [x] The model can be trained on a Kubernetes pod

Thanks to a self-hosted runner, the model can be trained on specialized hardware
on a Kubernetes pod.

- [x] The model performance can be improved by retraining with additional data.

Thanks to Label Studio, additional and high-quality training data can be used to
retrain the model.

!!! abstract "Take away"

    - **MLOps is about connecting the pieces, not perfecting each one**: The true
      value of MLOps doesn't come from mastering any single tool like Git, DVC, or
      Kubernetes. It comes from building automated pipelines that connect version
      control, data management, training, deployment, and monitoring into a cohesive
      workflow where changes flow smoothly from experimentation to production.
    - **Automation enables iteration, iteration enables improvement**: By automating
      repetitive tasks like model training, containerization, and deployment through
      CI/CD pipelines, you free up time and mental energy to focus on what actually
      improves models (better features, more data, architectural experiments) creating
      a flywheel where each iteration becomes easier and faster than the last.
    - **Reproducibility is a prerequisite for collaboration and debugging**: When
      models fail in production or performance degrades, the ability to trace back to
      exact code versions, data snapshots, hyperparameters, and dependencies (through
      Git, DVC, and containerization) transforms debugging from guesswork into
      systematic investigation, and enables teams to work together without stepping on
      each other's toes.
    - **Production readiness requires thinking beyond accuracy metrics**: A model
      that achieves 95% accuracy in a notebook but lacks proper serving
      infrastructure, monitoring, rollback capabilities, and retraining workflows is
      less valuable than an 85% accurate model deployed in a robust MLOps system,
      because the latter can be continuously improved while reliably serving users,
      while the former remains stuck in development limbo.

## End of your journey

You've built a complete MLOps workflow from local experimentation to production
deployment on Kubernetes, with continuous improvement through systematic data
labeling. You now have the skills to:

- Version control code, data, and models
- Automate training and deployment with CI/CD
- Serve models in production with monitoring
- Continuously improve models with new labeled data

We trust that you found this guide both enjoyable and informative. We encourage
you to explore the [additional MLOps-related resources](references.md) that we
believe might further enhance your understanding and skills in this rapidly
evolving and increasingly important field.

If you encounter any difficulties, please don't hesitate to reach out to us on
[GitHub](https://github.com/swiss-ai-center/a-guide-to-mlops).

Additionally, if you found our MLOps guide valuable, we would be grateful if you
could take a moment to star our GitHub repository. Your support helps us improve
and expand our offerings for the community. Thank you!

Happy learning! :)
