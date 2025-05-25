import uuid
from PIL import Image
from redis import Redis
from rq import Queue

from steps.ocr import ocr
from steps.signature_stamp import find_signature_stamp
from steps.split import split_pdf_to_images
from steps.type import get_document_type

queue_name = "pipeline"

redis = Redis()
queue = Queue(connection=redis, name=queue_name)


def set_status(task_id: str, status: str):
    redis.hset(f"task:{task_id}", "status", status)


def run_task(document_path: str) -> str:
    task_id = str(uuid.uuid4())

    queue.enqueue(process_document, task_id, document_path)

    return task_id


def process_document(task_id: str, document_path: str):
    set_status(task_id, "preprocessing")

    images = split_pdf_to_images(document_path)

    signature, stamp = find_signature_stamp(images)

    set_status(task_id, "processing")

    text = ocr(images)

    doc_type = get_document_type(text)

    redis.hset(
        f"task:{task_id}",
        mapping={
            "signature": str(signature),
            "stamp": str(stamp),
            "type": doc_type,
        },
    )

    set_status(task_id, "finished")


if __name__ == "__main__":
    image_paths = ['page1.png']
    images = [Image.open(p) for p in image_paths]

    text = ocr(images)
    print(text)
