from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import FastAPI

from app.api.documents import router as document_router
from app.api.tasks import router as tasks_router
from app.config import Settings
from app.db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Подключаемся к БД
    init_db()

    yield


app = FastAPI(lifespan=lifespan)


@lru_cache
def get_settings():
    return Settings()


app.include_router(document_router)
app.include_router(tasks_router)
