from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class TaskPayloadSchema(BaseModel):
    app: str = Field(...)
    environment: str = Field(...)
    database: str = Field(...)
    instance: str = Field(...)
    table: str = Field(...)

    class Config:
        example = {
            "demo": {
                "app": "test_app",
                "environment": "test_env",
                "database": "test_db",
                "instance": "test_instance",
                "table": "test_table",
            }
        }


class TaskResponseSchema(TaskPayloadSchema):
    id: int
    created_at: datetime

    class Config:
        example = {
            "demo": {
                "id": 1,
                "app": "test_app",
                "environment": "test_env",
                "database": "test_db",
                "instance": "test_instance",
                "table": "test_table",
                "created_at": datetime.now(),
            }
        }


class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Abdulazeez Abdulazeez Adeshina",
                "email": "abdulazeez@x.com",
                "password": "weakpassword",
            }
        }


class UserAuthSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weakpassword",
            }
        }
