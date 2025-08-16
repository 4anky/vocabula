from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from vocabula.core import settings


@asynccontextmanager
async def _lifespan(api: FastAPI) -> AsyncIterator[None]:
    # await connect_db()
    yield
    # await disconnect_db()


app = FastAPI(lifespan=_lifespan)


@app.get('/')
async def root():
    return {
        'message': 'Hello from Vocabula!',
        'config': settings.model_dump(exclude_unset=True),
    }
