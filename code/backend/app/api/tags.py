from fastapi import APIRouter

from .schemas import Tag

router = APIRouter(tags=["Работа с тегами"])


@router.get(
    "/tags", response_model=list[Tag], summary="Получить все доступные теги"
)
async def get_tags(): ...


@router.get(
    "/tags/{tag_id}", response_model=Tag, summary="Получить один тег по ID"
)
async def get_tag_by_id(tag_id: int): ...


@router.post("/tags/create", response_model=Tag, summary="Добавить тег")
async def create_tag(tag: Tag): ...


@router.delete("/tags/{tag_id}", summary="Удалить тег")
async def delete_tag(tag_id: int): ...
