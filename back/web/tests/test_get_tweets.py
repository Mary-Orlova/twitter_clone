"""
test_get_tweets.py

Тест - получения твита.
"""

import pytest


@pytest.mark.asyncio
async def test_get_tweets(client, test_user):
    """Тест получения твита"""

    # Создание твита
    tweet = client.post(
        "/api/tweets/",
        json={"tweet_data": "Test", "tweet_media_ids": []},
        headers={"api-key": "testkey"},
    ).json()

    response = client.get("/api/tweets/", headers={"api-key": "testkey"})
    assert response.status_code == 200
    assert len(response.json()["tweets"]) == 1
