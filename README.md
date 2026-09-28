# GCP Python API

A small Python API built with FastAPI as part of my transition into backend, cloud, and AI engineering.

The goal of this repository is to progressively build a production-ready service and use it as a hands-on environment for learning Python, FastAPI, Google Cloud, deployment, observability, and related backend concepts.

## Current Features

- Health check endpoint
- Greeting endpoint with a path parameter
- Local development with FastAPI CLI
- Dependency management with `uv`

## Tech Stack

- Python
- FastAPI
- uv

## Project Structure

```text
gcp-python-api/
├── pyproject.toml
├── README.md
├── uv.lock
└── src/
    └── gcp_python_api/
        ├── __init__.py
        └── main.py
```

## Getting Started

### Prerequisites

- Python
- [uv](https://docs.astral.sh/uv/)

### Install dependencies

```bash
uv sync
```

### Run the application

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

## Endpoints

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

## Roadmap

This repository will evolve incrementally as I explore production backend and cloud engineering concepts.

- [x] Bootstrap FastAPI application
- [x] Add basic endpoints
- [ ] Add automated tests
- [ ] Containerize with Docker
- [ ] Deploy to Google Cloud Run
- [ ] Add environment-based configuration
- [ ] Integrate Secret Manager
- [ ] Add structured logging
- [ ] Add monitoring and observability
- [ ] Add CI/CD
- [ ] Manage infrastructure as code
- [ ] Explore additional Google Cloud services

## Purpose

This is intentionally a learning-oriented project.

Rather than starting with a complex application, the repository will grow step by step, with each iteration introducing a new backend, cloud, or production engineering concept.