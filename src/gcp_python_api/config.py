from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str

    model_config = SettingsConfigDict(env_file=".env")
