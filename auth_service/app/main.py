from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.security import HTTPBearer

from app.api.router import router
from app.db.base import Base
from app.db.session import engine

bearer_scheme = HTTPBearer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Auth Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health", tags=["system"])
async def health():
    return {"status": "ok"}