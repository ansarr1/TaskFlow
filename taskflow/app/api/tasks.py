from fastapi import APIRouter, HTTPException, Response, status, Depends
from app.schemas.tasks import TaskCreate, TaskGet, TaskUpdate
from app.dependencies.common import pagination_params, get_current_user
router = APIRouter(prefix="/tasks", tags=["Tasks"])

tasks: list[TaskGet] = [
    {"id": 1, "title": "Изучить FastAPI", "completed": False},
    {"id": 2, "title": "Изучить PostgreSQL", "completed": False},
    {"id": 3, "title": "Создать первый проект", "completed": False},
]


@router.get("/", response_model=list[TaskGet])
async def get_tasks(
    pagination: dict = Depends(pagination_params),
    current_user: dict = Depends(get_current_user)
) -> list[TaskGet]:
    offset = pagination['offset']
    limit = pagination['limit']

    

    return tasks[offset:offset + limit]



@router.post("/", response_model=TaskGet)
async def create_task(payload: TaskCreate):
    new_id = max((task["id"] for task in tasks), default=0) + 1
    new_task = {"id": new_id, "title": payload.title, "completed": False}
    tasks.append(new_task)
    return new_task


@router.get("/{task_id}", response_model=TaskGet)
def get_task_by_id(task_id: int, title: str):
    for task in tasks:
        if task["id"] == task_id and (title in task["title"]):
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача не найдена",
    )


@router.patch("/{task_id}", response_model=TaskGet)
def update_task(task_id: int, payload: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if payload.title is not None:
                task["title"] = payload.title
            if payload.completed is not None:
                task["completed"] = payload.completed

            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача не найдена",
    )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Задача не найдена",
    )