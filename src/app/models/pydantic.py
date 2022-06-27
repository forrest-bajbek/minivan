from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class TaskPayloadSchema(BaseModel):
    task_app: str = Field(
        ...,
        description="Name of the app that is running the task.",
    )
    task_env: str = Field(
        ...,
        description="Environment in which the app is running (ie prod, stg, dev)",
    )
    task_name: str = Field(
        ...,
        description="Name of the task.",
    )
    task_status: str = Field(
        ...,
        description="Status of the task.",
    )
    task_watermark: datetime = Field(
        ...,
        description="Status of the task.",
    )
    task_start_at: datetime = Field(
        ...,
        description="Timestamp at which task started.",
    )
    task_stop_at: datetime | None = Field(
        default=None,
        description="Timestamp at which task stopped.",
    )
    task_metadata: dict | None = Field(
        default=None,
        description="Metadata about the task, specific to the app",
    )

    class Config:
        example = {
            "demo": {
                "task_app": "test_app",
                "task_env": "production",
                "task_name": "test_database.test_table",
                "task_status": "success",
                "task_watermark": "2022-06-26T00:00:00.000000",
                "task_start_at": "2022-06-26T03:25:32.099222",
                "task_stop_at": "2022-06-26T03:35:35.099222",
                "task_metadata": {
                    "database": "test_database",
                    "instance": "test_instance",
                    "table": "test_table",
                    "source_location": "mysql",
                    "target_location": "s3://test_location",
                },
            }
        }


class TaskResponseSchema(TaskPayloadSchema):
    id: int
    created_at: datetime
    updated_at: datetime
