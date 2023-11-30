# Hack4Cure - Backend

The backend repository of our project, see the bottom of the page for the frontend. You can try our dashboard without installing through this link:

https://hack4cure.vercel.app/

## Local development

Fetch the git submodules:

```
git submodule update --init --recursive
```

Build container:

```
docker build -t hack4cure .
```

Run container with auto-reload:

```
docker run -p 127.0.0.1:7000:7000 -it -v .:/app hack4cure
```

Create migrations

```
docker exec -it <container-id> aerich migrate
```

Run migrations

```
docker exec -it <container-id> aerich upgrade
```

Every branch is available on a Jenkins deployment with the format `https://dene.sh/hack4cure/{branch}/api/`.

Check out the Swagger UI Docs on https://dene.sh/hack4cure/master/api/docs.

## Frontend repository

https://github.com/ZsombiTech/hack4cure-frontend
