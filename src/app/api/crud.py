from datetime import datetime, timezone

from app.models.pydantic import TaskPayloadSchema
from app.models.redis import Task


async def post(payload: TaskPayloadSchema) -> Task:
    now = datetime.now(timezone.utc)
    task = Task(created_at=now, updated_at=now, **payload.dict())
    return await task.save()


# async def get(pk: str) -> Task | None:
#     summary = await TextSummary.filter(id=id).first().values()
#     if summary:
#         return summary
#     return None


# async def get_all() -> list[Task] | None:
#     summaries = await TextSummary.all().values()
#     return summaries


# async def delete(pk: str) -> str:
#     summary = await TextSummary.filter(id=id).first().delete()
#     return summary


# async def put(pk: str, payload: TaskPayloadSchema) -> dict | None:
#     summary = await TextSummary.filter(id=id).update(
#         url=payload.url, summary=payload.summary
#     )
#     if summary:
#         updated_summary = await TextSummary.filter(id=id).first().values()
#         return updated_summary
#     return None
