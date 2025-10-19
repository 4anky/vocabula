from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from vocabula.api import (
    root_router,
    users_router,
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(root_router)
app.include_router(users_router)
