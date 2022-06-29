from datetime import datetime, timezone, timedelta

from pydantic import BaseModel, Field
from pydantic.typing import Literal


class TaskPayloadSchema(BaseModel):
    task_app: str = Field(...)
    task_env: Literal["prod", "stg", "dev"] = Field(...)
    task_name: str = Field(...)
    task_status: Literal["start", "success", "failure"] = Field(...)
    task_watermark: datetime = Field(...)
    task_duration: float | None = Field(default=None)
    task_metadata: dict | None = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "task_app": "my app",
                "task_env": "dev",
                "task_name": "my task",
                "task_status": "success",
                "task_watermark": "2022-06-27T00:00:00.000000+00:00",
                "task_duration": 402.13,
                "task_metadata": {"key": "value", "some": ["list", "of", "items"]},
            }
        }


class TaskPayloadResponseSchema(BaseModel):
    id: int = Field(...)

    class Config:
        schema_extra = {"example": {"id": 1}}
