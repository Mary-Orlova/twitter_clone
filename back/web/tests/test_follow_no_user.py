"""
test_follow_no_user.py

Тест попытка подписаться на несуществующего пользователя.
"""

import pytest


@pytest.mark.asyncio
async def test_follow_no_user(client, test_user):
    """Тест попытка подписаться на несуществующего пользователя"""
    response = client.post("/api/users/999/follow", headers={"api-key": "testkey"})
    assert response.status_code == 404
    assert response.json() == {
        "result": False,
        "error_type": "NO USER",
        "error_message": "Нет пользователя с user_id для подписки",
    }
