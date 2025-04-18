from fastapi import APIRouter

from .schemas import Tag, TaskStatusResponse

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


tags_router = APIRouter(tags=["Работа с тэгами"])


@tags_router.get(
    "/tags", response_model=list[Tag], summary="Получить все доступные тэги"
)
async def get_tags(): ...


@tags_router.get(
    "/tags/{tag_id}", response_model=Tag, summary="Получить один тэг по ID"
)
async def get_tag_by_id(tag_id: int): ...


@tags_router.post("/tags/create", response_model=Tag, summary="Добавить тэг")
async def create_tag(tag: Tag): ...


@tags_router.delete("/tags/{tag_id}", summary="Удалить тэг")
async def delete_tag(tag_id: int): ...
