import logging
from datetime import datetime

from aredis_om import Field, JsonModel, Migrator

from app.db import redis_data

log = logging.getLogger("uvicorn")


class BaseJsonModel(JsonModel):
    class Meta:
        database = redis_data()


class Task(BaseJsonModel):
    created_at: datetime = Field(default=...)
    updated_at: datetime = Field(default=...)
    task_app: str = Field(default=..., index=True, full_text_search=True)
    task_env: str = Field(default=..., index=True, full_text_search=True)
    task_name: str = Field(default=..., index=True, full_text_search=True)
    task_status: str = Field(default=..., index=True, full_text_search=True)
    task_watermark: datetime = Field(default=..., index=True)
    task_start_at: datetime = Field(default=...)
    task_stop_at: datetime | None = Field(default=None)
    task_metadata: dict | None = Field(default=None, index=True, full_text_search=True)


Migrator().run()
