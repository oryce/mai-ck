import uuid
from typing import List

from redis import Redis
from rq import Queue

from .steps.ocr import ocr
from .steps.signature_stamp import find_signature_stamp
from .steps.split import split_pdf_to_images
from .steps.type import get_document_type
from ..db.models import TagModel

queue_name = "pipeline"

redis = Redis(host='redis',
              port=6379,
              password=None)
queue = Queue(connection=redis, name=queue_name)


def set_status(task_id: str, status: str):
    redis.hset(f"task:{task_id}", "status", status)


def run_task(document_path: str) -> str:
    task_id = str(uuid.uuid4())
    tag_ids = [tag.id for tag in TagModel.select(TagModel.id)]

    queue.enqueue(process_document, task_id, document_path, tag_ids)

    return task_id


def process_document(task_id: str, document_path: str, tag_ids: List[str]):
    set_status(task_id, "preprocessing")

    images = split_pdf_to_images(document_path)

    signature, stamp = find_signature_stamp(images)

    set_status(task_id, "processing")

    text = ocr(images)

    doc_type = get_document_type(text, tag_ids)

    redis.hset(
        f"task:{task_id}",
        mapping={
            "signature": str(signature),
            "stamp": str(stamp),
            "type": doc_type,
        },
    )

    set_status(task_id, "finished")


