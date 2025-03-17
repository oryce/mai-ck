from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class Document(BaseModel):
    id: int = Field(
        ...,
        description="Уникальный идентификатор документа в системе",
        example=1
    )
    uploaderId: int = Field(
        ...,
        description="Идентификатор пользователя, загрузившего документ",
        example=123
    )
    name: str = Field(
        ...,
        description="Название документа",
        min_length=1,
        max_length=30,
        example="Презентация на 17.03.25"
    )
    uploadDate: datetime = Field(
        ...,
        description="Дата и время загрузки документа в систему",
        example="2025-10-01T12:00:00Z"
    )
    createDate: datetime = Field(
        ...,
        description="Дата и время создания документа",
        example="2025-09-30T08:00:00Z"
    )
    typeId: int = Field(
        ...,
        description="Идентификатор типа документа",
        example=2
    )

    @validator('uploadDate', 'createDate', pre=True)
    def parse_dates(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "uploaderId": 123,
                "name": "Презентация 228",
                "uploadDate": "2025-10-01T12:00:00Z",
                "createDate": "2025-09-30T08:00:00Z",
                "typeId": 2
            }
        }


class TaskStatusResponse(BaseModel):
    taskId: str = Field(description="Id асинхронно выполняемой задачи")
    status: str = Field(desctiption="uploading | processing | complete")
    progress: int = Field(description="Прогресс выполнения задачи", ge=0, le=100)


class TaskIdResponse(BaseModel):
    taskId: str = Field(description="Id асинхронно выполняемой задачи")