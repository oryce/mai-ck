from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class Document(BaseModel):
    id: int = Field(
        ..., description="Уникальный идентификатор документа в системе", example=1
    )
    uploaderId: int = Field(
        ...,
        description="Идентификатор пользователя, загрузившего документ",
        example=123,
    )
    name: str = Field(
        ...,
        description="Название документа",
        min_length=1,
        max_length=30,
        example="Презентация на 17.03.25",
    )
    uploadDate: datetime = Field(
        ...,
        description="Дата и время загрузки документа в систему",
        example="2025-10-01T12:00:00Z",
    )
    createDate: datetime = Field(
        ...,
        description="Дата и время создания документа",
        example="2025-09-30T08:00:00Z",
    )
    typeId: int = Field(..., description="Идентификатор типа документа", example=2)

    @field_validator("uploadDate", "createDate", mode="before")
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


class TaskStatusResponse(BaseModel):
    task_id: str = Field(description="ID асинхронно-выполняемой задачи")
    status: str = Field(description="uploading | processing | complete")
    progress: int = Field(description="Прогресс выполнения задачи", ge=0, le=100)


class TaskIdResponse(BaseModel):
    task_id: str = Field(description="ID асинхронно-выполняемой задачи")


class Tag(BaseModel):
    id: str = Field(description="ID тега в системе")
    name: str = Field(description="Имя тега")
    auto_tag: bool = Field(description="Задаётся ли тег автоматически")
