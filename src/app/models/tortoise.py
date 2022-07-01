from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from app.models.enums import TaskEnvEnum, TaskStatusEnum, UserCategoryEnum


class Task(models.Model):
    id = fields.IntField(pk=True)
    task_app = fields.CharField(max_length=100)
    task_env = fields.CharEnumField(enum_type=TaskEnvEnum)
    task_name = fields.CharField(max_length=100)
    task_status = fields.CharEnumField(enum_type=TaskStatusEnum)
    task_watermark = fields.DatetimeField()
    task_duration = fields.FloatField(null=True)
    task_metadata = fields.JSONField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


TaskSchema = pydantic_model_creator(Task)


class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, unique=True)
    password_hash = fields.CharField(max_length=128)
    email = fields.CharField(max_length=320)
    full_name = fields.CharField(max_length=100, null=True)
    category = fields.CharEnumField(enum_type=UserCategoryEnum)
    is_admin = fields.BooleanField(default=False)
    is_disabled = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class PydanticMeta:
        exclude = ["password_hash"]


UserSchema = pydantic_model_creator(User)
