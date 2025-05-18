"""
test_post_like_tweet.py

Тест простановки лайка на твит.
"""

import pytest


@pytest.mark.asyncio
async def test_post_like_tweet(client, test_user):
    """Тест лайк на твит"""

    tweet = client.post(
        "/api/tweets/", json={"tweet_data": "Like test"}, headers={"api-key": "testkey"}
    ).json()

    tweet_id = tweet.get("tweet_id") or tweet.get("id")
    assert tweet_id is not None, "tweet_id не найден в ответе"

    response = client.post(
        f"/api/tweets/{tweet_id}/likes", headers={"api-key": "testkey"}
    )
    assert response.status_code == 200
