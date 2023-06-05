# Chapter 6: Move the ML experiment data to the cloud

## Create a new Git repository

Create an Git repository to collaborate with peers on your preferred Git
service.

!!! warning

    **Do not initialize the Git repository online**. You will manually
    initialize the repository later.

=== ":simple-github: GitHub"

    Follow the related documentation [_Creating a new repository_ -
    docs.github.com](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
    to create a new GitHub repository for this chapter.

=== ":simple-gitlab: GitLab"

    Follow the related documentation [_Create a project_ -
    docs.gitlab.com](https://docs.gitlab.com/ee/user/project/working_with_projects.html#create-a-project)
    to create a new GitLab project for this chapter.

## Push the changes to Git

Push the changes to Git.

```sh title="Execute the following command(s) in a terminal"

# Push the changes
git push --set-upstream origin main
```

## Check the results

Go to your online Git repository and you will be able to view the files that are stored there.

This chapter is now complete. Please review the summary for a recap of the key points.

## Summary

Congrats! You now have a codebase that can be used and shared among the team.

In this chapter, you have successfully:

1. Set up a new Git repository
2. Initialized Git in your project directory
3. Verified Git tracking for your files
4. Excluded experiment results, data, models and Python environment files from
Git commits
5. Pushed your changes to the Git repository

You fixed some of the previous issues:

- ✅ Codebase no longer needs manual download and is versioned

Another member of your team can easily clone the experiment
with the following commands.

```sh title="Execute the following command(s) in a terminal"
# Clone the Git repository
git clone <your git repository url>
```

You can now safely continue to the next chapter.

## State of the MLOps process

!!! bug

    `[TBD]`
