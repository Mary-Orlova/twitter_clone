"""
test_get_current_user.py

Тест - получения текущего пользователя через зависимость авторизации.
"""

import pytest


@pytest.mark.asyncio
async def test_get_current_user(client, test_user):
    """Тест получения текущего пользователя через зависимость авторизации""" ""
    response = client.get("/api/users/me", headers={"api-key": "testkey"})
    assert response.status_code == 200
    data = response.json()
    assert data["result"] is True
    assert data["user"]["name"] == "Test User"
