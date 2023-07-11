# Clean up

Now that you have completed the guide, it is crucial to properly manage and remove
the resources and environments you have created. This is necessary to avoid
unnecessary incurring costs and potential security concerns.

Here's a step-by-step guide to help you do that.

- Clean up your cloud provider resources
- Clean up your local environment
- Clean up your repository

!!! warning

    If you are using a new cloud account such as Google Cloud, make sure to delete the resources
    you created before the credits are consumed. Otherwise, **you will be charged**
    for the resources you created.

### Clean up cloud provider resources

In this section, you will delete the resources you created on your cloud provider.

=== ":simple-amazonaws: Amazon Web Services"

    _This is a work in progress._

=== ":simple-exoscale: Exoscale"

    _This is a work in progress._

=== ":simple-googlecloud: Google Cloud"

    **Delete the Google Storage bucket**

    !!! warning

        If you intend to keep the git repository but proceed with deleting the Google Storage bucket, the DVC remote will be disrupted. To continue using DVC with the Git repository, you will need to reconfigure it with a new remote.

    To delete the Google Storage bucket you created you can execute the following command :

    ```sh title="Execute the following command(s) in a terminal"
    gcloud storage rm --recursive gs://$GCP_BUCKET_NAME
    ```

    Alternatively, you can delete the bucket from the Google Cloud Console:

    1. Go to the [Google Cloud Storage Console](https://console.cloud.google.com/storage){:target="\_blank"}.
    2. Make sure you selected the correct project.
    3. Select the bucket you want to delete from the bucket list.
    4. Click on **Delete** at the top of the page.
    5. Follow the instructions to delete the bucket.

    **Delete the Service Account**

    To delete the service account you created you can execute the following command :

    ```sh title="Execute the following command(s) in a terminal"
    gcloud iam service-accounts delete dvc-service-account@${GCP_PROJECT_ID}.iam.gserviceaccount.com
    ```

    Alternatively, you can delete the service account from the Google Cloud Console:

    1. Go to the [Google Cloud IAM Console](https://console.cloud.google.com/iam-admin/serviceaccounts){:target="\_blank"}.
    2. Make sure you selected the correct project.
    3. Select the service account you want to delete from the service account list.
    4. Click on **Delete** at the top of the page.
    5. Follow the instructions to delete the service account.

    **Delete the local Service Account key**

    You can run the following command to delete the service account key you created locally:

    ```sh title="Execute the following command(s) in a terminal"
    rm ~/.config/gcloud/dvc-google-service-account-key.json
    ```

    **Delete the Google Cloud project**

    To delete the Google Cloud project you created:

    1. Go to the [Google Cloud Resource Manager Console](https://console.cloud.google.com/cloud-resource-manager){:target="\_blank"}.
    2. Select the project you created.
    3. Click on **Delete** at the top of the page.
    4. Follow the instructions to shut down the project.

=== ":simple-microsoftazure: Microsoft Azure"

    _This is a work in progress._

=== ":simple-kubernetes: Self-hosted Kubernetes"

    _This is a work in progress._

### Clean up your repository

In this section, you will delete the repository you created on GitHub or GitLab.

=== ":simple-github: GitHub"

    To delete the GitHub repository you created:

    1. Go to the repository page in GitHub.
    2. Click on **Settings** above the repository.
    3. Scroll down to the "Danger Zone" section at the bottom of the page.
    4. Click on **Delete this repository**.
    5. Follow the instructions to delete the repository.

=== ":simple-gitlab: GitLab"

    To delete the GitLab repository you created:

    1. Go to the repository page in GitLab.
    2. Click on the **Settings** button on the left side of the page.
    3. Scroll down to the "Advanced" section at the bottom of the page and click on "Expand".
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

In this section, you will delete the local environment you created for this guide.

Start by ensuring you have left the virtual environment created in the previous chapter.

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

Before you finish, double-check that you have deleted all the resources and environments you created. This will ensure that you don't incur unexpected costs or leave any security vulnerabilities.

Here is a checklist of all the resources and environments you created.

!!! tip

    You can click on the list items to mark them as completed if needed.

- [ ] The cloud provider S3 bucket
- [ ] The cloud provider credentials
- [ ] The cloud provider project
- [ ] The GitHub or GitLab repository
    - [ ] If you used GitLab, the Personal Access Token
- [ ] The projects directories
    - [ ] The `a-guide-to-mlops-jupyter-notebook` directory
    - [ ] The `a-guide-to-mlops` directory

### Summary

By following these steps, you have successfully cleaned up the resources and environments you created during the guide. We hope you found this guide helpful and that it has given you a good understanding of the importance of cleaning up after yourself in cloud computing environments.
