"""
schemas.py

Модуль Pydantic-схем валидации и передачи данных между сервисами Media - изображения.
"""

from pydantic import BaseModel, ConfigDict


class MediaOutSchema(BaseModel):
    """
    Схема ответа при загрузке изображения.

    :param result: bool - результат операции
    :param media_id: int - идентификатор медиафайла
    """

    result: bool = True
    media_id: int

    model_config = ConfigDict(from_attributes=True)
