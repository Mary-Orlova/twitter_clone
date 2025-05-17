"""
test_self_follow.py

Тест попытка подписаться на самого себя.
"""

import pytest


@pytest.mark.asyncio
async def test_self_follow(client, test_user):
    """Тест попытка подписаться на самого себя"""
    response = client.post(
        f"/api/users/{test_user.id}/follow", headers={"api-key": "testkey"}
    )
    assert response.status_code == 400
    assert response.json() == {
        "result": False,
        "error_type": "BAD FOLLOW",
        "error_message": "Пользователь не может подписаться на самого себя",
    }
