from datetime import datetime

from fastapi import APIRouter, HTTPException, Path

from app.models.pydantic import TaskPayloadSchema, TaskResponseSchema

router = APIRouter()

tasks = [
    {
        "id": 1,
        "app": "cloudwick",
        "environment": "testing",
        "database": "ema",
        "instance": "dev",
        "schema": None,
        "table": "bill",
        "created_at": datetime(2022, 6, 24, 23, 58, 19, 701579),
    },
    {
        "id": 2,
        "app": "cloudwick",
        "environment": "testing",
        "database": "ema",
        "instance": "dev",
        "schema": None,
        "table": "claim",
        "created_at": datetime(2022, 6, 24, 23, 58, 19, 701579),
    },
]


@router.get("/task/{id}", response_model=TaskResponseSchema)
def get_task(id: int = Path(..., gt=0)) -> TaskResponseSchema:
    requested_task = [task for task in tasks if task["id"] == id]
    if not requested_task:
        raise HTTPException(status_code=404, detail="Summary not found")
    return requested_task[0]


@router.get("/tasks", response_model=list[TaskResponseSchema])
def get_tasks() -> list[TaskResponseSchema]:
    return tasks


@router.post(
    "/task",
    response_model=TaskResponseSchema,
    status_code=201,
)
def create_task(payload: TaskPayloadSchema) -> TaskResponseSchema:
    task_id = len(tasks) + 1
    task_created_at = datetime.now()
    new_task = {
        "id": task_id,
        "app": payload.app,
        "environment": payload.environment,
        "database": payload.database,
        "instance": payload.instance,
        "schema": payload.schema,
        "table": payload.table,
        "created_at": task_created_at,
    }
    tasks.append(new_task)
    return new_task
