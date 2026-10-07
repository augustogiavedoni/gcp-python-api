from typing import Annotated

from pydantic import StringConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict

NonEmptyString = Annotated[str, StringConstraints(min_length=1)]


class Settings(BaseSettings):
    app_env: str
    demo_api_key: NonEmptyString
    gcp_project_id: NonEmptyString

    model_config = SettingsConfigDict(env_file=".env")
