"""
test_post_user.py

Тест создания пользователя.
"""

import pytest


@pytest.mark.asyncio
async def test_post_user(client):
    """Тест создания пользователя"""
    response = client.post(
        "/api/users/",
        json={
            "name": "New User",
            "password": "newpass",
        },
    )
