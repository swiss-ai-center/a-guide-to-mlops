# Clean up

Now that you have completed the guide, it is crucial to properly manage and
remove the resources and environments you have created. This is necessary to
avoid unnecessary incurring costs and potential security concerns.

Here's a step-by-step guide to help you do that.

- Clean up the cloud provider resources
- Clean up your local environment
- Clean up your repository

!!! warning

    If you are using a new cloud account such as Google Cloud, make sure to delete
    the resources you created before the credits are consumed. Otherwise,
    **you will be charged** for the resources you created.

### Clean up cloud provider resources

In this section, you will delete the resources you created on the cloud
provider.

=== ":simple-googlecloud: Google Cloud"

    **Delete the Kubernetes cluster**

    To delete the
    [Google Kubernetes cluster](https://console.cloud.google.com/kubernetes) you
    created, you can execute the following command:

    ```sh title="Execute the following command(s) in a terminal"
    # Delete the Kubernetes cluster
    gcloud container clusters delete --zone $GCP_K8S_CLUSTER_ZONE $GCP_K8S_CLUSTER_NAME
    ```

    Press ++y++ to confirm the deletion.

    To disable the Google Kubernetes Engine API, you can execute the following
    command:

    ```sh title="Execute the following command(s) in a terminal"
    # Disable the Google Kubernetes Engine API
    gcloud services disable container.googleapis.com --force
    ```

    **Delete the Google Artifact Registry**

    To delete the
    [Google Artifact Registry](https://console.cloud.google.com/artifacts) used to
    store the Docker images you created, you can execute the following command:

    ```sh title="Execute the following command(s) in a terminal"
    # Delete the artifact repository
    gcloud artifacts repositories delete --location $GCP_CONTAINER_REGISTRY_LOCATION $GCP_CONTAINER_REGISTRY_NAME
    ```

    Press ++y++ to confirm the deletion.

    To disable the Google Artifact Registry API, you can execute the following
    command:

    ```sh title="Execute the following command(s) in a terminal"
    # Disable the Google Artifact Registry API
    gcloud services disable artifactregistry.googleapis.com --force
    ```

    **Delete the Google Storage bucket**

    !!! warning

        If you intend to keep the Git repository but proceed with deleting the Google
        Storage bucket, the DVC remote will be disrupted. To continue using DVC with the
        Git repository, you will need to reconfigure it with a new remote.

    To delete the [Google Storage bucket](https://console.cloud.google.com/storage)
    you created, you can execute the following command:

    ```sh title="Execute the following command(s) in a terminal"
    # Delete the Google Storage bucket
    gcloud storage rm --recursive gs://$GCP_BUCKET_NAME
    ```

    Press ++y++ to confirm the deletion.

    **Delete the Google Service Account**

    To delete the
    [Google Service Account](https://console.cloud.google.com/iam-admin/serviceaccounts)
    you created, you can execute the following command:

    ```sh title="Execute the following command(s) in a terminal"
    # Delete the Google Service Account
    gcloud iam service-accounts delete google-service-account@${GCP_PROJECT_ID}.iam.gserviceaccount.com
    ```

    Press ++y++ to confirm the deletion.

    **Delete the local Google Service Account**

    You can run the following command to delete the Google Service Account you
    exported locally:

    ```sh title="Execute the following command(s) in a terminal"
    # Delete the local Google Service Account
    rm ~/.config/gcloud/google-service-account-key.json
    ```

    **Unlink the billing account**

    You can run the following command to unlink the billing account from the
    project:

    ```sh title="Execute the following command(s) in a terminal"
    # Unlink the billing account
    gcloud billing projects unlink $GCP_PROJECT_ID
    ```

    Press ++y++ to confirm the unlinking.

    **Delete the Google Cloud project**

    To delete the
    [Google Cloud project](https://console.cloud.google.com/home/dashboard) you
    created, you can execute the following command:

    ```sh title="Execute the following command(s) in a terminal"
    # Delete the Google Cloud project
    gcloud projects delete $GCP_PROJECT_ID
    ```

    Press ++y++ to confirm the deletion.

    **Close the Billing Account**

    To close the Billing Account you created:

    1. Go to the
       [Google Cloud Billing Console](https://console.cloud.google.com/billing){:target="\_blank"}.
    2. Select the Billing Account you created.
    3. Click on **Account management** in the menu.
    4. Select **Actions** from the project list and select **Disable billing**.
    5. Select *Close Billing Account* at the top of the page.
    6. Follow the instructions to close the account.

    **Remove the Payment method**

    To remove the payment method you added:

    1. Go to the **Payment method** in the 3-dots top right menu.
    2. Select the card you added and select **Remove**.
    3. Follow the instructions to remove the payment method.

=== ":material-cloud: Using another cloud provider? Read this!"

    This guide has been written with Google Cloud in mind. We are open to
    contributions to add support for other cloud providers such as
    [:simple-amazonwebservices: Amazon Web Services](https://aws.amazon.com),
    [:simple-exoscale: Exoscale](https://www.exoscale.com),
    [:material-microsoft-azure: Microsoft Azure](https://azure.microsoft.com) or
    [:simple-kubernetes: Self-hosted Kubernetes](https://kubernetes.io) but we might
    not officially support them.

    If you want to contribute, please open an issue or a pull request on the
    [GitHub repository](https://github.com/swiss-ai-center/a-guide-to-mlops). Your
    help is greatly appreciated!

### Clean up your repository

In this section, you will delete the repository you created on GitHub or GitLab.

=== ":simple-github: GitHub"

    To delete the GitHub repository you created:

    1. Go to the repository page in GitHub.
    2. Click on **Settings** above the repository.
    3. Scroll down to the "Danger Zone" section at the bottom of the page.
    4. Click on **Delete this repository**.
    5. Follow the instructions to delete the repository.

    To delete the GitHub Personal Access Token you created:

    1. Go to your GitHub **Settings** at the top right of the page.
    2. Click on **Developers settings** in the left sidebar.
    3. Click on **Personal access tokens** in the left sidebar and then on **Tokens
       (classic)**.
    4. Find the Personal Access Token you created for this guide.
    5. Click on the **Delete** button next to it.
    6. Follow the instructions to delete the token.

=== ":simple-gitlab: GitLab"

    To delete the GitLab repository you created:

    1. Go to the repository page in GitLab.
    2. Click on the **Settings** button on the left side of the page.
    3. Scroll down to the "Advanced" section at the bottom of the page and click on
       "Expand".
    4. Scroll down to "Delete this project".
    5. Click on the **Delete project** button.
    6. Follow the instructions to delete the repository.

    To delete the GitLab Personal Access Token you created:

    1. Go to your GitLab **Profile preferences** at the top right of the page.
    2. Click on **Access Tokens** in the left sidebar.
    3. Find the Personal Access Token you created for this guide.
    4. Click on the **Revoke** button next to it.
    5. Follow the instructions to revoke the token.

### Clean up your local environment

In this section, you will delete the local environment you created for this
guide.

Start by ensuring you have left the virtual environment created in the previous
chapter.

```sh title="Execute the following command(s) in a terminal"
# Deactivate the virtual environment
deactivate
```

Then, you can delete the Python virtual environment directory.

```sh title="Execute the following command(s) in a terminal"
# Move back to the root directory
cd ..

# Delete the a-guide-to-mlops-jupyter-notebook
rm -rf a-guide-to-mlops-jupyter-notebook

# Delete the a-guide-to-mlops directory
rm -rf a-guide-to-mlops
```

### Double-check everything

Before you finish, double-check that you have deleted all the resources and
environments you created. This will ensure that you don't incur unexpected costs
or leave any security vulnerabilities.

Here is a checklist of all the resources and environments you created.

!!! tip

    You can click on the list items to mark them as completed if needed.

- [ ] The cloud provider Kubernetes cluster
- [ ] The cloud provider container registry
- [ ] The cloud provider S3 bucket
- [ ] The cloud provider credentials
- [ ] The cloud provider project
- [ ] The GitHub or GitLab Personal Access Tokens
- [ ] The GitHub or GitLab repository
- [ ] The projects directories
    - [ ] The `a-guide-to-mlops-jupyter-notebook` directory
    - [ ] The `a-guide-to-mlops` directory

### Summary

By following these steps, you have successfully cleaned up the resources and
environments you created during the guide. We hope you found this guide helpful
and that it has given you a good understanding of the importance of cleaning up
after yourself in cloud computing environments.
