from fastapi import APIRouter, HTTPException, Path
from app.models.pydantic import TaskPayloadSchema, TaskPayloadResponseSchema
from app.models.tortoise import TaskSchema
from app.api import crud


router = APIRouter()


@router.post("/task", response_model=TaskPayloadResponseSchema, status_code=201)
async def post_task(payload: TaskPayloadSchema) -> TaskPayloadResponseSchema:
    task_id = await crud.post_task(payload)
    response = TaskPayloadResponseSchema(id=task_id)
    return response


@router.get("/task/{id}", response_model=TaskSchema)
async def get_task(id: int = Path(..., gt=0)) -> TaskSchema:
    task = await crud.get_task(id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/tasks", response_model=list[TaskSchema])
async def get_tasks() -> list[TaskSchema]:
    return await crud.get_tasks()


@router.delete("/task/{id}")
async def delete_summary(id: int = Path(..., gt=0)) -> dict:
    task = await crud.get_task(id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    await crud.delete_task(id)
    response = {"id": id, "deleted": True}
    return response
