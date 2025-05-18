from datetime import datetime
from typing import Optional

import app.db.models as db
from pydantic import BaseModel, Field, field_validator


class DocumentDto(BaseModel):
    id: int = Field(
        ..., description="Уникальный идентификатор документа в системе", example=1
    )
    uploader_id: int = Field(
        ...,
        description="Идентификатор пользователя, загрузившего документ",
        example=123,
        alias="uploaderId",
    )
    name: str = Field(
        ...,
        description="Название документа",
        min_length=1,
        max_length=30,
        example="Презентация на 17.03.25",
    )
    upload_date: datetime = Field(
        ...,
        description="Дата и время загрузки документа в систему",
        example="2025-10-01T12:00:00Z",
        alias="uploadDate",
    )
    create_date: datetime = Field(
        ...,
        description="Дата и время создания документа",
        example="2025-09-30T08:00:00Z",
        alias="createDate",
    )
    type_id: int = Field(
        ..., description="Идентификатор типа документа", example=2, alias="typeId"
    )

    @field_validator("upload_date", "create_date", mode="before")
    def parse_dates(cls, value):
        if isinstance(value, str):
            # Поддерживаем формат ISO с 'Z' (UTC)
            if value.endswith("Z"):
                value = value[:-1] + "+00:00"
            return datetime.fromisoformat(value)
        return value

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "uploaderId": 123,
                "name": "Презентация 228",
                "uploadDate": "2025-10-01T12:00:00Z",
                "createDate": "2025-09-30T08:00:00Z",
                "typeId": 2,
            }
        }

class PaginatedDocumentsResponse(BaseModel):
    first: int = Field(..., description="Номер первой страницы")
    last: int = Field(..., description="Номер последней страницы")
    prev: int = Field(..., description="Номер предыдущей страницы (-1 если нет)")
    next: int = Field(..., description="Номер следующей страницы (-1 если нет)")
    pages: int = Field(..., description="Общее количество страниц")
    data: list[DocumentDto] = Field(..., description="Список документов")


class TaskStatusResponse(BaseModel):
    task_id: str = Field(description="ID асинхронно-выполняемой задачи", alias="taskId")
    status: str = Field(description="uploading | processing | complete")
    progress: int = Field(description="Прогресс выполнения задачи", ge=0, le=100)


class TaskIdResponse(BaseModel):
    task_id: str = Field(description="ID асинхронно-выполняемой задачи", alias="taskId")


class TagDto(BaseModel):
    id: int = Field(description="ID тега в системе")
    name: str = Field(description="Имя тега")
    auto_tag: bool = Field(description="Задаётся ли тег автоматически", alias="autoTag")

    @staticmethod
    def from_model(model: db.TagModel) -> "TagDto":
        return TagDto(
            id=int(model.id), name=str(model.name), autoTag=bool(model.auto_tag)
        )


class AddTagRequest(BaseModel):
    tag_id: int = Field(description="ID тега", alias="tagId")


class CreateTagRequest(BaseModel):
    name: str = Field(description="Имя тега")
    auto_tag: Optional[bool] = Field(
        default=False, description="Задаётся ли тег автоматически", alias="autoTag"
    )
