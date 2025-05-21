from contextlib import asynccontextmanager
from functools import lru_cache

import httpx
from fastapi import FastAPI

from app.api.documents import router as document_router
from app.api.login.keycloak_client import KeycloakClient
from app.api.tags import router as tags_router
from app.api.tasks import router as tasks_router
from app.api.login.authorization import router as login_router
from app.config import Settings
from app.db import init_db
from app.db.models import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    create_tables()
    http_client = httpx.AsyncClient()
    app.state.keycloak_client = KeycloakClient(http_client)
    yield


app = FastAPI(lifespan=lifespan)


@lru_cache
def get_settings():
    return Settings()


app.include_router(document_router)
app.include_router(tasks_router)
app.include_router(tags_router)
app.include_router(login_router)
