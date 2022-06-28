import logging

import aioredis
import aredis_om
from redis import Redis

from app.config import get_settings

log = logging.getLogger("uvicorn")

settings = get_settings()


def redis_data(testing: bool = False) -> Redis:
    return aredis_om.get_redis_connection(
        url=f"{settings.redis_data_url}/{int(testing)}",
        encoding="utf8",
        decode_responses=True,
    )


def redis_cache(testing: bool = False) -> Redis:
    return aioredis.from_url(
        url=f"{settings.redis_cache_url}/{int(testing)}",
        encoding="utf8",
        decode_responses=True,
    )
