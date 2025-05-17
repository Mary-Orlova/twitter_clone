"""
media_services.py

Модуль media_services - публикация изображений в твите и проверка типа файла.
"""

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import Media
from ..exceptions import BackendException


async def post_image(session: AsyncSession, image_name: str) -> dict:
    """
    Метод публикации изображения в базе данных.

    :param session: Асинхронная сессия SQLAlchemy.
    :param image_name: Название файла изображения.
    :return: Словарь с результатом и media_id.
    """
    # Вставка новой записи в таблицу Media
    query_result = await session.execute(insert(Media).values(name=image_name))
    image_id = query_result.inserted_primary_key[0]
    await session.commit()
    return {"result": True, "media_id": image_id}


def check_file(file) -> None:
    """
    Метод проверки типа файла.

    :param file: Загруженный файл.
    """
    if file.content_type not in ("image/jpeg", "image/png"):
        raise BackendException(
            error_type="BAD FILE",
            error_message="Ошибка! Поддерживаемые типы изображений: jpeg, png.",
        )
