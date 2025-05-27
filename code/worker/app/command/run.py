from os import getenv
from pathlib import Path

from redis import Redis
from rq import Worker

from ..pipeline import Result, Status
from ..pipeline import run as run_pipeline

_redis = Redis(
    host=getenv("REDIS_HOST"),
    port=int(getenv("REDIS_PORT") or 6379),
    password=getenv("REDIS_PASSWORD"),
)


def command(args):
    worker = Worker([getenv("QUEUE")], connection=_redis)
    worker.work()


def worker_entrypoint(
    task_id: str, document_path: str, allowed_types: list[str], model: str
) -> dict[str, any]:
    for value in run_pipeline(document_path, allowed_types, model):
        if isinstance(value, Status):
            _redis.hset(f"task:{task_id}", "status", str(value.name))
        if isinstance(value, Result):
            _redis.hset(f"task:{task_id}", mapping={
                "type": value.type,
                "signature": str(value.signature),
                "stamp": str(value.stamp),
                # This is an awful hack.
                "doc_id": Path(document_path).name.replace(".pdf", ""),
            })
