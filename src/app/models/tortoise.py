from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Task(models.Model):
    id = fields.IntField(pk=True)
    task_app = fields.CharField(max_length=100)
    task_env = fields.CharField(max_length=20)
    task_name = fields.CharField(max_length=100)
    task_status = fields.CharField(max_length=20)
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
    category = fields.CharField(max_length=30)
    disabled = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class PydanticMeta:
        exclude = ["password_hash"]


UserSchema = pydantic_model_creator(User)
