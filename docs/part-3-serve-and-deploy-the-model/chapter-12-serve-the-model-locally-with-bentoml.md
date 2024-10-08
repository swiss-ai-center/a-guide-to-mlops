# Chapter 12 - Serve the model locally with BentoML

## Introduction

Now that the model is using [BentoML](../tools.md), enabling the extraction of
metadata upon saving, you will serve the model with the help of
[FastAPI](https://fastapi.tiangolo.com/) to create local endpoints for
interacting with the model.

In this chapter, you will learn how to:

1. Serve the model with BentoML and FastAPI
2. Push the changes to DVC and Git

The following diagram illustrates the control flow of the experiment at the end
of this chapter:

```mermaid
flowchart TB
    dot_dvc[(.dvc)] <-->|dvc pull
                         dvc push| s3_storage[(S3 Storage)]
    dot_git[(.git)] <-->|git pull
                         git push| gitGraph[Git Remote]
    workspaceGraph <-....-> dot_git
    data[data/raw]
    subgraph remoteGraph[REMOTE]
        s3_storage
        subgraph gitGraph[Git Remote]
            repository[(Repository)] --> action[Action]
            action[Action] --> |...|request[PR]
            request --> repository[(Repository)]
        end
    end
    subgraph cacheGraph[CACHE]
        dot_dvc
        dot_git
    end
    subgraph workspaceGraph[WORKSPACE]
        data --> code[*.py]
        subgraph dvcGraph["dvc.yaml"]
            code
        end
        params[params.yaml] -.- code
        subgraph bentoGraph[" "]
            bento_model[classifier.bentomodel]
            serve[serve.py] <--> bento_model
            fastapi[FastAPI] <--> |bentoml serve serve:classifierService| serve
        end
        bento_model <-.-> dot_dvc
        code <--> bento_model
    end
    subgraph browserGraph[BROWSER]
        localhost <--> fastapi
    end
    style workspaceGraph opacity:0.4,color:#7f7f7f80
    style dvcGraph opacity:0.4,color:#7f7f7f80
    style cacheGraph opacity:0.4,color:#7f7f7f80
    style data opacity:0.4,color:#7f7f7f80
    style dot_git opacity:0.4,color:#7f7f7f80
    style dot_dvc opacity:0.4,color:#7f7f7f80
    style code opacity:0.4,color:#7f7f7f80
    style params opacity:0.4,color:#7f7f7f80
    style s3_storage opacity:0.4,color:#7f7f7f80
    style repository opacity:0.4,color:#7f7f7f80
    style action opacity:0.4,color:#7f7f7f80
    style request opacity:0.4,color:#7f7f7f80
    style remoteGraph opacity:0.4,color:#7f7f7f80
    style gitGraph opacity:0.4,color:#7f7f7f80
    linkStyle 0 opacity:0.4,color:#7f7f7f80
    linkStyle 1 opacity:0.4,color:#7f7f7f80
    linkStyle 2 opacity:0.4,color:#7f7f7f80
    linkStyle 3 opacity:0.4,color:#7f7f7f80
    linkStyle 4 opacity:0.4,color:#7f7f7f80
    linkStyle 5 opacity:0.4,color:#7f7f7f80
    linkStyle 6 opacity:0.4,color:#7f7f7f80
    linkStyle 7 opacity:0.4,color:#7f7f7f80
    linkStyle 10 opacity:0.4,color:#7f7f7f80
    linkStyle 11 opacity:0.4,color:#7f7f7f80
    linkStyle 12 opacity:0.4,color:#7f7f7f80
```

## Steps

### Create the BentoML service

BentoML services allow to define the serving logic of machine learning models.

A BentoML service is a class that defines all the endpoints and the logic to
serve the model using FastAPI.

Create a new file `src/serve.py` and add the following code:

```py title="src/serve.py"
from __future__ import annotations
from bentoml.validators import ContentType
from typing import Annotated
from PIL.Image import Image
from pydantic import Field
import bentoml
import json


@bentoml.service(name="celestial_bodies_classifier")
class CelestialBodiesClassifierService:
    bento_model = bentoml.keras.get("celestial_bodies_classifier_model")

    def __init__(self) -> None:
        self.preprocess = self.bento_model.custom_objects["preprocess"]
        self.postprocess = self.bento_model.custom_objects["postprocess"]
        self.model = self.bento_model.load_model()

    @bentoml.api()
    def predict(
            self,
            image: Annotated[Image, ContentType("image/jpeg")] = Field(description="Planet image to analyze"),
    ) -> Annotated[str, ContentType("application/json")]:
        image = self.preprocess(image)

        predictions = self.model.predict(image)

        return json.dumps(self.postprocess(predictions))
```

This service will be used to serve the model with FastAPI and will do the
following:

1. The model is loaded from the BentoML model store
2. The `preprocess` function is loaded from the model's custom objects
3. The `postprocess` function is loaded from the model's custom objects
4. The `predict` method is decorated with `@bentoml.api()` to create an endpoint
5. The endpoint accepts an image as input
6. The endpoint returns a JSON response
7. The image is pre-processed
8. The predictions are made from the model
9. The predictions are post-processed and returned as a JSON string

### Serve the model

Serve the model with the following command:

```sh title="Execute the following command(s) in a terminal"
# Serve the model
bentoml serve --working-dir ./src serve:CelestialBodiesClassifierService
```

BentoML will load the model, create the FastAPI app and start it. You can then
access the auto-generated model documentation on
<http://localhost:3000>{:target="\_blank"}.

The following endpoint has been created:

- `/predict`: Upload a `png` or `jpg` image and get a prediction from the model.

You can try out predictions by inputing some images to the model through the
REST API!

### Try out the prediction endpoint

The following images are available in the `extra-data` repository that you will
use in a future chapter:
<https://github.com/swiss-ai-center/a-guide-to-mlops/tree/extra-data/extra_data>.

Here are some example you can use.

!!! warning

    Please be aware that this model is for demonstration purposes. Some inputs may
    be incorrectly predicted.

#### Moon example

Download the following image of the moon on your computer.

<figure markdown>
  ![Moon](https://raw.githubusercontent.com/swiss-ai-center/a-guide-to-mlops/extra-data/extra_data/TW9vbl8xNDU.jpg)
</figure>

Upload it to the `/predict` endpoint and check the prediction.

The output should be similar to this:

```json
{
  "prediction": "Moon",
  "probabilities": {
    "Earth": 7.035154793791354e-13,
    "Jupiter": 0.00007276538963196799,
    "MakeMake": 0.02092079259455204,
    "Mars": 0.010689028538763523,
    "Mercury": 0.023408930748701096,
    "Moon": 0.9338789582252502,
    "Neptune": 0.000002209141257480951,
    "Pluto": 0.0028652558103203773,
    "Saturn": 1.8474166695123945e-13,
    "Uranus": 1.9255971039910946e-7,
    "Venus": 0.008161773905158043
  }
}
```

#### Makemake example

Download the following image of Makemake on your computer.

<figure markdown>
  ![Makemake](https://raw.githubusercontent.com/swiss-ai-center/a-guide-to-mlops/extra-data/extra_data/TWFrZW1ha2VfMTQ2.jpg)
</figure>

Upload it to the `/predict` endpoint and check the prediction.

The output should be similar to this:

```json
{
  "prediction": "MakeMake",
  "probabilities": {
    "Earth": 1.7512833494492952e-7,
    "Jupiter": 0.041287556290626526,
    "MakeMake": 0.8213532567024231,
    "Mars": 0.0008790065185166895,
    "Mercury": 0.05630605295300484,
    "Moon": 0.07207279652357101,
    "Neptune": 0.0020877758506685495,
    "Pluto": 0.001172061893157661,
    "Saturn": 3.342878756029677e-7,
    "Uranus": 0.0000021771340925624827,
    "Venus": 0.004838812164962292
  }
}
```

#### Neptune example

Download the following image of Neptune on your computer.

<figure markdown>
  ![Neptune](https://raw.githubusercontent.com/swiss-ai-center/a-guide-to-mlops/extra-data/extra_data/TmVwdHVuZV8xNDY.jpg)
</figure>

Upload it to the `/predict` endpoint and check the prediction.

The output should be similar to this: You may notice the model got it wrong and
predicted Uranus instead!

```json
{
  "prediction": "Uranus",
  "probabilities": {
    "Earth": 1.949044925453336e-9,
    "Jupiter": 0.02630659192800522,
    "MakeMake": 0.00044166349107399583,
    "Mars": 0.0023288053926080465,
    "Mercury": 0.0007231549825519323,
    "Moon": 0.0012503587640821934,
    "Neptune": 0.3933066725730896,
    "Pluto": 0.002935060765594244,
    "Saturn": 0.0000018027430996880867,
    "Uranus": 0.5725908279418945,
    "Venus": 0.00011510706099215895
  }
}
```

### Check the changes

Check the changes with Git to ensure that all the necessary files are tracked.

```sh title="Execute the following command(s) in a terminal"
# Add all the files
git add .

# Check the changes
git status
```

The output should look like this.

```text
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
    new file:   src/serve.py
```

### Commit the changes to Git

Commit the changes to Git.

```sh title="Execute the following command(s) in a terminal"
# Commit the changes
git commit -m "BentoML can serve the model locally"

# Push the changes
git push
```

### Check the results

Congratulations! You now have a model served over a REST API!

This chapter is done, you can check the summary.

## Summary

In this chapter, you have successfully:

1. Served the model with BentoML and FastAPI
2. Pushed the changes to Git

You did fix some of the previous issues:

- [x] Model can be easily used outside of the experiment context

You could serve this model from anywhere. Additional services could submit
predictions to your model. The usage of FastAPI creates endpoints that are
automatically documented to interact with the model.

You can now safely continue to the next chapter.

## State of the MLOps process

- [x] Notebook has been transformed into scripts for production
- [x] Codebase and dataset are versioned
- [x] Steps used to create the model are documented and can be re-executed
- [x] Changes done to a model can be visualized with parameters, metrics and
      plots to identify differences between iterations
- [x] Codebase can be shared and improved by multiple developers
- [x] Dataset can be shared among the developers and is placed in the right
      directory in order to run the experiment
- [x] Experiment can be executed on a clean machine with the help of a CI/CD
      pipeline
- [x] CI/CD pipeline is triggered on pull requests and reports the results of
      the experiment
- [x] Changes to model can be thoroughly reviewed and discussed before
      integrating them into the codebase
- [x] Model can be saved and loaded with all required artifacts for future usage
- [x] Model can be easily used outside of the experiment context
- [ ] Model requires manual publication to the artifact registry
- [ ] Model is not accessible on the Internet and cannot be used anywhere
- [ ] Model requires manual deployment on the cluster
- [ ] Model cannot be trained on hardware other than the local machine

You will address these issues in the next chapters for improved efficiency and
collaboration. Continue the guide to learn how.

## Sources

Highly inspired by:

- [_Services_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/guides/services.html)
- [_Input and output types_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/guides/iotypes.html)
- [_Containerization_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/guides/containerization.html)
- [_Build options_ - docs.bentoml.com](https://docs.bentoml.com/en/latest/guides/build-options.html)
