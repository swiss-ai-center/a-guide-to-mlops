# Chapter 7: Move the ML experiment code to the cloud

## Introduction

At this point, the data is made available to team members using DVC, but the
experiment codebase itself is not.

By linking your local project to a remote repository on platforms like GitHub
or GitLab, you can seamlessly push, pull, and synchronize changes, facilitating
collaboration and ensuring smooth workflow.

```mermaid
flowchart LR
	789994[(".dvc")] -->|"dvc push"| 574108[("S3 Storage")]
	574108 -->|"dvc pull"| 789994
	429113[(".git")] -->|"git push"| 723944["Git Remote"]
	723944 -->|"git pull"| 429113
    356399 <-....-> 429113
	980408["data"] <-.-> 789994
	subgraph 438901["CACHE"]
		789994
		429113
	end
	subgraph 356399["LOCAL"]
		672354["prepare.py"] <-.-> 789994
		347464["train.py"] <-.-> 789994
		964259["evaluate.py"] <-.-> 789994
		980408 --> 672354
		subgraph 695374["dvc.yaml"]
			672354 --> 347464
			347464 --> 964259
		end
        238472["params.yaml"] -.- 672354
        238472 -.- 347464
        238472 <-.-> 789994
	end
	subgraph 935111["CLOUD"]
		574108
		subgraph 723944["Git Remote"]
			386452["Repository"]
		end
	end
    style 238472 opacity:0.4,color:#7f7f7f80
    style 789994 opacity:0.4,color:#7f7f7f80
    style 980408 opacity:0.4,color:#7f7f7f80
    style 438901 opacity:0.4,color:#7f7f7f80
    style 356399 opacity:0.4,color:#7f7f7f80
    style 672354 opacity:0.4,color:#7f7f7f80
    style 347464 opacity:0.4,color:#7f7f7f80
    style 964259 opacity:0.4,color:#7f7f7f80
    style 695374 opacity:0.4,color:#7f7f7f80
    style 574108 opacity:0.4,color:#7f7f7f80
    linkStyle 0 opacity:0.4,color:#7f7f7f80
    linkStyle 1 opacity:0.4,color:#7f7f7f80
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
```

## Create a remote Git repository

Create a Git repository on your preferred service to collaborate with peers.

=== ":simple-github: GitHub"

    Create a new GitHub repository for this chapter by accessing <https://github.com/new>. Configure the repository as you wish but **do not** check the box _"Add a README file"_.

=== ":simple-gitlab: GitLab"

    Create a new GitLab blank project for this chapter by accessing <https://gitlab.com/projects/new>. Configure the repository as you wish but **do not** check the box _"Initialize repository with a README"_.

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

# Set remote origin
git branch --set-upstream origin main

# Push the changes
git push
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

- ✅ Notebook has been transformed into scripts for production
- ✅ Codebase and dataset are versioned
- ✅ Steps used to create the model are documented and can be re-executed
- ✅ Changes done to a model can be visualized with parameters, metrics and plots to identify
differences between iterations
- ✅ Dataset can be shared among the developers and is placed in the right
directory in order to run the experiment
- ✅ Codebase can be shared and improved by multiple developers
- ❌ Experiment may not be reproducible on other machines
- ❌ Changes to model are not thoroughly reviewed and discussed before integration
- ❌ Model may have required artifacts that are forgotten or omitted in saved/loaded state
- ❌ Model cannot be easily used from outside of the experiment context

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources
