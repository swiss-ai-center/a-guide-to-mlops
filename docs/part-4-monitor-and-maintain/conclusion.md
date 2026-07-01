---
title: "Part 4 - Conclusion"
---

# Conclusion

Congratulations! You did it!

In this fourth part, you made the model observable in production. Predictions
and features are logged by the BentoML service and shipped to your S3 storage by
Fluent Bit, drift is detected by comparing these production logs against a
reference dataset with Evidently AI, and dashboards are accessible on
Kubernetes. A GitHub Actions workflow refreshes the drift report from production
logs and raises alerts.

The monitoring feedback loop is now closed: production predictions are compared
to the training distribution, abnormal behavior is surfaced to the team, and you
can decide what action to take.

The following diagram illustrates the bricks you set up at the end of this part:

```mermaid
flowchart TB
    dot_dvc[(.dvc)] <-->|dvc pull
                         dvc push| s3_storage[(S3 Storage)]
    dot_git[(.git)] <-->|git pull
                         git push| repository[(Repository)]
    workspaceGraph <-....-> dot_git
    data[data/raw]

    subgraph cacheGraph[CACHE]
        dot_dvc
        dot_git
    end

    subgraph workspaceGraph[WORKSPACE]
        dvcGraph --> bento_model[classifier.bentomodel]
        subgraph bentoGraph[bentofile.yaml]
            bento_model --> serve[serve.py]
            features[features.py] --> serve
        end
        serve --> drift_logs["logs/…/data/*.log"]
        bento_model <-.-> dot_dvc

        data --> prepare
        params[params.yaml] -.- prepare
        subgraph dvcGraph["dvc.yaml"]
            prepare --> train
            train --> evaluate
            train --> build_reference
        end
        params -.- train
        build_reference --> reference_features[reference_features.parquet]
    end

    subgraph remoteGraph[REMOTE]
        s3_storage
        subgraph gitGraph[Git Remote]
            repository[(Repository)] <--> action[Action]
            issue[Drift alert issue] --> repository
        end
        action --> registry
        s3_storage --> action
        subgraph clusterGraph[Kubernetes]
            subgraph clusterPodGraph[Pod]
                pod_train[Train model]
            end
            pod_runner[Runner] --> clusterPodGraph
            bento_service_cluster[classifier.bentomodel] --> k8s_fastapi[FastAPI]
            evidently_ui[Evidently UI] --> dashboard[Dashboard]
        end
        action --> pod_runner
        pod_train --> s3_storage

        registry[(Container
                  registry)] --> bento_service_cluster
    end

    drift_logs -.->|Fluent Bit| s3_storage
    s3_storage -->|monitor workflow| action
    action -->|report| evidently_ui
    action -->|alert| issue

    subgraph browserGraph[BROWSER]
        k8s_fastapi <--> publicURL["public URL"]
        dashboard <--> dashboardURL["dashboard URL"]
    end

    style workspaceGraph opacity:0.4,color:#7f7f7f80
    style cacheGraph opacity:0.4,color:#7f7f7f80
    style remoteGraph opacity:0.4,color:#7f7f7f80
    style gitGraph opacity:0.4,color:#7f7f7f80
    style clusterGraph opacity:0.4,color:#7f7f7f80
    style clusterPodGraph opacity:0.4,color:#7f7f7f80
    style browserGraph opacity:0.4,color:#7f7f7f80
    style params opacity:0.4,color:#7f7f7f80
    style data opacity:0.4,color:#7f7f7f80
    style prepare opacity:0.4,color:#7f7f7f80
    style train opacity:0.4,color:#7f7f7f80
    style evaluate opacity:0.4,color:#7f7f7f80
    style build_reference opacity:0.4,color:#7f7f7f80
    style dvcGraph opacity:0.4,color:#7f7f7f80
    style bentoGraph opacity:0.4,color:#7f7f7f80
    style bento_model opacity:0.4,color:#7f7f7f80
    style serve opacity:0.4,color:#7f7f7f80
    style features opacity:0.4,color:#7f7f7f80
    style drift_logs opacity:0.4,color:#7f7f7f80
    style reference_features opacity:0.4,color:#7f7f7f80
    style dot_git opacity:0.4,color:#7f7f7f80
    style dot_dvc opacity:0.4,color:#7f7f7f80
    style repository opacity:0.4,color:#7f7f7f80
    style s3_storage opacity:0.4,color:#7f7f7f80
    style action opacity:0.4,color:#7f7f7f80
    style registry opacity:0.4,color:#7f7f7f80
    style bento_service_cluster opacity:0.4,color:#7f7f7f80
    style k8s_fastapi opacity:0.4,color:#7f7f7f80
    style publicURL opacity:0.4,color:#7f7f7f80
    style dashboard opacity:0.4,color:#7f7f7f80
    style dashboardURL opacity:0.4,color:#7f7f7f80
    style evidently_ui opacity:0.4,color:#7f7f7f80
    style issue opacity:0.4,color:#7f7f7f80
    style pod_runner opacity:0.4,color:#7f7f7f80
    style pod_train opacity:0.4,color:#7f7f7f80
    linkStyle 0 opacity:0.4,color:#7f7f7f80
    linkStyle 1 opacity:0.4,color:#7f7f7f80
    linkStyle 2 opacity:0.4,color:#7f7f7f80
    linkStyle 3 opacity:0.4,color:#7f7f7f80
    linkStyle 4 opacity:0.4,color:#7f7f7f80
    linkStyle 5 opacity:0.4,color:#7f7f7f80
    linkStyle 6 opacity:0.4,color:#7f7f7f80
    linkStyle 7 opacity:0.4,color:#7f7f7f80
    linkStyle 8 opacity:0.4,color:#7f7f7f80
    linkStyle 9 opacity:0.4,color:#7f7f7f80
    linkStyle 10 opacity:0.4,color:#7f7f7f80
    linkStyle 11 opacity:0.4,color:#7f7f7f80
    linkStyle 12 opacity:0.4,color:#7f7f7f80
    linkStyle 13 opacity:0.4,color:#7f7f7f80
    linkStyle 14 opacity:0.4,color:#7f7f7f80
    linkStyle 15 opacity:0.4,color:#7f7f7f80
    linkStyle 16 opacity:0.4,color:#7f7f7f80
    linkStyle 17 opacity:0.4,color:#7f7f7f80
    linkStyle 18 opacity:0.4,color:#7f7f7f80
    linkStyle 19 opacity:0.4,color:#7f7f7f80
    linkStyle 20 opacity:0.4,color:#7f7f7f80
    linkStyle 21 opacity:0.4,color:#7f7f7f80
    linkStyle 22 opacity:0.4,color:#7f7f7f80
    linkStyle 23 opacity:0.4,color:#7f7f7f80
    linkStyle 24 opacity:0.4,color:#7f7f7f80
    linkStyle 25 opacity:0.4,color:#7f7f7f80
    linkStyle 26 opacity:0.4,color:#7f7f7f80
```

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

### Destroy the Kubernetes cluster

When you are done with this part, you can destroy the Kubernetes cluster.

```sh title="Execute the following command(s) in a terminal"
# Destroy the Kubernetes cluster
gcloud container clusters delete --zone $GCP_K8S_CLUSTER_ZONE $GCP_K8S_CLUSTER_NAME
```

!!! tip

    If you need to quickly recreate the cluster after destroying it, here are the
    steps involved:

    * Create the Kubernetes cluster.
    * Deploy the containerized model on Kubernetes.
    * Identify the specialized node.
    * Label the nodes.
    * Create the Kubernetes secret for the base runner registration.
    * Deploy the base runner.
    * Retrieve the Kubernetes cluster credentials.
    * Update the Kubernetes `GCP_K8S_KUBECONFIG` CI/CD secret.

    Refer to the previous chapters for the specific commands. Additionally, ensure
    that all necessary environment variables are correctly defined.

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
