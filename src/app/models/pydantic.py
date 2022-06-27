from datetime import datetime, timezone

from pydantic import BaseModel, Field
from pydantic.typing import Literal


class TaskPayloadSchema(BaseModel):
    task_app: str = Field(...)
    task_env: Literal["prod", "stg", "dev"] = Field(...)
    task_name: str = Field(...)
    task_status: Literal["start", "success", "failure"] = Field(...)
    task_watermark: datetime = Field(...)
    task_start_at: datetime = Field(...)
    task_stop_at: datetime | None = Field(default=None)
    task_metadata: dict | None = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "task_app": "my app",
                "task_env": "dev",
                "task_name": "my task",
                "task_status": "success",
                "task_watermark": "2022-06-27 00:00:00.000000+00:00",
                "task_start_at": datetime.now(timezone.utc),
                "task_stop_at": datetime.now(timezone.utc),
                "task_metadata": {"key": "value", "some": ["list", "of", "items"]},
            }
        }


class TaskResponseSchema(BaseModel):
    pk: str = Field(...)

    class Config:
        schema_extra = {"example": {"pk": "01G6K6JQ5BPD6BX15MDBVP5PY4"}}
