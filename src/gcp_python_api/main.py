from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI

from .config import Settings

app = FastAPI()


@lru_cache
def get_settings() -> Settings:
    return Settings()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/greet/{name}")
async def greet(name: str) -> dict[str, str]:
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
