from app.auth.auth_handler import get_password_hash
from app.models.pydantic import TaskPayloadSchema, UserSignupPayloadSchema
from app.models.tortoise import Task, User


async def create_task(payload: TaskPayloadSchema) -> int:
    task = Task(**payload.dict())
    await task.save()
    return task.id


async def get_task(id: int) -> dict | None:
    task = await Task.filter(id=id).first().values()
    return task if task else None


async def get_tasks() -> list[dict | None]:
    tasks = await Task.all().values()
    return tasks


async def delete_task(id: int) -> bool:
    task = await Task.filter(id=id).first().delete()
    return bool(task)


# async def put(id: int, payload: TaskPayloadSchema) -> dict | None:
#     summary = await TextSummary.filter(id=id).update(
#         url=payload.url, summary=payload.summary
#     )
#     if summary:
#         updated_summary = await TextSummary.filter(id=id).first().values()
#         return updated_summary
#     return None


async def user_exists(username: str) -> bool:
    user = await User.filter(username=username).first().values()
    return True if user else False


async def create_user(payload: UserSignupPayloadSchema) -> User | None:
    user = User(
        username=payload.username,
        password_hash=get_password_hash(payload.password),
        email=payload.email,
        full_name=payload.full_name,
        category=payload.category,
    )
    await user.save(force_create=True)
    return user


async def get_user(id: int) -> dict | None:
    user = await User.filter(id=id).first().values()
    return user if user else None


async def get_user_from_username(username: str) -> dict:
    user = await User.filter(username=username).first().values()
    return user if user else None
