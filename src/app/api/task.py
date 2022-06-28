from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query  # , Path, Query
from fastapi_cache.decorator import cache
from aredis_om.model.model import NotFoundError

from app.api import crud
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
async def get_task(pk: str) -> Task:
    try:
        task = await Task.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/tasks", response_model=list[Task])
async def get_tasks() -> list[Task]:
    tasks = [await Task.get(pk) async for pk in await Task.all_pks()]
    return tasks


@router.delete("/task/{pk}")
async def delete_task(pk: str):
    deleted = await Task.delete(pk)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"pk": pk, "deleted": True}


"""
task_app
task_env
task_name
task_status
task_watermark
task_start_at
task_stop_at
task_metadata
"""
