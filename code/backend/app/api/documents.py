import datetime
import hashlib
import os
import tempfile
from typing import Annotated

from fastapi import (
    APIRouter,
    HTTPException,
    Query,
    Response,
    Security,
    UploadFile,
    status,
)
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse
from peewee import JOIN, fn, prefetch

from app.auth import AccessTokenCredentials, oauth2
from app.config import Settings
from app.db import db
from app.db.models import DocumentModel, DocumentTagModel, DocumentTypeModel, TagModel
from app.task_queue import enqueue

from .schemas import DocumentDto, PaginatedDocumentsResponse, TaskIdResponse

settings = Settings()

router = APIRouter(tags=["Работа с документами"])


def build_query(sort: str, tags: str | None):
    """
    Common part of the SELECT that we can call from a thread-pool.
    """
    q = (
        DocumentModel
        # use LEFT OUTER so a missing type row never hides a document
        .select().join(
            DocumentTypeModel,
            JOIN.LEFT_OUTER,
            on=(DocumentModel.type == DocumentTypeModel.id),
        )
    )

    # tag filtering (return docs that have *all* requested tags)
    if tags:
        try:
            tag_ids = [int(t.strip()) for t in tags.split(",") if t.strip()]
        except ValueError:
            raise HTTPException(400, "Некорректный формат тегов")

        subq = (
            DocumentTagModel.select(DocumentTagModel.document_id)
            .where(DocumentTagModel.tag_id.in_(tag_ids))
            .group_by(DocumentTagModel.document_id)
            .having(fn.COUNT(DocumentTagModel.tag_id.distinct()) == len(tag_ids))
        )

        q = q.where(DocumentModel.id.in_(subq))

    order_field = (
        DocumentModel.upload_date.desc()
        if sort == "newest-first"
        else DocumentModel.upload_date.asc()
    )
    return q.order_by(order_field)


@router.get(
    "/documents",
    response_model=PaginatedDocumentsResponse,
    summary="Получить документы с фильтрацией и сортировкой",
)
async def get_documents(
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, alias="perPage"),
    sort: str = Query(
        "newest-first",
        pattern="^(newest-first|oldest-first)$",
        description="Сортировка: newest-first или oldest-first",
    ),
    tags: str | None = Query(None, description="Фильтр по тегам (через запятую)"),
):
    # build the query once – no DB work has happened yet
    base_query = build_query(sort, tags)

    # 1) how many rows in total?
    total: int = await run_in_threadpool(base_query.count)
    pages = (total + per_page - 1) // per_page if total else 0

    if pages and page > pages:
        raise HTTPException(400, "Некорректный номер страницы")

    # 2) fetch the requested slice + its DocumentType in one round-trip
    docs = await run_in_threadpool(
        lambda: list(
            prefetch(
                base_query.paginate(page, per_page),
                DocumentTypeModel,
                DocumentTagModel.select().join(TagModel),
            )
        )
    )

    # 3) convert to DTOs
    data = [
        DocumentDto(
            id=d.id,
            uploaderId=d.uploader_id,
            name=d.name,
            uploadDate=d.upload_date,
            createDate=d.creation_date,
            type=d.type.name if d.type else None,
            tags=[link.tag.name for link in d.tags],
        )
        for d in docs
    ]

    return PaginatedDocumentsResponse(
        first=1,
        last=pages or 0,
        prev=page - 1 if page > 1 else -1,
        next=page + 1 if page < pages else -1,
        pages=pages,
        data=data,
    )


@router.get(
    "/documents/{document_id}",
    response_model=DocumentDto,
    summary="Получить один документ по id",
)
async def get_document(document_id: int):
    try:
        document = (
            DocumentModel.select(DocumentModel, DocumentTypeModel)
            .switch(DocumentModel)
            .join(DocumentTypeModel)
            .where(DocumentModel.id == document_id)
            .first()
        )

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Документ не найден"
            )

        return DocumentDto(
            id=document.id,
            uploaderId=document.uploader.id,
            name=document.name,
            uploadDate=document.upload_date,
            createDate=document.creation_date,
            typeId=document.type.id,
        )
    except HTTPException:
        raise
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post(
    "/documents/upload",
    response_model=TaskIdResponse,
    summary="Загрузить документ",
)
async def upload_document(
    file: UploadFile, oidc: Annotated[AccessTokenCredentials, Security(oauth2)]
) -> TaskIdResponse:
    # Записываем файл на диск, одновременно хешируя его. Мы хотим именовать файлы на диске
    # их хешами, поэтому сначала записываем во временный файл, а затем переименовываем.
    digest = hashlib.sha256()

    tmp_file = tempfile.NamedTemporaryFile(
        dir=settings.upload_dir, suffix=".tmp", delete=False
    )

    try:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            tmp_file.write(chunk)
    finally:
        tmp_file.close()

    file_hash = digest.hexdigest()
    file_path = os.path.join(settings.storage_dir, f"{file_hash}.pdf")

    os.replace(tmp_file.name, file_path)

    DocumentModel.create(
        id=file_hash,
        uploader_id=oidc.token["sub"],
        name=file.filename,
        upload_date=datetime.datetime.now(),
        creation_date=datetime.datetime.now(),
    )

    # Создаём задачу на обработку. Воркеру нужен абсолютный путь.
    task_id = enqueue(os.path.abspath(file_path))

    return TaskIdResponse(taskId=task_id)


@router.patch(
    "/documents/{document_id}", response_model=DocumentDto, summary="Изменить документ"
)
async def update_document(document_id: int) -> DocumentDto: ...


@router.delete(
    "/documents/{document_id}",
    summary="Удалить документ",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document(document_id: int):
    try:
        with db.atomic():
            DocumentTagModel.delete().where(
                DocumentTagModel.document == document_id
            ).execute()

            deleted_count = (
                DocumentModel.delete().where(DocumentModel.id == document_id).execute()
            )

            if deleted_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Документ не найден"
                )

        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except HTTPException:
        raise
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get(
    "/documents/{document_id}/file",
    summary="Скачать PDF-документ",
    response_class=FileResponse,
)
async def get_document_file(document_id: str):
    """
    Возвращает оригинальный PDF файл документа.
    """
    file_path = os.path.join(settings.storage_dir, f"{document_id}.pdf")

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Файл не найден"
        )

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=f"{document_id}.pdf",
    )


@router.get(
    "/documents/{document_id}/preview",
    summary="Скачать превью документа",
    response_class=FileResponse,
)
async def get_document_preview(document_id: str):
    """
    Возвращает превью (первую страницу) документа.
    """
    file_path = os.path.join(settings.storage_dir, f"{document_id}_preview.jpg")

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Превью не найдено"
        )

    return FileResponse(
        file_path,
        media_type="image/jpeg",
        filename=f"{document_id}_preview.jpg",
    )
