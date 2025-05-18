"""
test_follow_user.py

Тест подписка на пользователя.
"""

import uuid

import pytest


@pytest.mark.asyncio
async def test_follow_user(client, test_user):
    """Тест подписки на пользователя"""

    # Создание второго пользователя
    user2 = client.post(
        "/api/users/",
        json={"name": "User2", "password": "pass", "api_key": str(uuid.uuid4())},
    ).json()

    user2_id = user2.get("id") or user2.get("user", {}).get("id")
    assert user2_id is not None, "Не найден id пользователя в ответе"

    # Создание подписки пользователя тестового на пользователя2
    response = client.post(
        f"/api/users/{user2_id}/follow", headers={"api-key": "testkey"}
    )
    assert response.status_code == 200
    assert response.json() == {"result": True}
