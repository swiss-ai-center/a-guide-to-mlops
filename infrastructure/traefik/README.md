# Traefik

## Introduction

Traefik is the reverse proxy used to access all the apps.

## Additional configuration

You must create the `acme.json` file prior to run the container.

```sh
# Create ACME file
touch acme.json

# Set the right permissions
chmod 0600 acme.json
```

You might want to change the email address defined in the `traefik.yaml` file.

You might also want to edit the FQDN in the `.env` file and uncomment external
HTTP/HTTPS configuration in `docker-compose.yaml` file to enable access.

## Additional resources

- [Traefik](https://containo.us/traefik/) - Open-source Edge Router that makes
  publishing your services a fun and easy experience.
