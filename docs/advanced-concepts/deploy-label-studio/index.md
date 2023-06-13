# Label Studio

As the website of [Label Studio](https://labelstud.io/) mentions:

!!! quote

	A flexible data labeling tool for all data types. Prepare training data for computer vision, natural language processing, speech, voice, and video models.

Label Studio allows to easily annotate datasets.

## Deploy Label Studio

!!! warning

	These instructions are meant to be followed on a publicly accessible server with a domain name and a reverse proxy. For more details, have a look at the repository's `README` accessible at <https://github.com/csia-pme/a-guide-to-mlops/blob/main/infrastructure/README.md>.

Deploying Label Studio with Docker Compose is a convenient way to quickly set up and manage the application in a containerized environment. Here are the general steps you can follow:

1. Install Docker, Docker Compose and Git
2. Clone this Git repository
3. Navigate to the `infrastructure/label-studio` directory

Create the directories that we mapped in the `infrastructure/label-studio/docker-compose.yml` file:

```sh title="In a terminal, execute the following command(s)" 
mkdir label-studio-data
mkdir db-data
```

Update the FQDNs in the `infrastructure/labelstudio/.env` file to your owns.

Start the container using the following command:

```sh title="In a terminal, execute the following command(s)"
docker compose up --detach
```

This command will start the container in detached mode, which means it will run in the background.

Start the reverse proxy as well in the `infrastructure/traefik` directory.

Access the Label Studio interface by navigating to the FQDN you provided in the `.env` file in your web browser.

That's it! You should now be able to access and use Label Studio. You can also stop the container using the following command:

```sh title="In a terminal, execute the following command(s)"
docker compose down
```

This will stop and remove the container.
