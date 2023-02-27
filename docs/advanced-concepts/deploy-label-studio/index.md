# Deploy Label Studio

Deploying Label Studio with Docker Compose is a convenient way to quickly set up and manage the application in a containerized environment. Here are the general steps you can follow:

1. Install Docker and Docker Compose on your local machine or server.
2. Clone this Git repository
3. Navigate to the `infrastructure/label-studio` directory

Create the two directories that we mapped in the `infrastructure/label-studio/docker-compose.yml` file:

```sh title="In a terminal, execute the following command(s)" 
mkdir label-studio-data
mkdir db-data
```

Start the container using the following command:

```sh title="In a terminal, execute the following command(s)"
docker compose up --detach
```

This command will start the container in detached mode, which means it will run in the background.

Access the Label Studio interface by navigating to <http://localhost:8080> in your web browser.

That's it! You should now be able to access and use Label Studio. You can also stop the container using the following command:

```sh title="In a terminal, execute the following command(s)"
docker compose down
```

This will stop and remove the container.

You can start Traefik as well in the `infrastructure/traefik` directory to access Label Studio with a domain name. Edit your FQDN in the `infrastructure/label-studio/.env` file.
