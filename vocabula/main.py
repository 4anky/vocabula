from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from vocabula.api import (
    root_router,
    users_router,
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None]:
    yield


app = FastAPI(lifespan=lifespan, root_path='/api')
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],  # Vite dev server origin; or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(root_router)
app.include_router(users_router)
