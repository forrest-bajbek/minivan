from fastapi import APIRouter  # , Path, Query

from app.api import crud
from app.models.pydantic import TaskPayloadSchema, TaskResponseSchema

# from app.models.redis import Task

router = APIRouter()


@router.post("/task", response_model=TaskResponseSchema, status_code=201)
async def post_task(payload: TaskPayloadSchema) -> TaskResponseSchema:
    task = await crud.post(payload)
    return TaskResponseSchema(pk=task.pk)


# @router.delete("/task/{pk}")
# async def delete_task(pk: str):
#     task = Task.get(pk)
#     return task.delete()


# @router.get("/tasks", response_model=list[Task])
# async def get_tasks() -> list[Task]:
#     pks = Task.all_pks()
#     tasks = [Task.get(pk) for pk in pks]
#     return tasks


# @router.get("/task/{pk}", response_model=Task, status_code=200)
# async def get_task(pk: str) -> Task:
#     task = Task.get(pk)
#     return task


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
