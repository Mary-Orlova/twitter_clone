"""
test_post_upload_media.py

Тест загрузки медиа-файла в твит.
"""

import pytest


@pytest.mark.asyncio
async def test_post_upload_media(client, test_user):
    """Тест загрузки медиа-файла"""
    files = {"file": ("test.txt", b"Test content", "text/plain")}
    response = client.post("/api/medias", headers={"api-key": "testkey"}, files=files)
