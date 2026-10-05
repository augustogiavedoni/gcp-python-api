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
- Continuous integration with GitHub Actions
- Automated deployment to Cloud Run from `main`
- Environment-based configuration with Pydantic Settings
- Demo secret configuration without exposing secret values
- Structured application logging using Python's standard `logging` module
- JSON logs compatible with Google Cloud Logging

## Tech Stack

- Python 3.14
- FastAPI
- uv
- Docker
- Google Artifact Registry
- Google Cloud Run
- Pydantic Settings
- Python logging
- Google Cloud Logging

## Project Structure

```text
gcp-python-api/
├── .dockerignore
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── Dockerfile
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
├── uv.lock
├── src/
│   └── gcp_python_api/
│       ├── __init__.py
|       ├── config.py
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

Returns the health status of the application.

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

Returns a greeting for the provided name.

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

### Environment

Returns the environment in which the application is running.

```http
GET /environment
```

Example:

```http
GET /environment
```

Response:

```json
{
  "result": "development"
}
```

### API key configuration

Checks whether the demo API key is configured without exposing its value.

```http
GET /api-key
```

Example:

```http
GET /api-key
```

Response:

```json
{
  "is_configured": true
}
```

## Configuration

Application configuration is managed with `pydantic-settings`.

The application currently uses the following settings:

| Variable | Description | Example |
| --- | --- | --- |
| `APP_ENV` | Environment in which the application is running | `development` |
| `DEMO_API_KEY` | Demo secret used to validate secret configuration | `local-demo-key` |

For local development, create a `.env` file in the project root:

```env
APP_ENV=development
DEMO_API_KEY=local-demo-key
```

The `.env` file is excluded from both Git and the Docker build context.

In deployed environments, configuration is provided at runtime rather than being included in the container image. Cloud Run provides `APP_ENV` as an environment variable when the container starts.

Environment variables take precedence over values defined in `.env`, allowing the same application and container image to be configured differently across environments.

In Cloud Run, sensitive configuration such as `DEMO_API_KEY` is provided through Google Cloud Secret Manager and made available to the application at runtime.

## Logging

The application uses Python's standard `logging` module and emits structured JSON logs to stdout.

When running on Cloud Run, container output is automatically collected by Google Cloud Logging. Structured JSON entries are stored as `jsonPayload`, allowing fields such as `severity`, `message`, and other contextual attributes to be queried independently.

No Google Cloud logging SDK is required for the current setup.

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

## CI/CD

The repository uses GitHub Actions for continuous integration and deployment.

### Continuous Integration

Pull requests targeting `main` run the CI workflow, which:

1. Checks out the repository
2. Installs Python and `uv`
3. Installs project and development dependencies
4. Runs the automated test suite
5. Validates that the Docker image can be built

This prevents changes from being merged without first validating the application.

### Continuous Deployment

Pushes to `main` run the deployment workflow.

The deployment pipeline:

```text
Push to main
    ↓
Run automated tests
    ↓
Authenticate to Google Cloud
    ↓
Build Docker image
    ↓
Push image to Artifact Registry
    ↓
Deploy image to Cloud Run
    ↓
Create new Cloud Run revision
```

Docker images are tagged with the Git commit SHA, providing traceability between source code, container images, and Cloud Run revisions.

### Google Cloud Authentication

GitHub Actions authenticates to Google Cloud using Workload Identity Federation.

This avoids storing long-lived Google Cloud service account keys in GitHub.

The deployment and runtime identities are intentionally separated:

```text
GitHub Actions service account
    ↓
Deploys the service

Cloud Run runtime service account
    ↓
Runs the application
```

The deployment identity is authorized to deploy new Cloud Run revisions and to act as the runtime service account during deployment.

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
- [x] Add CI/CD
- [x] Add environment-based configuration
- [x] Integrate Secret Manager
- [x] Add structured logging
- [ ] Add monitoring and observability
- [ ] Manage infrastructure as code
- [ ] Explore additional Google Cloud services
- [ ] Introduce AI workloads with Vertex AI

## Purpose

This repository is intentionally small.

Rather than starting with a complex application, each iteration introduces a specific backend, cloud, or production engineering concern while keeping the underlying service simple enough to make the infrastructure and architectural decisions easy to understand.
