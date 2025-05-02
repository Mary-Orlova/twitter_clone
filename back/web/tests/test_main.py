"""
Модуль для тестирования базового эндпоинта приложения.
"""

from fastapi.testclient import TestClient

from back.web.project.main import app

# Инициализация тестового клиента FastAPI
test_client = TestClient(app)


def test_main(test_client):
    """
    Тест проверяет, что эндпоинт /api/test возвращает правильный id и name.

    :return: None
    """
    response = test_client.get("/api/test")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Mary"}
