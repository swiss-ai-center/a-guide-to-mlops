# CML: Cannot create a runner every time

## Observations

CML uses Terraform to create a runner on Kubernetes. From time to time, the creation of this runner does not work. The pipeline attempts to create the runner and fails. An example can be found here: <https://git-ext.iict.ch/aii4.0/ml-ops-example/-/jobs/852>. Even with debugging on, I was not able to find the root cause of the problem. Re-running the pipeline solves the problem and is stable for a time before failing again.

## Implications

The pipeline fails and must be ran again. It is time consuming and unreliable.

## Ideas considered

View the logs on the Kubernetes cluster to identify the problem.
