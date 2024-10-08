from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.health import router

prep = "with NO lifespan"

@asynccontextmanager
async def lifespan(fast_api_app: FastAPI):
    global prep

    prep = "WITH lifespan"

    yield


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": prep}

app.include_router(
    router
)
