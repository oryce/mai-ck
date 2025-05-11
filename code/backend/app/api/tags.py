from typing import List

from app.db.models import DocumentModel, DocumentTagModel, TagModel
from fastapi import APIRouter, HTTPException, status
from peewee import IntegrityError

from .schemas import AddTagRequest, CreateTagRequest, TagDto

router = APIRouter(tags=["Работа с тегами"])


@router.post("/documents/{document_id}/tags", status_code=status.HTTP_201_CREATED)
async def add_tag_to_document(document_id: int, tag_request: AddTagRequest):
    document = DocumentModel.get_or_none(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    tag = TagModel.get_or_none(tag_request.tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    try:
        DocumentTagModel.create(document=document, tag=tag)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Tag already added to the document")

    return {"message": "Tag added successfully"}


@router.get("/tags", response_model=List[TagDto], summary="Получить все теги")
async def get_tags():
    return list(map(TagDto.from_model, TagModel.select()))


@router.post(
    "/tags",
    response_model=TagDto,
    status_code=status.HTTP_201_CREATED,
    summary="Создать тег",
)
async def create_tag(tag: CreateTagRequest):
    try:
        new_tag = TagModel.create(name=tag.name, auto_tag=tag.auto_tag)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Tag already exists")

    return TagDto.from_model(new_tag)


@router.delete(
    "/tags/{tag_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить тег"
)
async def delete_tag(tag_id: int):
    tag = TagModel.get_or_none(tag_id)

    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag.delete_instance(recursive=True)

    return None
