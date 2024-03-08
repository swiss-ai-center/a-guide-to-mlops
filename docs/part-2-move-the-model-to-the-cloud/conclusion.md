---
title: "Part 2 - Conclusion"
---

# Conclusion

Congratulations! You did it!

In this second part, you were able to share your experiment on the cloud and
with your peers. A new team member can easily clone the repository and reproduce
the experiment locally. The experiment is also reproducible on the cloud and
ensures it still works in a different environment. Once the experiment is
reproduced, the results are published and shared with the team. You can also
compare the results with the previous ones and decide if you want to merge the
new model or not.

The following diagram illustrates the bricks you set up at the end of this part:

```mermaid
flowchart LR
	dot_dvc[(.dvc)] -->|dvc push| s3_storage[(S3 Storage)]
	s3_storage -->|dvc pull| dot_dvc
	dot_git[(.git)] -->|git push| gitGraph[Git Remote]
	gitGraph -->|git pull| dot_git
    workspaceGraph <-....-> dot_git
	data[data/raw] <-.-> dot_dvc
    subgraph remoteGraph[REMOTE]
        s3_storage
        subgraph gitGraph[Git Remote]
            repository[(Repository)] --> action[Action]
            action -->|dvc pull| action_data[data/raw]
            action_data -->|dvc repro| action_out[metrics & plots]
            action_out -->|cml publish| pr[Pull Request]
            pr --> repository
        end
	end
	subgraph cacheGraph[CACHE]
		dot_dvc
		dot_git
	end
	subgraph workspaceGraph[WORKSPACE]
		prepare[prepare.py] <-.-> dot_dvc
		train[train.py] <-.-> dot_dvc
		evaluate[evaluate.py] <-.-> dot_dvc
		data --> prepare
		subgraph dvcGraph["dvc.yaml (dvc repro)"]
			prepare --> train
			train --> evaluate
		end
        params[params.yaml] -.- prepare
        params -.- train
        params <-.-> dot_dvc
	end
```

Do not forget to [Clean up](./clean-up.md) if you want to stop here or continue
with
[Part 3 - Serve and deploy the model](../part-3-serve-and-deploy-the-model/introduction.md)
of the MLOps guide!
