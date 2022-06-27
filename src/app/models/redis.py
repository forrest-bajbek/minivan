from datetime import datetime

from aredis_om import Field, JsonModel

from app.db import get_redis_connection_data


class Task(JsonModel):
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

    class Meta:
        database = get_redis_connection_data()
