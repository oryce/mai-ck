from fastapi import APIRouter, HTTPException, Path, Depends, status
from app.db.models import *
from .schemas import Tag
from peewee import DoesNotExist

router = APIRouter(tags=["Работа с тегами"])


@router.get("/tags", response_model=list[Tag], summary="Получить все доступные теги")
async def get_tags(): ...


@router.post("/tags/create", response_model=Tag, summary="Добавить тег")
async def create_tag(tag: Tag): ...


@router.delete("/tags/{tag_id}", summary="Удалить тег")
async def delete_tag(tag_id: int): ...


@router.put('/document/{document_id}/tags', status_code=status.HTTP_201_CREATED)
async def add_tag_to_document(
        document_id: int,
        tag_request: TagRequest
):
    tag_id = tag_request.tagId

    try:
        # Проверка существования документа
        document = Document.get(Document.id == document_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        # Проверка существования тега
        tag = Tag.get(Tag.id == tag_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Tag not found")

    # Проверка, был ли уже добавлен этот тег к документу
    if DocumentTags.select().where(
            DocumentTags.documentId == document_id, DocumentTags.tagId == tag_id
    ).exists():
        raise HTTPException(status_code=400, detail="Tag already added to the document")

    # Добавляем тег к документу
    DocumentTags.create(documentId=document_id, tagId=tag_id)

    return {"message": "Tag added successfully"}
