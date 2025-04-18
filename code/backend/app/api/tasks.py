from fastapi import APIRouter

from .schemas import TaskStatusResponse

router = APIRouter(tags=["Работа с асинхронными задачами"])


@router.get(
    "/tasks/{task_id}",
    response_model=TaskStatusResponse,
    summary="Получить статус задачи",
)
async def get_task(task_id: str): ...


@router.get(
    "/tasks",
    response_model=list[TaskStatusResponse],
    summary="Получить статусы всех задач",
)
async def get_tasks(): ...


@router.delete("/tasks/{task_id}", summary="Удалить задачу")
async def delete_task(task_id: int): ...
