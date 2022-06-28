import logging

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.api import ping, task
from app.db import redis_cache

# from fastapi.middleware.cors import CORSMiddleware

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router, tags=["ping"])
    application.include_router(task.router, tags=["task"])
    return application


app = create_application()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:8000"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    r = redis_cache()
    FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
