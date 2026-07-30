# Chapter 4.5 - Review drift alerts and decide on action

## Introduction

Now that the drift alert system is in place, the monitoring workflow opens a
GitHub issue whenever drift exceeds the thresholds defined in `src/monitor.py`.
The issue records the drift score and links to the Evidently dashboard. It flags
that something changed, but the team still has to decide what to do about it.

This chapter shows how to review that issue and choose one of three actions:

1. **Dismiss and tune the thresholds** when the alert is a false positive or the
   thresholds are too sensitive.
2. **Roll back** to the last known-good model when the deployed model degrades
   in production.
3. **Label new data and retrain** when the drift reflects a real new
   distribution that the model must learn.

Because the drift thresholds live in `src/monitor.py` and the model, data, and
deployment configuration are all versioned with Git and DVC, every decision from
a threshold tweak to a full rollback or retrain is a reproducible operational
procedure rather than an ad-hoc fix.

In this chapter, you will learn how to:

1. Open and read the drift-alert issue created by the monitoring workflow
2. Decide whether to tune thresholds, roll back, or label new data and retrain
3. Adjust drift thresholds quickly in `src/monitor.py`
4. Roll back to the last known-good version with Git and DVC
5. Verify the chosen action and close the issue

The following diagram illustrates the decision flow at the end of this chapter:

```mermaid
flowchart TB
    issue[Drift-alert issue] -->|review| decision{Decision}
    decision -->|false positive| tune[Adjust thresholds]
    decision -->|model degraded| rollback[Revert commits on main]
    rollback -->|CI/CD| redeploy[Redeploy via pipeline]
    decision -->|new distribution| label[Label new data]
    label --> retrain[Retrain with DVC]
    retrain --> new_reference[Rebuild reference dataset]

    style issue opacity:0.4,color:#7f7f7f80
    style decision opacity:0.4,color:#7f7f7f80
    style tune opacity:0.4,color:#7f7f7f80
    style rollback opacity:0.4,color:#7f7f7f80
    style redeploy opacity:0.4,color:#7f7f7f80
    style label opacity:0.4,color:#7f7f7f80
    style retrain opacity:0.4,color:#7f7f7f80
    style new_reference opacity:0.4,color:#7f7f7f80
```

## Steps

### Open the drift-alert issue

The monitoring workflow labels the alert with `drift-alert`. Open your
repository in the GitHub interface and go to the **Issues** tab. If other issues
are open, filter by the `drift-alert` label to find the alert.

Click the issue to open it. The issue body contains:

* The metrics that crossed their thresholds, for example
  `image_mean: 0.2341 > 0.1500`.
* A link to the public Evidently dashboard, if `DASHBOARD_URL` was configured.
* A **Next steps** reminder to roll back, label new data, or dismiss the alert.

If this was a test alert or the drift has already been handled, click the
**Close issue** button so the next real alert is not suppressed.

### Review the evidence

The issue shows the drift scores extracted from `monitoring/report.json` and
links to the Evidently dashboard. You already inspected both in the previous
chapter, so use that review to decide which branch of the decision tree applies:

* **Noise or expected variation**: tune the thresholds.
* **Real degradation of the deployed model**: roll back.
* **A new but valid distribution**: label new data and retrain (the workflow is
  covered in Part 5).

### Option 1: Dismiss and tune the thresholds

When the alert is a false positive or the thresholds are too tight, adjust the
constants at the top of `src/monitor.py`:

```py title="src/monitor.py"
# Drift detection thresholds and methods.
DRIFT_SHARE_THRESHOLD = 0.5
NUM_DRIFT_METHOD = "wasserstein"
NUM_DRIFT_THRESHOLD = 0.3
CAT_DRIFT_METHOD = "jensenshannon"
CAT_DRIFT_THRESHOLD = 0.1
EMBEDDING_DRIFT_THRESHOLD = 0.7
```

Adjust the drift threshold values, then commit the change and close the issue:

```sh title="Execute the following command(s) in a terminal"
# Commit the adjusted thresholds
git add src/monitor.py
git commit -m "Adjust drift thresholds after reviewing extra-data alert"
git push
```

The next scheduled monitoring workflow (or manual trigger) will use the new
thresholds and only open a new issue if drift still exceeds them.

### Option 2: Roll back the deployment

If the deployed model is clearly worse than the previous version, roll back to
the last known-good version. Every commit to `main` produces a deployable image
and the DVC pointer files track the model artifact and data, so reverting `main`
and letting the CI/CD pipeline redeploy is all it takes.

#### Find the previous known-good version

The CI/CD pipeline pushes a Docker image for every commit to `main`. Each image
is tagged with the Git commit SHA, so the registry is a history of deployed
model versions.

List the available image tags in the container registry:

```sh title="Execute the following command(s) in a terminal"
# List available tags for the classifier image
gcloud artifacts docker images list \
  $GCP_CONTAINER_REGISTRY_HOST/celestial-bodies-classifier \
  --include-tags \
  --format='table(TAG)'
```

The output looks similar to this:

```text
TAG
latest
a1b2c3d4e5f6789012345678901234567890abcd
b2c3d4e5f6789012345678901234567890abcdef
c3d4e5f6789012345678901234567890abcdef01
```

The `latest` tag always points to the most recent build. The long hexadecimal
strings are Git commit SHAs. Pick the SHA just before the bad deployment; that
is your rollback target.

You can also find the same SHA in Git:

```sh title="Execute the following command(s) in a terminal"
# Show recent commits on main
git log --oneline -10 main
```

Set the rollback target once so the following commands can reuse it:

```sh title="Execute the following command(s) in a terminal"
# Replace with the SHA you picked above
export PREVIOUS_SHA=a1b2c3d4e5f6789012345678901234567890abcd
```

#### Roll back with Git and DVC

The rollback restores the exact code, model artifact, and data that produced the
previous version on `main`, so the source of truth stays consistent and the
CI/CD pipeline redeploys cleanly.

Create a new commit on `main` that reverts the bad commits since the last
known-good version, using the same commit SHA as the previous step.
`--no-commit` reverts them all at once, into a single rollback commit. This
preserves history: the bad deployment stays visible in the Git log, which keeps
the deployed state traceable. The revert also restores the DVC pointer files, so
the pipeline pulls the previous model artifact and data:

```sh title="Execute the following command(s) in a terminal"
# Revert the commits since the last known-good version
git revert --no-commit $PREVIOUS_SHA..

# Commit the rollback
git commit -m "Rollback to $PREVIOUS_SHA"

# Push the rollback to trigger the CI/CD pipeline
git push
```

After the push, the CI/CD pipeline will build and deploy the rolled-back version
automatically, bringing the container registry back into sync with Git and DVC.

After the rollback succeeds, close the drift-alert issue from the GitHub
interface and add a comment that records the action taken, for example "Rolled
back deployment to `$PREVIOUS_SHA`."

### Option 3: Label new data and retrain

Rolling back is the wrong choice when the drift reflects a real new distribution
that the previous model never saw. In that case the model needs to learn from
the new data.

The full labeling and retraining workflow is covered in Part 5. Close the
drift-alert issue once you have decided to send the new samples there.

### Verify the chosen action

Each decision has its own verification step.

For a **threshold tune**, wait for the next scheduled monitoring workflow or
trigger the workflow manually to confirm the alert no longer triggers.

For a **rollback**, confirm that the previous model is serving again by checking
the running image and sending a test prediction.

Check the deployed image:

```sh title="Execute the following command(s) in a terminal"
kubectl get deployment celestial-bodies-classifier-deployment \
  -o jsonpath='{.spec.template.spec.containers[0].image}'
```

The output should contain the rollback SHA, for example:

```text
europe-west6-docker.pkg.dev/mlops-surname-project/mlops-surname-registry/celestial-bodies-classifier:a1b2c3d4e5f6789012345678901234567890abcd
```

Find the external IP of the model service:

```sh title="Execute the following command(s) in a terminal"
# Get the external IP of the model service
kubectl get service celestial-bodies-classifier-service
```

Then send a test image to the `/predict` endpoint. Replace `<EXTERNAL-IP>` with
the value from the previous command:

```sh title="Execute the following command(s) in a terminal"
# Send a test image to the deployed model
curl -X POST -F "image=@data/raw/Mercury/Mercury_1.jpg" http://<EXTERNAL-IP>:80/predict
```

If the prediction distribution and confidence look like they did before the bad
deployment, the rollback succeeded.

For a **retrain**, verify the outcome once the Part 5 workflow is complete.

### Commit the changes

This chapter does not require manual code edits, but the rollback commands above
do change the Git history on `main`. If you chose to adjust drift thresholds
after reviewing the alert, update `src/monitor.py` and commit those changes
separately. If you sent new data to Part 5, the commits will come from that
workflow. In all cases, close the drift-alert issue from the GitHub interface
once the action is verified.

## Summary

In this chapter, you have successfully:

1. Opened and reviewed the drift-alert issue created by the monitoring workflow
2. Chose between tuning thresholds, rolling back, or labeling new data and
   retraining
3. Adjusted drift thresholds in `src/monitor.py`
4. Rolled back to the last known-good version with Git and DVC
5. Verified the chosen action and closed the issue

You fixed some of the previous issues:

- [x] Drift alerts lead to a reviewed decision

All the items of the MLOps process for this part are now addressed.

!!! abstract "Take away"

    - **A drift alert is a review ticket, not an automatic action**: the issue
      preserves the exact scores and a dashboard link so a human can decide what to do
      next.
    - **False positives are fixed by tuning thresholds**: `src/monitor.py` keeps
      thresholds, methods, and report generation in one place, so a threshold change
      propagates to both the dashboard and the CI/CD alert.
    - **Rollback is only possible because every artifact is versioned**: Git
      tracks the code, DVC tracks the model and data, and the container registry
      tracks every deployable image.
    - **The Git/DVC rollback is the canonical recovery**: it restores the source
      of truth and lets the CI/CD pipeline redeploy the old version cleanly.
    - **Real new distributions need retraining, not rollback**: Part 5 covers
      the labeling workflow.
    - **Close the issue when the decision is executed**: the alerting script
      skips creation while an open drift-alert issue exists, so a stale issue blocks
      future alerts.

## State of the MLOps process

- [x] Model predictions can be monitored in production
- [x] Data drift and concept drift are monitored
- [x] Automated reports and dashboard are configured
- [x] Drift signals trigger actionable alerts
- [x] Drift alerts lead to a reviewed decision

Continue to the conclusion to review what you have learned.

## Sources

- [_Artifact Registry: List images_ - cloud.google.com](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images)
- [_GitHub CLI: gh issue_](https://cli.github.com/manual/gh_issue)
