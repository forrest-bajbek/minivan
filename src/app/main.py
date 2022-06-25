import logging

from fastapi import Depends, FastAPI

from app.api import ping, report, task, user
from app.auth.auth_bearer import jwtBearer

log = logging.getLogger("uvicorn")

users = []


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router, tags=["ping"])
    application.include_router(user.router, tags=["user"])
    application.include_router(
        task.router,
        # dependencies=[Depends(jwtBearer)],
        tags=["task"],
    )
    application.include_router(
        report.router,
        # dependencies=[Depends(jwtBearer)],
        tags=["report"],
    )
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
