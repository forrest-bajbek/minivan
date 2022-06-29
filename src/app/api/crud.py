from app.models.pydantic import TaskPayloadSchema
from app.models.tortoise import Task


async def post_task(payload: TaskPayloadSchema) -> int:
    task = Task(**payload.dict())
    await task.save()
    return task.id


async def get_task(id: int) -> dict | None:
    task = await Task.filter(id=id).first().values()
    if task:
        return task
    return None


async def get_tasks() -> list[dict | None]:
    tasks = await Task.all().values()
    return tasks


async def delete_task(id: int) -> int:
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
