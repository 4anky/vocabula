from datetime import datetime

import pytest
from fastapi import status
from sqlalchemy import select

from vocabula.models import User


@pytest.mark.asyncio
async def test_user_creation(db_session, client):
    """Tests the creation of user."""
    async with db_session as session:
        users_cur = await session.execute(select(User))
    assert users_cur.fetchone() is None

    resp = await client.post(
        '/users',
        json={'username': 'test_username'},
        headers={'Accept': 'application/json'},
    )
    assert resp.status_code == status.HTTP_201_CREATED, resp.content
    new_user = resp.json()
    assert set(new_user.keys()) == {'id', 'username', 'created_at'}
    assert new_user['username'] == 'test_username'
    assert new_user['id'] == 1
    assert isinstance(
        datetime.fromisoformat(new_user['created_at'].replace('Z', '+00:00')), datetime
    )

    async with db_session as session:
        users_cur = await session.execute(select(User))
    assert len(users_cur.fetchall()) == 1
