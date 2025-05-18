"""
test_double_follow.py

Тест повторной подписки на одного и того же пользователя.
"""

import pytest


@pytest.mark.asyncio
async def test_double_follow(client, test_user):
    """Тест попытка повторной подписки"""
    user2 = client.post(
        "/api/users/",
        json={"name": "User2", "password": "pass", "api_key": "some-unique-key"},
    ).json()
    user2_id = user2.get("id")

    # Первая подписка
    client.post(f"/api/users/{user2_id}/follow", headers={"api-key": "testkey"})

    # Вторая попытка подписки
    response = client.post(
        f"/api/users/{user2_id}/follow", headers={"api-key": "testkey"}
    )
    assert response.status_code == 400
    assert response.json() == {
        "result": False,
        "error_type": "BAD FOLLOW",
        "error_message": "Такая подписка уже существует",
    }
