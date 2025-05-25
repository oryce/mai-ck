import uuid

from redis import Redis
from rq import Queue

from .steps.ocr import ocr
from .steps.signature_stamp import find_signature_stamp
from .steps.split import split_pdf_to_images
from .steps.type import get_document_type

redis = Redis()
queue = Queue(connection=redis, name="pipeline")


def set_status(task_id: str, status: str):
    redis.hset(f"task:{task_id}", "status", status)


def run_task(document_path: str):
    job = queue.enqueue(process_document, document_path)
    return job


def process_document(document_path, task_id):
    set_status(task_id, "preprocessing")

    images = split_pdf_to_images(document_path)

    signature, stamp = find_signature_stamp(images)

    set_status(task_id, "processing")

    text = ocr(images)

    type = get_document_type(text)

    redis.hset(f"task:{task_id}", "signature", str(signature))
    redis.hset(f"task:{task_id}", "stamp", str(stamp))
    redis.hset(f"task:{task_id}", "type", type)

    set_status(task_id, "finished")
