from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Security

from .api.documents import router as document_router
from .api.tags import router as tags_router
from .api.tasks import router as tasks_router
from .auth import oidc, oauth2
from .db import init_db
from .db.models import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    create_tables()

    yield


app = FastAPI(lifespan=lifespan, dependencies=[Depends(oidc), Security(oauth2)])


app.include_router(document_router)
app.include_router(tasks_router)
app.include_router(tags_router)
