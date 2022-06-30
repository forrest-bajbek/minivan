from datetime import datetime

from pydantic import BaseModel, EmailStr, Field
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


class UserSignupPayloadSchema(BaseModel):
    username: str = Field(default=..., max_length=100)
    password: str = Field(default=..., min_length=8, max_length=32)
    email: EmailStr = Field(default=...)
    full_name: str = Field(default=None, max_length=100)
    category: Literal["human", "robot"] = Field(default=...)

    class Config:
        schema_extra = {
            "example": {
                "username": "forrestbajbek",
                "email": "forrest@bajbek.com",
                "password": "weakpassword",
                "full_name": "Forrest Bajbek",
                "category": "human",
            }
        }


class UserLoginPayloadSchema(BaseModel):
    username: str = Field(default=..., max_length=100)
    password: str = Field(default=..., min_length=8, max_length=32)

    class Config:
        schema_extra = {
            "example": {
                "username": "forrestbajbek",
                "password": "weakpassword",
            }
        }
