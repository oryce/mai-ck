from redis import Redis
from rq import Queue
from steps.split import split_document_to_images
from steps.ocr import run_ocr
from steps.ollama import get_doc_type
from steps.search_sig_stamp import search_signature_and_stamp
import uuid

queue_name = "doc_pipeline"
redis_conn = Redis()
q = Queue(connection=redis_conn, name=queue_name)


def update_status(task_id, status):
    redis_conn.hset(f"task:{task_id}", "status", status)


def run_task(doc_path: str):
    q.enqueue(process_document, doc_path)


def process_document(doc_path):
    task_id = str(uuid.uuid4())
    update_status(task_id, "received")

    update_status(task_id, "splitting")
    images = split_document_to_images(doc_path)

    update_status(task_id, "search_sig_print")
    has_stamp, has_sig = search_signature_and_stamp(images)

    update_status(task_id, "ocr")
    text = run_ocr(images)

    update_status(task_id, "uploading")
    doc_type = get_doc_type(text)

    redis_conn.hset(f"task:{task_id}", "has_stamp", has_stamp)
    redis_conn.hset(f"task:{task_id}", "has_sig", has_sig)
    redis_conn.hset(f"task:{task_id}", "doc_type", doc_type)
    update_status(task_id, "done")

    return task_id
