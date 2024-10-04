---
title: "Part 3 - Conclusion"
---

# Conclusion

Congratulations! You did it!

In this third part, you were able to move the model outside of the experiment
context. The model is now saved and loaded with BentoML. You can serve the model
locally and deploy it on Kubernetes. The model is also retrained on a Kubernetes
pod.

The model is now ready to be used in production.

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
        bento_model[classifier.bentomodel] <-.-> dot_dvc
        prepare[prepare.py] <-.-> dot_dvc
        train[train.py] <-.-> dot_dvc
        evaluate[evaluate.py] <-.-> dot_dvc
        data --> prepare
        bento_model --> |import_model
                         load_model|evaluate
        train --> |save_model
                   export_model|bento_model
        subgraph dvcGraph["dvc.yaml (dvc repro)"]
            prepare --> train
            train --> evaluate
        end
        params[params.yaml] -.- prepare
        params -.- train
        params <-.-> dot_dvc
        subgraph bentoGraph[bentofile.yaml]
            bento_model
            serve[serve.py] <--> bento_model
        end
    end

    subgraph remoteGraph[REMOTE]
        s3_storage
        subgraph gitGraph[Git Remote]
            repository[(Repository)] --> action[Action]
            request[PR] --> |merge|repository
        end
        action --> |bentoml containerize
                    docker push|registry
        s3_storage -.- |...|request
        subgraph clusterGraph[Kubernetes]
            subgraph clusterPodGraph[Kubernetes Pod]
                pod_train[Train model] <-.-> k8s_gpu[GPUs]
                bento_artifact[Model artifact]
            end
            pod_runner[Runner] --> clusterPodGraph
            action --> |dvc pull
                        dvc repro|bento_artifact
            action -->|dvc pull
                       dvc repro| pod_train
            bento_service_cluster[classifier.bentomodel] --> k8s_fastapi[FastAPI]
        end
        bento_artifact -->|bentoml build|action
        action --> |self-hosted|pod_runner
        pod_train -->|cml publish| request
        pod_train -->|dvc push| s3_storage

        registry[(Container
                  registry)] --> bento_service_cluster
        action --> |kubectl apply|bento_service_cluster
    end

    subgraph browserGraph[BROWSER]
        k8s_fastapi <--> publicURL["public URL"]
    end

    linkStyle 19 opacity:0.0
```

The main goal of the MLOps process is to ensure that the model is reproducible,
reliable and can be used in production. This goal is now achieved.

The next part is an improvement of the MLOps process. You will learn how to
label new data and retrain the model using Label Studio.

Do not forget to [Clean up](./clean-up.md) if you want to stop here or continue
with
[Part 4 - Labeling the data and retrain](../part-4-labeling-the-data-and-retrain/introduction.md)
of the MLOps guide!
