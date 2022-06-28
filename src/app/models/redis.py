import logging
from datetime import datetime

from aredis_om import Field, JsonModel

from app.db import redis_data

log = logging.getLogger("uvicorn")


class BaseJsonModel(JsonModel):
    class Meta:
        database = redis_data()


class Task(BaseJsonModel):
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)
    task_app: str = Field(...)
    task_env: str = Field(...)
    task_name: str = Field(...)
    task_status: str = Field(...)
    task_watermark: datetime = Field(...)
    task_start_at: datetime = Field(...)
    task_stop_at: datetime | None = Field(default=None)
    task_metadata: dict | None = Field(default=None)
