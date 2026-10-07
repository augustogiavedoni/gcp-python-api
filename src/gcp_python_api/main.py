import logging
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI, Request

from .config import Settings
from .logging_config import configure_logging, get_trace

configure_logging()

logger = logging.getLogger(__name__)
app = FastAPI()


@lru_cache
def get_settings() -> Settings:
    return Settings()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/greet/{name}")
async def greet(
    name: str,
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict[str, str]:
    extra = {
        "endpoint": "/greet/{name}",
        "requested_name": name,
    }

    trace = get_trace(request, settings.gcp_project_id)

    if trace:
        extra["logging.googleapis.com/trace"] = trace

    logger.info("Greeting requested", extra=extra)

    return {"message": f"Hello, {name}!"}


@app.get("/environment")
async def environment(
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict[str, str]:
    return {"result": settings.app_env}


@app.get("/api-key")
async def api_key(
    settings: Annotated[Settings, Depends(get_settings)],
) -> dict[str, bool]:
    return {"is_configured": bool(settings.demo_api_key)}
