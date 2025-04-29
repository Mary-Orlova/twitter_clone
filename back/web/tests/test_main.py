from fastapi.testclient import TestClient
from back.web.project.main import app

test_client = TestClient(app)


def test_main(test_client):
    """Тест - возвращает id и name"""
    response = test_client.get("/api/test")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Mary"}
