import functools
import logging

from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    redis_data_url: str
    redis_cache_url: str
    environment: str = "dev"
    testing: bool = False


@functools.cache
def get_settings() -> Settings:
    log.info("Loading config settings from the environment...")
    return Settings()
