from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.models.pydantic import TaskPayloadResponseSchema, TaskPayloadSchema
from app.models.tortoise import TaskSchema

router = APIRouter()


@router.post("/task", response_model=TaskPayloadResponseSchema, status_code=201)
async def post_task(payload: TaskPayloadSchema) -> TaskPayloadResponseSchema:
    task_id = await crud.create_task(payload)
    return {"id": task_id}


@router.get("/task/{id}", response_model=TaskSchema)
async def get_task(id: int = Path(..., gt=0)) -> TaskSchema:
    task = await crud.get_task(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/tasks", response_model=list[TaskSchema])
async def get_tasks() -> list[TaskSchema]:
    tasks = await crud.get_tasks()
    print(tasks)
    return tasks


@router.delete("/task/{id}")
async def delete_summary(id: int = Path(..., gt=0)) -> dict:
    deleted = await crud.delete_task(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": deleted}
