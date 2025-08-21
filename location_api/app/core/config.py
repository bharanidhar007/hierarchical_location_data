from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    ENV: str = "dev"
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "Location API"
    SECRET_KEY: str = "dev"
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/locations"
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 60
    ENABLE_GRAPHQL: bool = True
    USE_POSTGIS: bool = True
    DEFAULT_LOCALE: str = "en"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
