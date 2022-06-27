import logging
import os

import aioredis
import aredis_om

log = logging.getLogger("uvicorn")


def get_redis_connection_data():
    return aredis_om.get_redis_connection(
        url="{base_url}/{db}".format(
            base_url=os.getenv("REDIS_DATA_URL"),
            db=int(os.getenv("TESTING", 0)),
        ),
        encoding="utf8",
        decode_responses=True,
    )


def get_redis_connection_cache():
    return aioredis.from_url(
        url="{base_url}/{db}".format(
            base_url=os.getenv("REDIS_CACHE_URL"),
            db=int(os.getenv("TESTING", 0)),
        ),
        encoding="utf8",
        decode_responses=True,
    )
