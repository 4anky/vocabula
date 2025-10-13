__all__ = ('get_hello',)


async def get_hello() -> dict[str, str]:
    return {'message': 'Hello World'}
