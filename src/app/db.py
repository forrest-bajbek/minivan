import logging

import aioredis
import aredis_om
from redis import Redis

from app.config import get_settings

log = logging.getLogger("uvicorn")

settings = get_settings()


def redis_data() -> Redis:
    return aredis_om.get_redis_connection(
        url=settings.redis_data_url,
        encoding="utf8",
        decode_responses=True,
    )


def redis_cache() -> Redis:
    return aioredis.from_url(
        url=settings.redis_cache_url,
        encoding="utf8",
        decode_responses=True,
    )
