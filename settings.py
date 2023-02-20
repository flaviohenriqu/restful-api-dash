from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    dsn_url: str
    dsn_sync_url: str

    app_name: str = "Athenian Dashboard API"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
