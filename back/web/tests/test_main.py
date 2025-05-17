"""
test_main.py

Тест базового эндпоинта приложения.
"""

import pytest


@pytest.mark.asyncio
async def test_main(client):
    """
    Тест проверяет, что эндпоинт /api/test возвращает правильный id и name.

    :return: None
    """
    response = client.get("/api/test")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Mary"}
