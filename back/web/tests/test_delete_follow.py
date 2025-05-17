"""
test_delete_follow.py

Тест удаления подписки.
"""

import uuid

import pytest


@pytest.mark.asyncio
async def test_delete_follow(client, test_user):
    """Тест - Метод удалению подписки пользователя"""
    # Создание второго пользователя
    user2 = client.post(
        "/api/users/",
        json={
            "name": "UserToUnfollow",
            "password": "pass",
            "api_key": str(uuid.uuid4()),
        },
    ).json()
    user2_id = user2.get("id")
    assert user2_id is not None

    # Подписка на пользователя
    response = client.post(
        f"/api/users/{user2_id}/follow", headers={"api-key": "testkey"}
    )
    assert response.status_code == 200

    # Удаление подписки на пользователя
    response = client.delete(
        f"/api/users/{user2_id}/follow", headers={"api-key": "testkey"}
    )
    assert response.status_code == 200
    assert response.json() == {"result": True}

    # Повторная попытка удалить подписку
    response = client.delete(
        f"/api/users/{user2_id}/follow", headers={"api-key": "testkey"}
    )
    assert response.status_code == 404
