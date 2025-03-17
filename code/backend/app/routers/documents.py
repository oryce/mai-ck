from app.models.document import Document, TaskStatusResponse, TaskIdResponse, Tag
from fastapi import APIRouter, HTTPException, status, Query, BackgroundTasks
from typing import List
from typing import Optional

document_router = APIRouter(tags=['Работа с документами'])

@document_router.get("/documents", response_model=List[Document], summary="Получить документы с фильтрацией и сортировкой")
async def read_documents(
    tag: Optional[str] = Query(None, description="Фильтр по тегу"),
    sort_by: Optional[str] = Query(None, description="Поле для сортировки (например, 'name', 'uploadDate')"),
    order: Optional[str] = Query("asc", description="Порядок сортировки: 'asc' (по возрастанию) или 'desc' (по убыванию)")
):
    ...

@document_router.get("/documents/{document_id}", response_model=Document, summary="Получить один документ по id")
async def read_document(document_id: int):
    ...

@document_router.get("/documents", response_model=List[Document], summary="Получить документы по тегу")
async def read_documents_by_tag(tag: Optional[str] = None):
    ...

@document_router.post("/documents/create", response_model=Document, summary="Добавить документ")
async def create_document(document: Document):
    ...

@document_router.post("/documents/upload", response_model=TaskIdResponse, summary="Загрузить документ асинхронно")
async def upload_document(background_tasks: BackgroundTasks):
    ...

@document_router.patch("/documents/{document_id}", response_model=Document, summary="Изменить документ")
async def update_document(document_id: int, document: Document):
    ...

@document_router.put("/documents/{document_id}", response_model=Document, summary="Полностью обновить документ")
async def replace_document(document_id: int, document: Document):
    ...

@document_router.delete("/documents/{document_id}", summary="Удалить документ")
async def delete_document(document_id: int):
    ...


task_router = APIRouter(tags=['Работа с асинхронными задачами'])

@task_router.get("/tasks/{task_id}", response_model=TaskStatusResponse, summary="Получить статус задачи")
async def get_task_status(task_id: str):
    ...

@task_router.get("/tasks", response_model=List[TaskStatusResponse], summary="Получить статусы всех задач")
async def get_all_tasks():
    ...

@task_router.delete("/tasks/{task_id}", summary="Удалить задачу")
async def delete_task(task_id: int):
    ...


tags_router = APIRouter(tags=["Работа с тэгами"])

@tags_router.get("/tags", response_model=List[Tag], summary="Получить все доступные тэги")
async def read_tags():
    ...

@tags_router.get("/tags/{tag_id}", response_model=Tag, summary="Получить один тэг по ID")
async def read_tags(tag_id: int):
    ...

@tags_router.post("/tags/create", response_model=Tag, summary="Добавить тэг")
async def create_tag(tag : Tag):
    ...

@tags_router.delete("/tags/{tag_id}", summary="Удалить тэг")
async def delete_tag(tag_id: int):
    ...