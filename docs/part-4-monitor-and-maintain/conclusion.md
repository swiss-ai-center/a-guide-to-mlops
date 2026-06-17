---
title: "Part 4 - Conclusion"
---

# Conclusion

!!! warning

    This part of the guide is a work in progress. The conclusion will summarize the
    monitoring and maintenance practices introduced in this part once the content is
    written.

Part 5 is an improvement of the MLOps process. You will learn how to label new
data and retrain the model using Label Studio.

## Next steps

**Ready to continue?**

Proceed to
[Part 5 - Label data and retrain](../part-5-label-data-and-retrain/introduction.md)
to learn how to systematically label new data and continuously improve your
model.

**Stopping here?**

If you decide to conclude your progress at this point, see the
[Clean up guide](../clean-up.md) for instructions on removing the resources you
created:

- Local Git repository and DVC cache
- Python virtual environment
- Cloud storage bucket (S3/GCS)
- Container registry and Docker images
- Kubernetes cluster and deployments
- CI/CD pipeline configurations
- Self-hosted runners (if configured)

This is necessary to return to a clean state on your computer, avoid unnecessary
incurring costs, and address potential security concerns when using cloud
services.

!!! note

    Part 5 (data labeling) works entirely locally and doesn't require cloud
    infrastructure. If you're continuing to Part 5, you can
    **Clean up cloud resources** (delete your Kubernetes cluster, container
    registry, and cloud storage) to avoid costs but keep your local resources (local
    Git repository, DVC cache, and data files) as they are needed for the next
    section.

    You can safely skip cleanup if you plan to continue with the next part
    immediately, but we strongly recommend stopping the **Kubernetes cluster** to
    avoid unnecessary costs.
