import logging

from fastapi import FastAPI

from app.api import ping, report, task, user

log = logging.getLogger("uvicorn")

users = []


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router, tags=["ping"])
    application.include_router(user.router, tags=["user"])
    application.include_router(task.router, tags=["task"])
    application.include_router(report.router, tags=["report"])
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
