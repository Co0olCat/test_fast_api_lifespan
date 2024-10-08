from fastapi import APIRouter, FastAPI
from contextlib import asynccontextmanager


health_prep = "with NO lifespan"


@asynccontextmanager
async def health_lifespan(app: FastAPI):
    global health_prep

    health_prep = "WITH lifespan"

    yield

router = APIRouter(lifespan=health_lifespan)


@router.get("/health")
async def health_check():
    global health_prep

    return {"status": health_prep}
