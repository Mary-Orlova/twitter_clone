"""
test_post_tweet.py

Тест создания твита.
"""

import pytest


@pytest.mark.asyncio
async def test_post_tweet(client, test_user):
    """Тест создание твита"""
    tweet_data = {"tweet_data": "Test tweet content", "tweet_media_ids": []}
    response = client.post(
        "/api/tweets/", json=tweet_data, headers={"api-key": "testkey"}
    )
    assert response.status_code == 200
    assert "tweet_id" in response.json()
