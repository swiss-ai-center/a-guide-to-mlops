# Train the model on a Kubernetes cluster with CML

!!! warning

	This is a work in progress.

## Introduction

The purpose of this guide is to improve the results obtained at the end of [The guide](../../the-guide/introduction/index.md) to allow the training of the model on a Kubernetes cluster with the help of CML.

Carrying out the guide is necessary to follow this guide.

In this chapter, you will learn how to:

1. Create a Kubernetes cluster on Google Cloud
2. Configure CML to start a runner on Kubernetes
3. Start the training of the model from your CI/CD pipeline on the Kubernetes cluster

## Steps

### Enable the Google Kubernetes Engine API

You must enable the Google Kubernetes Engine API to create Kubernetes clusters on Google Cloud.

[Enable Google Kubernetes Engine API :octicons-arrow-up-right-16:](https://console.cloud.google.com/flows/enableapi?apiid=container.googleapis.com){ .md-button .md-button--primary }

### Create the Kubernetes cluster

Create the Google Kubernetes cluster with the Google Cloud CLI.

```sh title="Execute the following command(s) in a terminal"
gcloud container clusters create \
	--machine-type=e2-standard-2 \
	--num-nodes=2 \
	--zone=europe-west6-a \
	mlops-kubernetes
```

### Install kubectl

Install the Kubernetes CLI using the Google Cloud CLI to interact with Kubernetes clusters.

```sh title="Execute the following command(s) in a terminal"
# Install kubectl with gcloud
gcloud components install kubectl
```

### Validate kubectl can access the cluster

Validate kubectl can access the cluster using Google Cloud credentials.

```sh title="Execute the following command(s) in a terminal"
kubectl get namespaces
```

The output should be similar to this.

```
NAME              STATUS   AGE
default           Active   25m
kube-node-lease   Active   25m
kube-public       Active   25m
kube-system       Active   25m
```

### Display the nodes labels

Display the nodes labels with the following command.

```sh title="Execute the following command(s) in a terminal"
kubectl get nodes --show-labels
```

The output should be similar to this. As noticed, you have two nodes in your cluster.

```
NAME                                              STATUS   ROLES    AGE   VERSION            LABELS
gke-mlops-kubernetes-default-pool-d4f966ea-8rbn   Ready    <none>   49s   v1.24.9-gke.3200   beta.kubernetes.io/arch=amd64,[...]
gke-mlops-kubernetes-default-pool-d4f966ea-p7qm   Ready    <none>   50s   v1.24.9-gke.3200   beta.kubernetes.io/arch=amd64,[...]
```

### Labelize the nodes

Let's imagine one node has a GPU and the other one doesn't. You can labelize the nodes to be able to use the GPU node for the training of the model. For our expiriment, there is no need to have a GPU to train the model but it's for demonstration purposes.

```sh title="Execute the following command(s) in a terminal"
kubectl label nodes <your-node-1-name> gpu=true
kubectl label nodes <your-node-2-name> gpu=false
```

In the previous example, the nodes are named `gke-mlops-kubernetes-default-pool-d4f966ea-8rbn` and `gke-mlops-kubernetes-default-pool-d4f966ea-p7qm`. The command will be the following.

```sh title="Labelization example"
kubectl label nodes gke-mlops-kubernetes-default-pool-d4f966ea-8rbn gpu=true
kubectl label nodes gke-mlops-kubernetes-default-pool-d4f966ea-p7qm gpu=false
```

You can check the labels with the `kubectl get nodes --show-labels` command. You should see for both nodes the `gpu` label with the value `true` or `false`.

### Update the CI/CD configuration file

You'll now update the CI/CD configuration file to start a runner on the Kubernetes cluster with the help of CML. Using the labels defined previously, you'll be able to start the training of the model on the node with the GPU.

=== ":simple-github: GitHub"

	In order to allow CML to create a self-hosted runner, a Personal Access Token (PAT) must be
	created.

	Follow the [_Personal Access Token_ - cml.dev](https://cml.dev/doc/self-hosted-runners?tab=GitHub#personal-access-token) guide to create a personal access token named `CML_PAT` with the `repo` scope.

	Store the Personal Access Token as a CI/CD variable by going to the **Settings** section from
	the top header of your GitHub repository.

	Select **Secrets and variables > Actions** and select **New repository secret**.

	Create a new variable named `CML_PAT` with the value of
	the Personal Access Token as its value. Save the variable by selecting
	**Add secret**.

	Update the `.github/workflows/mlops.yml` file.

	```yaml  title=".github/workflows/mlops.yml" hl_lines="9-10 42-133"
	TODO
	```

	Check the differences with Git to validate the changes.

	```sh title="Execute the following command(s) in a terminal"
	# Show the differences with Git
	git diff .github/workflows/mlops.yml
	```

	The output should be similar to this:

	```diff
	diff --git a/.github/workflows/mlops.yml b/.github/workflows/mlops.yml
	index 0ca4d29..10afa49 100644
	--- a/.github/workflows/mlops.yml
	+++ b/.github/workflows/mlops.yml
	TODO
	```

	Take some time to understand the changes made to the file.

=== ":simple-gitlab: GitLab"

	Update the `.gitlab-ci.yml` file.

	```yaml title=".gitlab-ci.yml" hl_lines="2 19-38 43-47"
	TODO
	```

	Check the differences with Git to validate the changes.

	```sh title="Execute the following command(s) in a terminal"
	# Show the differences with Git
	git diff .gitlab-ci.yml
	```

	The output should be similar to this:

	```diff
	diff --git a/.gitlab-ci.yml b/.gitlab-ci.yml
	index 561d04f..fad1002 100644
	--- a/.gitlab-ci.yml
	+++ b/.gitlab-ci.yml
	TODO
	```

	Take some time to understand the changes made to the file.

### Push the CI/CD pipeline configuration file to Git

=== ":simple-github: GitHub"

	Push the CI/CD pipeline configuration file to Git.

	```sh title="Execute the following command(s) in a terminal"
	# Add the configuration file
	git add .github/workflows/mlops.yml

	# Commit the changes
	git commit -m "A pipeline will run my experiment on Kubernetes on each push"

	# Push the changes
	git push
	```

=== ":simple-gitlab: GitLab"

	Push the CI/CD pipeline configuration file to Git.

	```sh title="Execute the following command(s) in a terminal"
	# Add the configuration file
	git add .gitlab-ci.yml

	# Commit the changes
	git commit -m "A pipeline will run my experiment on Kubernetes on each push"

	# Push the changes
	git push
	```

### Check the results

On GitLab, you can see the pipeline running on the **CI/CD > Pipelines** page.

On GitHub, you can see the pipeline running on the **Actions** page.

TODO

This chapter is done, you can check the summary.

## Summary

Congrats! You now can train your model on on a custom infrastructure with custom hardware for specific use-cases.

In this chapter, you have successfully:

1. Created a Kubernetes cluster on Google Cloud
2. Configured CML to start a runner on Kubernetes
3. Trained the model on the Kubernetes cluster

## State of the MLOps process

- ✅ The training of the model can be done on a custom infrastructure with custom hardware for specific use-cases.

## Sources

Highly inspired by the [_Self-hosted (On-premise or Cloud) Runners_ - cml.dev](https://cml.dev/doc/self-hosted-runners), [_Install kubectl and configure cluster access_ - cloud.google.com](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl), [_gcloud container clusters create_ - cloud.google.com](https://cloud.google.com/sdk/gcloud/reference/container/clusters/create), the [_Install Tools_ - kubernetes.io](https://kubernetes.io/docs/tasks/tools/), [_Assigning Pods to Nodes_ - kubernetes.io](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector) and [_Assign Pods to Nodes_ - kubernetes.io](https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes/) guides.

Want to see what the result at the end of this chapter should look like? Have a
look at the Git repository directory here:
[train-the-model-on-a-kubernetes-cluster-with-cml](https://github.com/csia-pme/a-guide-to-mlops/tree/main/docs/advanced-concepts/train-the-model-on-a-kubernetes-cluster-with-cml).
