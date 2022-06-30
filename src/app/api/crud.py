from app.auth.auth_handler import get_password_hash
from app.models.pydantic import TaskPayloadSchema, UserSignupPayloadSchema
from app.models.tortoise import Task, User


async def create_task(payload: TaskPayloadSchema) -> Task:
    task = Task(**payload.dict())
    await task.save()
    return task


async def get_task(id: int) -> Task | None:
    task = await Task.filter(id=id).first().values()
    return task if task else None


async def get_tasks() -> list[Task | None]:
    tasks = await Task.all().values()
    return tasks


async def delete_task(id: int) -> Task:
    task = await Task.filter(id=id).first().delete()
    return task


# async def put(id: int, payload: TaskPayloadSchema) -> dict | None:
#     summary = await TextSummary.filter(id=id).update(
#         url=payload.url, summary=payload.summary
#     )
#     if summary:
#         updated_summary = await TextSummary.filter(id=id).first().values()
#         return updated_summary
#     return None


async def create_user(payload: UserSignupPayloadSchema) -> User | None:
    user = await User.filter(username=payload.username).first().values()
    if user:
        return None
    new_user = User(
        username=payload.username,
        password_hash=get_password_hash(payload.password),
        email=payload.email,
        full_name=payload.full_name,
        category=payload.category,
    )
    await new_user.save(force_create=True)
    return new_user


async def get_user(id: int) -> User | None:
    user = await User.filter(id=id).first().values()
    return user if user else None


async def get_user_from_username(username: str) -> User:
    user = await User.filter(username=username).first().values()
    return user if user else None
