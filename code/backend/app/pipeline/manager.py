import uuid

from app.config import Settings
from app.db.models import TagModel
from redis import Redis
from rq import Queue

from .steps.ocr import ocr
from .steps.signature_stamp import find_signature_stamp
from .steps.split import split_pdf_to_images
from .steps.type import get_document_type

queue_name = "pipeline"

__settings = Settings()

__redis = Redis(host=__settings.redis_host, password=__settings.redis_password)
__queue = Queue(connection=__redis, name=queue_name)


def set_status(task_id: str, status: str):
    __redis.hset(f"task:{task_id}", "status", status)


def run_task(document_path: str) -> str:
    task_id = str(uuid.uuid4())
    tag_names = [tag.name for tag in TagModel.select(TagModel.name)]

    __queue.enqueue(process_document, task_id, document_path, tag_names)

    return task_id


def process_document(task_id: str, document_path: str, tag_names: list[str]):
    set_status(task_id, "preprocessing")

    images = split_pdf_to_images(document_path)

    signature, stamp = find_signature_stamp(images)

    set_status(task_id, "processing")

    text = ocr(images)

    doc_type = get_document_type(text, tag_names)

    __redis.hset(
        f"task:{task_id}",
        mapping={
            "signature": str(signature),
            "stamp": str(stamp),
            "type": doc_type,
        },
    )

    set_status(task_id, "finished")
