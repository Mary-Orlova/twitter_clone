"""
schemas.py

Модуль Pydantic-схем для валидации данных и обмена данных между сервисами.

"""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class BaseUser(BaseModel):
    """
    Схема базовая пользователя.

    :param api_key: API-ключ пользователя.
    :param name: Имя пользователя.
    :param password: Пароль пользователя.
    """

    api_key: str
    name: str
    password: Optional[str]


class UserIn(BaseUser):
    """
    Схема для входящих данных пользователя (регистрация/создание).
    """

    pass


class UserOut(BaseUser):
    """
    Схема для вывода данных пользователя (ответ клиенту).

    :param id: Идентификатор пользователя в БД.
    """

    id: int

    model_config = ConfigDict(from_attributes=True)


class AuthorBaseSchema(BaseModel):
    """
    Схема базовая для автора.

    :param id: Идентификатор пользователя.
    :param name: Имя пользователя.
    """

    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class AuthorLikeSchema(BaseModel):
    """
    Схема автора для лайков.

    :param user_id: Идентификатор пользователя.
    :param name: Имя пользователя.
    """

    user_id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserOutSchema(BaseModel):
    """
    Схема пользователя для с подписчиками и подписками.

    :param id: Идентификатор пользователя.
    :param name: Имя пользователя.
    :param followers: Список подписчиков.
    :param following: Список пользователей, на которых подписан пользователь.
    """

    id: int
    name: str
    followers: Optional[List[AuthorBaseSchema]]
    following: Optional[List[AuthorBaseSchema]]

    model_config = ConfigDict(from_attributes=True)


class UserResultOutSchema(BaseModel):
    """
    Схема результата поиска пользователя.

    :param result: Флаг успешности.
    :param user: Данные пользователя.
    """

    result: bool = True
    user: UserOutSchema

    model_config = ConfigDict(from_attributes=True)
