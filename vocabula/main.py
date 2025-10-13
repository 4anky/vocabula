import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from vocabula.api import (
    root_router,
    users_router,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await asyncio.create_subprocess_exec('alembic', 'upgrade', 'head')
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(root_router)
app.include_router(users_router)
