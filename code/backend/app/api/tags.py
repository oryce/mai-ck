from fastapi import APIRouter, HTTPException, Path, Depends, status
from app.db.models import *
from .schemas import Tag
from peewee import DoesNotExist
from typing import Optional, List

router = APIRouter(tags=["Работа с тегами"])


@router.put('/document/{document_id}/tags', status_code=status.HTTP_201_CREATED)
async def add_tag_to_document(
        document_id: int,
        tag_request: TagRequest
):
    tag_id = tag_request.tagId

    try:
        document = Document.get(Document.id == document_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        tag = Tag.get(Tag.id == tag_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Tag not found")

    if DocumentTags.select().where(
            DocumentTags.documentId == document_id, DocumentTags.tagId == tag_id
    ).exists():
        raise HTTPException(status_code=400, detail="Tag already added to the document")

    DocumentTags.create(documentId=document_id, tagId=tag_id)

    return {"message": "Tag added successfully"}


@router.get("/tags", response_model=List[TagResponse], summary="Получить все теги")
async def get_tags():
    return list(Tag.select())


@router.put("/tags", response_model=TagResponse, status_code=status.HTTP_201_CREATED, summary="Создать тег")
async def create_tag(tag: TagCreate):
    if Tag.select().where(Tag.name == tag.name).exists():
        raise HTTPException(status_code=400, detail="Tag with this name already exists")

    new_tag = Tag.create(name=tag.name, autoTag=tag.autoTag)
    return new_tag


@router.delete("/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить тег")
async def delete_tag(tag_id: int):
    try:
        tag = Tag.get_by_id(tag_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag.delete_instance(recursive=True)  # удаляет также записи в DocumentTags
    return None  # 204 No Content
