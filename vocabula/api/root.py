from fastapi import APIRouter

from ..services import get_hello

__all__ = ('root_router',)

root_router = APIRouter(prefix='', tags=['Health Check'])


@root_router.get('/')
async def health_check() -> dict[str, str]:
    return await get_hello()
