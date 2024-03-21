# Chapter 14: Deploy and access the model on Kubernetes

## Introduction

In this chapter, you will learn how to deploy the model on Kubernetes and access
it from a Kubernetes pod using the previous Docker image.

This will allow the model to be used by other applications and services on a
public endpoint accessible from anywhere.

In this chapter, you will learn how to:

1. Create the Kubernetes cluster
2. Validate kubectl can access the Kubernetes cluster
3. Create the Kubernetes configuration files
4. Deploy the Docker image on Kubernetes
5. Access the model

!!! danger

    The following steps will create resources on the cloud provider. These resources
    will be deleted at the end of the guide, but you might be charged for them.
    Kubernetes clusters are not free on most cloud providers and can be expensive.
    Make sure to delete the resources at the end of the guide.

The following diagram illustrates control flow of the experiment at the end of
this chapter:

```mermaid
flowchart TB
    dot_dvc[(.dvc)] <-->|dvc pull\ndvc push| s3_storage[(S3 Storage)]
    dot_git[(.git)] <-->|git pull\ngit push| gitGraph[Git Remote]
    workspaceGraph <-....-> dot_git
    data[data/raw]
    subgraph cacheGraph[CACHE]
        dot_dvc
        dot_git
        bento_artifact[(Containerized\nartifact)]
    end
    subgraph remoteGraph[REMOTE]
        s3_storage
        subgraph gitGraph[Git Remote]
            repository[(Repository)] --> action[Action]
            action[Action] --> |...|request[PR]
            request --> repository[(Repository)]
        end
        subgraph clusterGraph[Kubernetes]
            bento_service_cluster[classifier.bentomodel] --> k8s_fastapi[FastAPI]
        end
        registry[(Container\nregistry)] --> |kubectl apply|bento_service_cluster
    end
    subgraph workspaceGraph[WORKSPACE]
        data --> code[*.py]
        subgraph dvcGraph["dvc.yaml"]
            code
        end
        params[params.yaml] -.- code
        code <--> bento_model[classifier.bentomodel]
        subgraph bentoGraph[bentofile.yaml]
            bento_model <--> serve[serve.py]
        end

        bentoGraph -->|bento build\nbento containerize| bento_artifact
        bento_model <-.-> dot_dvc
        bento_artifact -->|docker push| registry
    end

    subgraph browserGraph[BROWSER]
        k8s_fastapi <--> publicURL["public URL"]
    end
    style workspaceGraph opacity:0.4,color:#7f7f7f80
    style dvcGraph opacity:0.4,color:#7f7f7f80
    style cacheGraph opacity:0.4,color:#7f7f7f80
    style data opacity:0.4,color:#7f7f7f80
    style dot_git opacity:0.4,color:#7f7f7f80
    style dot_dvc opacity:0.4,color:#7f7f7f80
    style code opacity:0.4,color:#7f7f7f80
    style serve opacity:0.4,color:#7f7f7f80
    style bento_model opacity:0.4,color:#7f7f7f80
    style bentoGraph opacity:0.4,color:#7f7f7f80
    style bento_artifact opacity:0.4,color:#7f7f7f80
    style params opacity:0.4,color:#7f7f7f80
    style s3_storage opacity:0.4,color:#7f7f7f80
    style repository opacity:0.4,color:#7f7f7f80
    style action opacity:0.4,color:#7f7f7f80
    style request opacity:0.4,color:#7f7f7f80
    style remoteGraph opacity:0.4,color:#7f7f7f80
    style gitGraph opacity:0.4,color:#7f7f7f80
    linkStyle 0 opacity:0.4,color:#7f7f7f80
    linkStyle 1 opacity:0.4,color:#7f7f7f80
    linkStyle 2 opacity:0.4,color:#7f7f7f80
    linkStyle 3 opacity:0.4,color:#7f7f7f80
    linkStyle 4 opacity:0.4,color:#7f7f7f80
    linkStyle 5 opacity:0.4,color:#7f7f7f80
    linkStyle 8 opacity:0.4,color:#7f7f7f80
    linkStyle 9 opacity:0.4,color:#7f7f7f80
    linkStyle 10 opacity:0.4,color:#7f7f7f80
    linkStyle 11 opacity:0.4,color:#7f7f7f80
    linkStyle 12 opacity:0.4,color:#7f7f7f80
    linkStyle 13 opacity:0.4,color:#7f7f7f80
    linkStyle 14 opacity:0.4,color:#7f7f7f80
```

## Steps

### Install the Kubernetes CLI

Install the Kubernetes CLI (kubectl) on your machine.

=== ":simple-googlecloud: Google Cloud"

    Install kubectl with the Google Cloud CLI:

    ```sh title="Execute the following command(s) in a terminal"
    # Install kubectl with gcloud
    gcloud components install kubectl
    ```

=== ":material-cloud: Using another cloud provider? Read this!"

    This guide has been written with Google Cloud in mind. We are open to
    contributions to add support for other cloud providers such as
    [:simple-amazonaws: Amazon Web Services](https://aws.amazon.com),
    [:simple-exoscale: Exoscale](https://www.exoscale.com),
    [:simple-microsoftazure: Microsoft Azure](https://azure.microsoft.com) or
    [:simple-kubernetes: Self-hosted Kubernetes](https://kubernetes.io) but we might
    not officially support them.

    If you want to contribute, please open an issue or a pull request on the
    [GitHub repository](https://github.com/swiss-ai-center/a-guide-to-mlops). Your
    help is greatly appreciated!

### Create the Kubernetes cluster

In order to deploy the model on Kubernetes, you will need a Kubernetes cluster.

Follow the steps below to create one.

=== ":simple-googlecloud: Google Cloud"

    **Enable the Google Kubernetes Engine API**

    You must enable the Google Kubernetes Engine API to create Kubernetes clusters
    on Google Cloud with the following command:

    !!! tip

        You can display the available services in your project with the following
        command:

        ```sh title="Execute the following command(s) in a terminal"
        # List the services
        gcloud services list
        ```

    ```sh title="Execute the following command(s) in a terminal"
    # Enable the Google Kubernetes Engine API
    gcloud services enable container.googleapis.com
    ```

    **Create the Kubernetes cluster**

    Create the Google Kubernetes cluster with the Google Cloud CLI.

    Export the cluster name as an environment variable. Replace `<my cluster name>`
    with a cluster name of your choice. It has to be lowercase and words separated
    by hyphens. For example, use `mlops-kubernetes` for the cluster name.

    ```sh title="Execute the following command(s) in a terminal"
    export GCP_K8S_CLUSTER_NAME=<my cluster name>
    ```

    Export the cluster zone as an environment variable. You can view the available
    zones at
    [Regions and zones](https://cloud.google.com/compute/docs/regions-zones#available).
    You should ideally select a zone close to where most of the expected traffic
    will come from. Replace `<my cluster zone>` with your own zone (ex:
    `europe-west6-a` for Zurich, Switzerland).

    ```sh title="Execute the following command(s) in a terminal"
    export GCP_K8S_CLUSTER_ZONE=<my cluster zone>
    ```

    Create the Kubernetes cluster. You can also view the available types of machine
    with the `gcloud compute machine-types list` command:

    !!! info

         This can take several minutes. Please be patient.

    ```sh title="Execute the following command(s) in a terminal"
    # Create the Kubernetes cluster
    gcloud container clusters create \
    	--machine-type=e2-standard-2 \
    	--num-nodes=2 \
    	--zone=$GCP_K8S_CLUSTER_ZONE \
    	$GCP_K8S_CLUSTER_NAME
    ```

    The output should be similar to this:

    ```text
    Default change: VPC-native is the default mode during cluster creation for versions greater than 1.21.0-gke.1500. To create advanced routes based clusters, please pass the `--no-enable-ip-alias` flag
    Default change: During creation of nodepools or autoscaling configuration changes for cluster versions greater than 1.24.1-gke.800 a default location policy is applied. For Spot and PVM it defaults to ANY, and for all other VM kinds a BALANCED policy is used. To change the default values use the `--location-policy` flag.
    Note: Your Pod address range (`--cluster-ipv4-cidr`) can accommodate at most 1008 node(s).
    Creating cluster mlops-kubernetes in europe-west6-a... Cluster is being health-checked (master is hea
    lthy)...done.
    Created [https://container.googleapis.com/v1/projects/mlops-code-395207/zones/europe-west6-a/clusters/mlops-kubernetes].
    To inspect the contents of your cluster, go to: https://console.cloud.google.com/kubernetes/workload_/gcloud/europe-west6-a/mlops-kubernetes?project=mlops-code-395207
    kubeconfig entry generated for mlops-kubernetes.
    NAME              LOCATION        MASTER_VERSION   MASTER_IP    MACHINE_TYPE   NODE_VERSION     NUM_NODES  STATUS
    mlops-kubernetes  europe-west6-a  1.27.2-gke.1200  34.65.19.80  e2-standard-2  1.27.2-gke.1200  2          RUNNING
    ```

=== ":material-cloud: Using another cloud provider? Read this!"

    This guide has been written with Google Cloud in mind. We are open to
    contributions to add support for other cloud providers such as
    [:simple-amazonaws: Amazon Web Services](https://aws.amazon.com),
    [:simple-exoscale: Exoscale](https://www.exoscale.com),
    [:simple-microsoftazure: Microsoft Azure](https://azure.microsoft.com) or
    [:simple-kubernetes: Self-hosted Kubernetes](https://kubernetes.io) but we might
    not officially support them.

    If you want to contribute, please open an issue or a pull request on the
    [GitHub repository](https://github.com/swiss-ai-center/a-guide-to-mlops). Your
    help is greatly appreciated!

### Validate kubectl can access the Kubernetes cluster

Validate kubectl can access the Kubernetes cluster:

```sh title="Execute the following command(s) in a terminal"
# Get namespaces
kubectl get namespaces
```

The output should be similar to this:

```text
NAME              STATUS   AGE
default           Active   2m
gmp-public        Active   2m
gmp-system        Active   2m
kube-node-lease   Active   2m
kube-public       Active   2m
kube-system       Active   2m
```

### Create the Kubernetes configuration files

In order to deploy the model on Kubernetes, you will need to create the
Kubernetes configuration files. These files describe the deployment and service
of the model.

Create a new directory called `kubernetes` in the root of the project.

Create a new file called `deployment.yaml` in the `kubernetes` directory with
the following content. Replace `<docker image>` with the Docker image you have
created in the previous steps:

!!! tip

    You can find the Docker image with the following command:

    ```sh title="Execute the following command(s) in a terminal"
    # Get the Docker image
    echo $GCP_CONTAINER_REGISTRY_HOST/celestial-bodies-classifier:latest
    ```

```yaml title="kubernetes/deployment.yaml"
apiVersion: apps/v1
kind: Deployment
metadata:
  name: celestial-bodies-classifier-deployment
  labels:
    app: celestial-bodies-classifier
spec:
  replicas: 1
  selector:
    matchLabels:
      app: celestial-bodies-classifier
  template:
    metadata:
      labels:
        app: celestial-bodies-classifier
    spec:
      containers:
      - name: celestial-bodies-classifier
        image: <docker image>
```

Create a new file called `service.yaml` in the `kubernetes` directory with the
following content:

```yaml title="kubernetes/service.yaml"
apiVersion: v1
kind: Service
metadata:
  name: celestial-bodies-classifier-service
spec:
  type: LoadBalancer
  ports:
    - name: http
      port: 80
      targetPort: 3000
      protocol: TCP
  selector:
    app: celestial-bodies-classifier
```

The `deployment.yaml` file describes the deployment of the model. It contains
the number of replicas, the image to use, and the labels to use.

The `service.yaml` file describes the service of the model. It contains the type
of service, the ports to use, and the labels to use.

### Deploy the Bento on Kubernetes

To deploy the containerised Bento model artifact on Kubernetes, you will need to
apply the Kubernetes configuration files.

Apply the Kubernetes configuration files with the following commands:

```sh title="Execute the following command(s) in a terminal"
# Apply the deployment
kubectl apply -f kubernetes/deployment.yaml

# Apply the service
kubectl apply -f kubernetes/service.yaml
```

The output should be similar to this:

```text
deployment.apps/celestial-bodies-classifier-deployment created
service/celestial-bodies-classifier-service created
```

### Access the model

To access the model, you will need to find the external IP address of the
service. You can do so with the following command:

!!! info

    The external IP address of the service can take a few minutes to be available.

```sh title="Execute the following command(s) in a terminal"
# Get the description of the service
kubectl describe services celestial-bodies-classifier
```

The output should be similar to this:

```text hl_lines="11"
Name:                     celestial-bodies-classifier-service
Namespace:                default
Labels:                   <none>
Annotations:              cloud.google.com/neg: {"ingress":true}
Selector:                 app=celestial-bodies-classifier
Type:                     LoadBalancer
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.24.1.34
IPs:                      10.24.1.34
LoadBalancer Ingress:     34.65.255.92
Port:                     http  80/TCP
TargetPort:               3000/TCP
NodePort:                 http  30882/TCP
Endpoints:                10.20.0.9:3000
Session Affinity:         None
External Traffic Policy:  Cluster
Events:
  Type    Reason                Age                  From                Message
  ----    ------                ----                 ----                -------
  Normal  Type                  36m                  service-controller  ClusterIP -> LoadBalancer
```

The `LoadBalancer Ingress` field contains the external IP address of the
service. In this case, it is `34.65.255.92`.

Try to access the model at the port `80` using the external IP address of the
service. You should be able to access the FastAPI documentation page at
`http://<load balancer ingress ip>:80`. In this case, it is
`http://34.65.255.92:80`.

### Check the changes

Check the changes with Git to ensure that all the necessary files are tracked:

```sh title="Execute the following command(s) in a terminal"
# Add all the files
git add .

# Check the changes
git status
```

The output should look similar to this:

```text
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
(use "git restore --staged <file>..." to unstage)
    new file:   kubernetes/deployment.yaml
    new file:   kubernetes/service.yaml
```

### Commit the changes to Git

Commit the changes to Git.

```sh title="Execute the following command(s) in a terminal"
# Commit the changes
git commit -m "Kubernetes can be used to deploy the model"

# Push the changes
git push
```

## Summary

Congratulations! You have successfully deployed the model on Kubernetes with
BentoML and Docker, accessed it from an external IP address.

You can now use the model from anywhere.

In this chapter, you have successfully:

1. Created the Kubernetes configuration files and deployed the BentoML model
   artifact on Kubernetes
2. Access the model

## State of the MLOps process

- [x] Notebook has been transformed into scripts for production
- [x] Codebase and dataset are versioned
- [x] Steps used to create the model are documented and can be re-executed
- [x] Changes done to a model can be visualized with parameters, metrics and
      plots to identify differences between iterations
- [x] Codebase can be shared and improved by multiple developers
- [x] Dataset can be shared among the developers and is placed in the right
      directory in order to run the experiment
- [x] Experiment can be executed on a clean machine with the help of a CI/CD
      pipeline
- [x] CI/CD pipeline is triggered on pull requests and reports the results of
      the experiment
- [x] Changes to model can be thoroughly reviewed and discussed before
      integrating them into the codebase
- [x] Model can be saved and loaded with all required artifacts for future usage
- [x] Model can be easily used outside of the experiment context
- [x] Model is accessible from the Internet and can be used anywhere
- [ ] Model requires manual deployment on the cluster
- [ ] Model cannot be trained on hardware other than the local machine

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by:

- [_Connecting a repository to a package_ - docs.github.com](https://docs.github.com/en/packages/learn-github-packages/connecting-a-repository-to-a-package)
- [_Working with the Container registry_ - docs.github.com](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [_Containerization_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/guides/containerization.html)
- [_Build options_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/guides/build-options.html)
