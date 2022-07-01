import logging

from fastapi import Depends, FastAPI

from app.auth.auth_bearer import JWTBearer
from app.db import init_db
from app.internal import admin
from app.routers import ping, task, user

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(ping.router)
    application.include_router(admin.router)
    application.include_router(user.router)
    application.include_router(task.router)

    return application


app = create_application()


@app.get("/")
async def root():
    return {"message": "Welcome to minivan!"}


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
