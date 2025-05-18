"""
test_get_user_by_id.py

Тест - получения информации о пользователе по id.
"""

import pytest


@pytest.mark.asyncio
async def test_get_user_by_id(client, test_user):
    """Тест получение информации о пользователе по id"""
    response = client.get(f"/api/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["user"]["id"] == test_user.id
