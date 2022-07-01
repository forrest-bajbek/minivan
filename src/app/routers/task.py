from fastapi import APIRouter, HTTPException, Path, Security

from app.models.pydantic import TaskPayloadSchema
from app.models.tortoise import TaskSchema
from app.routers import crud
from app.routers.user import get_current_user

router = APIRouter(tags=["task"])


@router.post(
    "/task",
    status_code=201,
    dependencies=[Security(get_current_user, scopes=["write"])],
)
async def post_task(payload: TaskPayloadSchema) -> dict:
    task_id = await crud.create_task(payload)
    return {"id": task_id}


@router.get(
    "/task/{id}",
    response_model=TaskSchema,
    dependencies=[Security(get_current_user, scopes=["read"])],
)
async def get_task(id: int = Path(..., gt=0)) -> TaskSchema:
    task = await crud.get_task(id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get(
    "/tasks",
    response_model=list[TaskSchema],
    dependencies=[Security(get_current_user, scopes=["read"])],
)
async def get_tasks() -> list[TaskSchema]:
    tasks = await crud.get_tasks()
    print(tasks)
    return tasks


@router.delete(
    "/task/{id}",
    dependencies=[Security(get_current_user, scopes=["write"])],
)
async def delete_summary(id: int = Path(..., gt=0)) -> dict:
    deleted = await crud.delete_task(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": deleted}
