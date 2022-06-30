import logging
import os
from functools import cache

from pydantic import AnyUrl, BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)
    database_url: AnyUrl = os.environ.get("DATABASE_URL")
    jwt_secret: str = os.environ.get("JWT_SECRET")
    jwt_algorithm: str = os.environ.get("JWT_ALGORITHM")
    jwt_expire_minutes: int = os.environ.get("JWT_EXPIRE_MINUTES")


@cache
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()
