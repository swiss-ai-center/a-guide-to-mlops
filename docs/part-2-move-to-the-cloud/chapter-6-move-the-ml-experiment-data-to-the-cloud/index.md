# Chapter 6: Move the ML experiment data to the cloud

## Introduction

Now that we have a local Git repository and can reproduce the experiment with
DVC, let's set up a remote repository for effortless collaboration with the team.

By linking your local project to a remote repository on platforms like GitHub
or GitLab, you can seamlessly push, pull, and synchronize changes, facilitating
collaboration and ensuring smooth workflow.

## Create a remote Git repository

Create a Git repository on your preferred service to collaborate with peers.

!!! warning

    **Do not initialize the Git repository online**. You will manually
    initialize the repository later.

=== ":simple-github: GitHub"

    Follow the related documentation [_Creating a new repository_ -
    docs.github.com](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
    to create a new GitHub repository for this chapter.

=== ":simple-gitlab: GitLab"

    Follow the related documentation [_Create a project_ -
    docs.gitlab.com](https://docs.gitlab.com/ee/user/project/)
    to create a new GitLab project for this chapter.

## Configure Git for the remote branch

Add the remote origin to your repository. Your Git service should provide these
instructions as well.

```sh title="Execute the following command(s) in a terminal"
# Add the remote origin
git remote add origin <your git repository url>
```

## Push the changes to Git

Set the remote as the upstream branch and push the changes to Git.

```sh title="Execute the following command(s) in a terminal"

# Push the changes
git push --set-upstream origin main
```

After setting the upstream branch, you can simply use `git push` and `git pull`
without additional arguments to interact with the remote branch.

## Check the results

Go to your online Git repository and you will be able to view the files that are stored there.

This chapter is now complete. Please review the summary for a recap of the key points.

## Summary

Congrats! You now have a codebase that can be used and shared among the team.

In this chapter, you have successfully:

1. Set up a remote Git repository
2. Added the remote to your local git repository
3. Pushed your changes to the remote Git repository

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
