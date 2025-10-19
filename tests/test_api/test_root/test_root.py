import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_healthcheck(client):
    resp = await client.get('/')
    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert resp.json() == {'message': 'Hello World'}
