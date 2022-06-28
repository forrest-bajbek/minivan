from datetime import datetime, timezone

from aredis_om.model.model import NotFoundError
from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from app.models.pydantic import TaskPayloadSchema, TaskResponseSchema
from app.models.redis import Task

router = APIRouter()


@router.post("/task", response_model=TaskResponseSchema, status_code=201)
async def post_task(payload: TaskPayloadSchema) -> TaskResponseSchema:
    now = datetime.now(timezone.utc)
    task = Task(created_at=now, updated_at=now, **payload.dict())
    result = await task.save()
    return TaskResponseSchema(pk=result.pk)


@router.get("/task/{pk}", response_model=Task, status_code=200)
@cache(expire=600)
async def get_task(pk: str) -> Task:
    try:
        task = await Task.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/task/{pk}")
async def delete_task(pk: str):
    deleted = await Task.delete(pk)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"pk": pk, "deleted": True}
