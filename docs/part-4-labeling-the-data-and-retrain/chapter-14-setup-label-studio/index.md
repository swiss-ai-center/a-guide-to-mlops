# Chapter 14: Setup Label Studio

??? info "You want to take over from this chapter? Collapse this section and follow the instructions below."

    _Work in progress._

    [//]: # "TODO"

!!! warning "This is a work in progress"

    This chapter is a work in progress. Please check back later for updates. Thank
    you!

## Introduction

[Label Studio](../../tools) is an open-source data labeling tool that is
designed to help streamline the process of labeling data for machine learning.
It provides a user-friendly interface for annotating data, as well as a variety
of features for managing and organizing labeled data.

Label Studio supports a wide range of data types and annotation types, including
text, image, and audio data, as well as classification, segmentation, and entity
recognition annotations. It also allows users to create custom annotation types
and workflows, which can be useful for specific machine learning tasks.

Some of the key features of Label Studio include:

- **User-friendly interface**: Label Studio provides a simple and intuitive
    interface for annotating data, which can help to reduce errors and improve
    efficiency.
- **Customizable workflows**: Label Studio allows users to create custom
  workflows
    for data labeling, which can be tailored to specific machine learning tasks.
- **Collaboration tools**: Label Studio provides tools for collaborating on data
    labeling tasks, such as assigning tasks to different users and reviewing and
    approving annotations.
- **Integration with ML frameworks**: Label Studio can be integrated with popula
    machine learning frameworks, such as TensorFlow, PyTorch, and Keras, which can
    help to streamline the process of training and deploying machine learning
    models.

Overall, Label Studio is a powerful and flexible tool for data labeling that can
help to improve the accuracy and efficiency of machine learning models, while
reducing the time and cost of data labeling.

Let's imagine new data related to our experiment were provided. However, this
additional data is not tagged with labels defining which planet or moon
corresponds to the new item.

An expert would need to visualize all the new items and tag them manually,
identifying which celestial body the item is. Other experts could help to
labelize the data as well, adding missing tags, fixing mislabeled items and
enhancing existing data.

After making use of Label Studio to manually annotate additional data, it will
be reinjected in the model for retraining, which will then improve the
performance of the model.

In this chapter, you will learn how to:

1. Install Docker
1. Install Label Studio
1. Create a Label Studio project

Let's get started!

## Steps

### Install Docker

Because LabelStudio requires several moving parts (nginx server, PostgreSQL
database) and a specific Python version, we will use
[Docker](https://www.docker.com/) to set it up in a simple manner.

Start by downloading and installing Docker.

Ensure the docker service is started:

```
sudo systemctl start docker
```

Check the status of the docker service with:

```
sudo systemctl status docker
```

!!! todo
    TODO: check commands on macOS. Use Docker compose client on windows?

### Install Label Studio

Create a `docker-compose.yml` file in a `labelstudio` directory with the
following content:

!!! todo
    Simply download from a repo. This docker setup is irrelevant for the experiment
    itself.

```
version: "3.9"
services:
  nginx:
    build: .
    image: heartexlabs/label-studio:latest
    restart: unless-stopped
    ports:
      - "8080:8085"
      - "8081:8086"
    depends_on:
      - app
    environment:
      - LABEL_STUDIO_HOST=${LABEL_STUDIO_HOST:-}
    #   Optional: Specify SSL termination certificate & key
    #   Just drop your cert.pem and cert.key into folder 'deploy/nginx/certs'
    #      - NGINX_SSL_CERT=/certs/cert.pem
    #      - NGINX_SSL_CERT_KEY=/certs/cert.key
    volumes:
      - ./mydata:/label-studio/data:rw
      - ./deploy/nginx/certs:/certs:ro
    #   Optional: Override nginx default conf
    #      - ./deploy/my.conf:/etc/nginx/nginx.conf
    command: nginx

app:
  stdin_open: true
  tty: true
  build: .
  image: heartexlabs/label-studio:latest
  restart: unless-stopped
  expose:
    - "8000"
  depends_on:
    - db
  environment:
    - DJANGO_DB=default
    - POSTGRE_NAME=postgres
    - POSTGRE_USER=postgres
    - POSTGRE_PASSWORD=
    - POSTGRE_PORT=5432
    - POSTGRE_HOST=db
    - LABEL_STUDIO_HOST=${LABEL_STUDIO_HOST:-}
    - JSON_LOG=1
  #      - LOG_LEVEL=DEBUG
  volumes:
    - ./mydata:/label-studio/data:rw
  command: label-studio-uwsgi

db:
  image: postgres:11.5
  hostname: db
  restart: unless-stopped
  # Optional: Enable TLS on PostgreSQL
  # Just drop your server.crt and server.key into folder 'deploy/pgsql/certs'
  # NOTE: Both files must have permissions u=rw (0600) or less
  #    command: >
  #      -c ssl=on
  #      -c ssl_cert_file=/var/lib/postgresql/certs/server.crt
  #      -c ssl_key_file=/var/lib/postgresql/certs/server.key
  environment:
    - POSTGRES_HOST_AUTH_METHOD=trust
  volumes:
    - ${POSTGRES_DATA_DIR:-./postgres-data}:/var/lib/postgresql/data
    - ./deploy/pgsql/certs:/var/lib/postgresql/certs:ro
```

The application will run using a non-root docker user with ID `1001`. In order
to adjust the required permissions, enter:

    docker run -it --user root -v `pwd`/mydata:/label-studio/data
    heartexlabs/label-studio:latest chown -R 1001:root /label-studio

And start Docker Compose with:

    docker compose up

You can then open the Label Studio web interface at
[localhost:8080](https://localhost:8080).

### Create a Label Studio project

Create a new project by going to the Label Studio web interface, select
**Create Project** in the center of the screen. Name your project (MLOps
example) then select **Labeling Setup**.

In **Structured Data Parsing**, select **Tabular Data**. Toggle the **Code**
option and paste the following snippet.

```
<View>
    <Image name="image" value="$image"/>
    <Choices name="choice" toName="image">
        <Choice value="Mercury"/>
        <Choice value="Venus"/>
        <Choice value="Earth"/>
        <Choice value="Moon"/>
        <Choice value="Mars"/>
        <Choice value="Jupiter"/>
        <Choice value="Saturn"/>
        <Choice value="Uranus"/>
        <Choice value="Neptune"/>
        <Choice value="Pluto"/>
        <Choice value="Makemake"/>
    </Choices>
</View>
```

This will create a simple menu to select the categaory of a celestial body.
Select **Save** to save the project.

You have now configured a Label Studio project that will allow to import
existing data with their labels and labelize new data using the web interface.

## Summary

In this chapter, you have successfully:

1. Installed Docker
2. Launched Docker service
1. Installed Label Studio
2. Created a Label Studio project adapted to our experiment

You can now safely continue to the next chapter.

## State of the MLOps process

- ❌ Dataset cannot be improved easily by labeling to improve the model's
  performance
- ❌ Model cannot be retrained easily with improved dataset
- ❌ Model prediction cannot be used in the annotation process

## Sources

Highly inspired by:

* [Import pre-annotated data into Label Studio - labelstud.io](https://labelstud.io/guide/predictions.html)
* [Install and upgrade - labelstud.io](https://labelstud.io/guide/install.html#Install-with-Docker)
