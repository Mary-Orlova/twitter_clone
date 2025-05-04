"""
Pydantic-схема для валидации и передачи данных между сервисами Media - изображения.
"""

from pydantic import BaseModel


class MediaOutSchema(BaseModel):
    """
    Схема ответа при загрузке изображения.

    :param result: bool - результат операции
    :param media_id: int - идентификатор медиафайла
    """

    result: bool = True
    media_id: int

    class Config:
        orm_mode = True
