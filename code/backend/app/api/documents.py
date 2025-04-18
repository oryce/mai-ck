from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Query

from .schemas import Document, TaskIdResponse

router = APIRouter(tags=["Работа с документами"])


@router.get(
    "/documents",
    response_model=list[Document],
    summary="Получить документы с фильтрацией и сортировкой",
)
async def get_documents(
    tag: Optional[str] = Query(None, description="Фильтр по тегу"),
    sort_by: Optional[str] = Query(
        None, description="Поле для сортировки (например, 'name', 'uploadDate')"
    ),
    order: Optional[str] = Query(
        "asc",
        description="Порядок сортировки: 'asc' (по возрастанию) или 'desc' (по убыванию)",
    ),
): ...


@router.get(
    "/documents/{document_id}",
    response_model=Document,
    summary="Получить один документ по id",
)
async def get_document(document_id: int): ...


@router.post(
    "/documents/upload",
    response_model=TaskIdResponse,
    summary="Загрузить документ",
)
async def upload_document(background_tasks: BackgroundTasks): ...


@router.patch(
    "/documents/{document_id}", response_model=Document, summary="Изменить документ"
)
async def update_document(document_id: int, document: Document): ...


@router.delete("/documents/{document_id}", summary="Удалить документ")
async def delete_document(document_id: int): ...
