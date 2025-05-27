from fastapi import APIRouter

from app.db import db
from app.db.models import DocumentModel, DocumentTagModel, DocumentTypeModel, TagModel
from app.task_queue import Status, get_task_result, get_task_status

from .schemas import TaskStatusResponse

router = APIRouter(tags=["Работа с асинхронными задачами"])


def update_document_metadata(
    doc_id: str, type_name: str, signature: bool, stamp: bool
) -> None:
    """
    1. Находит документ по doc_id.
    2. Находит тип документа по name и присваивает его найденному документу.
    3. Если signature/stamp == True, добавляет теги «Подпись» и/или «Печать».
    4. Сохраняет все изменения.

    Исключения:
        ValueError — если не найден документ или тип документа.
    """
    with db.atomic():  # одна транзакция, чтобы всё прошло целиком или не прошло вовсе
        # 1) ищем документ
        try:
            document = DocumentModel.get(DocumentModel.id == doc_id)
        except DocumentModel.DoesNotExist:
            raise ValueError(f"Документ с id={doc_id} не найден")

        # 2) ищем тип и присваиваем
        try:
            doc_type = DocumentTypeModel.get(DocumentTypeModel.name == type_name)
        except DocumentTypeModel.DoesNotExist:
            raise ValueError(f"Тип документа «{type_name}» не найден")

        document.type = doc_type
        document.save()  # можно отложить, но так нагляднее

        # 3) подготавливаем список тегов, которые нужно добавить
        tags_to_attach = []
        if signature:
            try:
                tags_to_attach.append(TagModel.get(TagModel.name == "Подпись"))
            except TagModel.DoesNotExist:
                pass  # или создайте автоматически, если это желаемо
        if stamp:
            try:
                tags_to_attach.append(TagModel.get(TagModel.name == "Печать"))
            except TagModel.DoesNotExist:
                pass

        # добавляем связи «документ-тег», избегая дубликатов
        for tag in tags_to_attach:
            DocumentTagModel.get_or_create(document=document, tag=tag)


@router.get(
    "/tasks/{task_id}",
    response_model=TaskStatusResponse,
    summary="Получить статус задачи",
)
async def get_task(task_id: str):
    task_status = get_task_status(task_id) or Status.ENQUEUED

    match task_status:
        case Status.ENQUEUED:
            status = "enqueued"
            progress = 0
        case Status.PREPROCESSING:
            status = "preprocessing"
            progress = 30
        case Status.PROCESSING:
            status = "processing"
            progress = 60
        case Status.FINISHED:
            status = "finished"
            progress = 100

    # This is a hack. Ideally we would want the worker to notify us in some way
    # (perhaps, with a message queue.) Too bad we don't have the time to implement
    # that.
    if task_status == Status.FINISHED:
        result = get_task_result(task_id)

        print(result.doc_id, result.type, result.signature, result.stamp)

        if result:
            update_document_metadata(
                result.doc_id, result.type, result.signature, result.stamp
            )

    return TaskStatusResponse(taskId=task_id, status=status, progress=progress)


@router.get(
    "/tasks",
    response_model=list[TaskStatusResponse],
    summary="Получить статусы всех задач",
)
async def get_tasks(): ...


@router.delete("/tasks/{task_id}", summary="Отменить задачу")
async def delete_task(task_id: int): ...
