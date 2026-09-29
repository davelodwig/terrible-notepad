# Terrible API — API Service (top-level)

This folder contains the API service and is self-contained: it includes a
`requirements.txt`, `dev-requirements.txt`, a `.devcontainer/` directory,
tests, and a README.

Quickstart (local):

```bash
cd api
python -m pip install -r requirements.txt
python -m pip install -r dev-requirements.txt
uvicorn app.main:app --reload
```

Database

By default the API expects a MongoDB-compatible database. The development
devcontainer will start a MongoDB instance for you automatically via
`api/.devcontainer/docker-compose.yml`.

To run the devcontainer (recommended):

1. Open the `api` folder in VS Code.
2. Run `Remote-Containers: Reopen in Container` — this starts the `dev` and
	`mongo` services via Docker Compose and sets `MONGO_URI` for the app.

Configuration

Create a `.env` file at the root of the `api` folder (you can copy
`.env.example`). The application uses Pydantic `BaseSettings` for centralized
configuration. The devcontainer will load `.env` automatically.


You can also run the Compose setup manually:

```bash
cd api/.devcontainer
docker compose up --build
```

Entrypoint and readiness

The API devcontainer uses an entrypoint script that waits for Mongo to be reachable
before starting the application. This prevents startup races when the Compose
services are brought up together. The scripts are in `.devcontainer/entrypoint.sh`
and `.devcontainer/wait-for-mongo.sh`.


Manual DB configuration

To connect to a remote MongoDB or Amazon DocumentDB-compatible service set:

```bash
export MONGO_URI="mongodb://user:pass@host:27017"
export MONGO_DB="terrible"
```

Notes
- If `MONGO_URI` is not provided the API will return HTTP 503 for data endpoints.
- Tests that require the DB are skipped unless `MONGO_URI` is set.

