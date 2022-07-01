from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.enums import TaskEnvEnum, TaskStatusEnum, UserCategoryEnum


class TaskPayloadSchema(BaseModel):
    task_app: str = Field(...)
    task_env: TaskEnvEnum = Field(...)
    task_name: str = Field(...)
    task_status: TaskStatusEnum = Field(...)
    task_watermark: datetime = Field(...)
    task_duration: float | None = Field(default=None)
    task_metadata: dict | None = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "task_app": "Sonic Adventure",
                "task_env": "dev",
                "task_name": "Collect the chaos emeralds.",
                "task_status": "complete",
                "task_watermark": "2022-06-27T00:00:00.000000+00:00",
                "task_duration": 1200.13,
                "task_metadata": {"key": "value", "some": ["list", "of", "items"]},
            }
        }


class UserCreatePayloadSchema(BaseModel):
    username: str = Field(default=..., max_length=100)
    password: str = Field(default=..., min_length=8, max_length=32)
    email: EmailStr = Field(default=...)
    full_name: str = Field(default=None, max_length=100)
    category: UserCategoryEnum = Field(default=...)

    class Config:
        schema_extra = {
            "example": {
                "username": "sonic",
                "email": "sonic@hedgehog.com",
                "password": "openyourheart",
                "full_name": "Sonic The Hedgehog",
                "category": "human",
            }
        }


class UserPasswordResetPayloadSchema(BaseModel):
    username: str = Field(default=..., max_length=100)
    new_password: str = Field(default=..., min_length=8, max_length=32)

    class Config:
        schema_extra = {
            "example": {
                "username": "shadow",
                "new_password": "maria",
            }
        }
