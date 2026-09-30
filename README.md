# GCP Python API

A small FastAPI service built to explore backend and cloud engineering practices on Google Cloud.

The project evolves incrementally, introducing containerization, deployment, testing, CI/CD, observability, infrastructure as code, and other production-oriented concepts over time.

## Current Features

- Health check endpoint
- Greeting endpoint with path parameter validation
- Local development with FastAPI
- Dependency management with `uv`
- Automated API tests with `pytest` and FastAPI `TestClient`
- Containerization with Docker
- Container images stored in Google Artifact Registry
- Deployment to Google Cloud Run

## Tech Stack

- Python 3.14
- FastAPI
- uv
- Docker
- Google Artifact Registry
- Google Cloud Run

## Project Structure

```text
gcp-python-api/
├── .dockerignore
├── Dockerfile
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
├── uv.lock
├── src/
│   └── gcp_python_api/
│       ├── __init__.py
│       └── main.py
└── tests/
    └── test_main.py
```

## Getting Started

### Prerequisites

For local development:

- Python 3.14+
- [uv](https://docs.astral.sh/uv/)

For running the container:

- Docker

### Install dependencies

```bash
uv sync
```

### Run locally

```bash
uv run fastapi dev
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Greet

```http
GET /greet/{name}
```

Example:

```http
GET /greet/Augusto
```

Response:

```json
{
  "message": "Hello, Augusto"
}
```

## Testing

Tests are written with `pytest` and FastAPI's `TestClient`.

Run the test suite with:

```bash
uv run pytest
```

The current test suite validates:

- Successful health check responses
- Greeting endpoint responses

Tests are kept separate from the application source under the `tests/` directory.

## Dependency Management

`uv` is the source of truth for project dependencies.

Dependencies are managed through:

```text
pyproject.toml
    ↓
uv.lock
```

The Docker image currently installs dependencies with `pip`, so the locked dependencies are exported to `requirements.txt` before building the image:

```bash
uv export \
  --format requirements-txt \
  --no-dev \
  --no-emit-project \
  --output-file requirements.txt
```

`requirements.txt` is therefore a generated build artifact and should be regenerated whenever `uv.lock` changes.

## Docker

### Build the image

Cloud Run requires a Linux AMD64-compatible image:

```bash
docker build \
  --platform linux/amd64 \
  -t gcp-python-api .
```

### Run locally

```bash
docker run --rm \
  -p 8080:8080 \
  gcp-python-api
```

The containerized API will be available at:

```text
http://localhost:8080
```

You can also override the port:

```bash
docker run --rm \
  -e PORT=9000 \
  -p 9000:9000 \
  gcp-python-api
```

The application listens on `0.0.0.0` and uses the `PORT` environment variable, matching the runtime expectations of Google Cloud Run.

## Google Cloud

The container image is stored in Google Artifact Registry and deployed to Google Cloud Run.

The deployment flow is:

```text
Source code
    ↓
Docker image
    ↓
Artifact Registry
    ↓
Cloud Run
    ↓
HTTPS service
```

Each deployment to Cloud Run creates an immutable revision of the service.

## Roadmap

- [x] Bootstrap FastAPI application
- [x] Add basic endpoints
- [x] Add automated tests
- [x] Containerize with Docker
- [x] Publish container image to Artifact Registry
- [x] Deploy to Google Cloud Run
- [ ] Add CI/CD
- [ ] Add environment-based configuration
- [ ] Integrate Secret Manager
- [ ] Add structured logging
- [ ] Add monitoring and observability
- [ ] Manage infrastructure as code
- [ ] Explore additional Google Cloud services
- [ ] Introduce AI workloads with Vertex AI

## Purpose

This repository is intentionally small.

Rather than starting with a complex application, each iteration introduces a specific backend, cloud, or production engineering concern while keeping the underlying service simple enough to make the infrastructure and architectural decisions easy to understand.
