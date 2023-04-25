# Clean up and Conclusion

## Cleaning up resources and environments

Now that you have completed the guide, it's important to clean up the resources and environments you created to avoid incurring unnecessary costs and security related issues. Here's a step-by-step guide to help you do that.

!!! warning

    If you are using a new Google Cloud account, make sure to delete the resources you created before the credits are consumed. Otherwise, **you will be charged for the resources you created.**

### Google Cloud

#### Delete the Google Storage bucket

!!! warning

    Ignore this if you plan deleting the git repository. When deleting the Google Storage bucket, **it will break the DVC remote**. You will need to reconfigure it to a new remote if you want to keep the Git repository to use DVC.

To delete the Google Storage bucket you created you can execute the following command :

```sh title="Execute the following command(s) in a terminal"
gcloud storage rm --recursive gs://<your bucket name>
```

Alternatively, you can delete the bucket from the Google Cloud Console:

1. Go to the [Google Cloud Storage Console](https://console.cloud.google.com/storage){:target="\_blank"}.
2. Make sure you selected the correct project.
3. Select the bucket you want to delete from the bucket list.
4. Click on **Delete** at the top of the page.
5. Follow the instructions to delete the bucket.

#### Delete the Service Account

To delete the service account you created you can execute the following command :

```sh title="Execute the following command(s) in a terminal"
gcloud iam service-accounts delete dvc-service-account@<id of your gcp project>.iam.gserviceaccount.com
```

Alternatively, you can delete the service account from the Google Cloud Console:

1. Go to the [Google Cloud IAM Console](https://console.cloud.google.com/iam-admin/serviceaccounts){:target="\_blank"}.
2. Make sure you selected the correct project.
3. Select the service account you want to delete from the service account list.
4. Click on **Delete** at the top of the page.
5. Follow the instructions to delete the service account.

#### Delete the local Service Account key

You can run the following command to delete the service account key you created locally:

```sh title="Execute the following command(s) in a terminal"
rm ~/.config/gcloud/dvc-google-service-account-key.json
```

#### Delete the Google Cloud project

To delete the Google Cloud project you created:

1. Go to the [Google Cloud Resource Manager Console](https://console.cloud.google.com/cloud-resource-manager){:target="\_blank"}.
2. Select the project you created.
3. Click on **Delete** at the top of the page.
4. Follow the instructions to shut down the project.

### Repository

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

In order to remove the packages installed with Poetry, you can run the following command:

```sh title="Execute the following command(s) in a terminal"
poetry env remove --all
```

To clean up your local environment, you can simply delete the project directory you created for this guide.

### Double-check everything

Before you finish, double-check that you have deleted all the resources and environments you created. This will ensure that you don't incur unexpected costs or leave any security vulnerabilities.

Here is a checklist of all the resources and environments you created:

- Google Cloud project
- Google Cloud Storage bucket
- Google Cloud Service Account
- Google Cloud Service Account key
- GitHub/GitLab repository
- If you used GitLab, you also created a Personal Access Token
- Project directory on your local machine

### Summary

By following these steps, you have successfully cleaned up the resources and environments you created during the guide. We hope you found this guide helpful and that it has given you a good understanding of the importance of cleaning up after yourself in cloud computing environments.

If you have any questions or concerns, please do not hesitate to contact us on [GitHub](https://github.com/csia-pme/a-guide-to-mlops){:target="\_blank"}.

## Conclusion

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
