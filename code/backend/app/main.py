from fastapi import FastAPI
from app.routers.documents import router as router_documents

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

app.include_router(router_documents)