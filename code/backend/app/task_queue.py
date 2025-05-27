import uuid
from dataclasses import dataclass
from enum import Enum

from redis import Redis
from rq import Queue

from .config import Settings
from .db.models import DocumentTypeModel

QUEUE_NAME = "documents"
MODEL = "gemma3:4b"  # TODO (~oryce, 27.05.25): Don't hardcode the model
WORKER_ENTRYPOINT = "app.command.run.worker_entrypoint"

_settings = Settings()

_redis = Redis(
    host=_settings.redis_host,
    port=_settings.redis_port,
    password=_settings.redis_password,
    decode_responses=True,
)

_queue = Queue(QUEUE_NAME, connection=_redis)


class Status(Enum):
    ENQUEUED = 0
    PREPROCESSING = 1
    PROCESSING = 2
    FINISHED = 3


@dataclass
class Result:
    type: str
    signature: bool
    stamp: bool
    doc_id: str


def enqueue(document_path: str) -> str:
    task_id = str(uuid.uuid4())
    allowed_types = [type.name for type in DocumentTypeModel.select()]

    _queue.enqueue(
        WORKER_ENTRYPOINT,
        task_id,
        document_path,
        allowed_types,
        MODEL,
    )

    return task_id


def get_task_status(task_id: str) -> Status | None:
    if status := _redis.hget(f"task:{task_id}", "status"):
        return Status[status]
    else:
        return None


def get_task_result(task_id: str) -> Result | None:
    task = _redis.hgetall(f"task:{task_id}")

    if task["status"] != str(Status.FINISHED.name):
        return None

    return Result(
        task["type"],
        task["signature"] == "True",
        task["stamp"] == "True",
        task["doc_id"],
    )
