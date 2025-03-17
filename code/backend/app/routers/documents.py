from app.models.document import Document, TaskStatusResponse, TaskIdResponse
from fastapi import APIRouter, HTTPException, status, Query, BackgroundTasks
from typing import List
from typing import Optional

router = APIRouter(tags=['Работа с документами'])

@router.get("/documents", response_model=List[Document], summary="Получить документы с фильтрацией и сортировкой")
async def read_documents(
    tag: Optional[str] = Query(None, description="Фильтр по тегу"),
    sort_by: Optional[str] = Query(None, description="Поле для сортировки (например, 'name', 'uploadDate')"),
    order: Optional[str] = Query("asc", description="Порядок сортировки: 'asc' (по возрастанию) или 'desc' (по убыванию)")
):
    ...

@router.post("/documents/create", response_model=Document, summary="Добавить документ")
async def create_document(document: Document):
    ...

@router.get("/documents/{document_id}", response_model=Document, summary="Получить один документ по id")
async def read_document(document_id: int):
    ...

@router.patch("/documents/{document_id}", response_model=Document, summary="Изменить документ")
async def update_document(document_id: int, document: Document):
    ...

@router.put("/documents/{document_id}", response_model=Document, summary="Полностью обновить документ")
async def replace_document(document_id: int, document: Document):
    ...

@router.delete("/documents/{document_id}", summary="Удалить документ")
async def delete_document(document_id: int):
    ...

@router.get("/documents", response_model=List[Document], summary="Получить документы по тегу")
async def read_documents_by_tag(tag: Optional[str] = None):
    ...

@router.post("/documents/upload", response_model=TaskIdResponse, summary="Загрузить документ асинхронно")
async def upload_document(background_tasks: BackgroundTasks):
    ...

@router.get("/tasks/{task_id}", response_model=TaskStatusResponse, summary="Получить статус задачи")
async def get_task_status(task_id: str):
    ...

@router.get("/tasks", response_model=List[TaskStatusResponse], summary="Получить статусы всех задач")
async def get_all_tasks():
    ...
