"""
test_delete_like.py

Тест удаления лайка пользователя с твита.
"""

import pytest


@pytest.mark.asyncio
async def test_delete_like(client, test_user):
    """Тест - Метод удалению лайка пользователя с твита"""
    # Создание твита
    tweet = client.post(
        "/api/tweets/",
        json={"tweet_data": "Test tweet for unlike"},
        headers={"api-key": "testkey"},
    ).json()
    tweet_id = tweet.get("tweet_id") or tweet.get("id")
    assert tweet_id is not None

    # Простановка лайка
    response = client.post(
        f"/api/tweets/{tweet_id}/likes", headers={"api-key": "testkey"}
    )
    assert response.status_code == 200

    # Удаление лайка с твита
    response = client.delete(
        f"/api/tweets/{tweet_id}/likes", headers={"api-key": "testkey"}
    )
    assert response.status_code == 200
    assert response.json() == {"result": True}

    # Попытка удалить лайк повторно
    response = client.delete(
        f"/api/tweets/{tweet_id}/likes", headers={"api-key": "testkey"}
    )

    assert response.status_code == 404
