from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "LIFE RPG ENGINE API"
    environment: str = "local"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./life_rpg_engine.db"
    log_level: str = "INFO"
    auth_secret_key: str = "dev-secret-change-me"
    auth_access_token_expire_minutes: int = 10080

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
