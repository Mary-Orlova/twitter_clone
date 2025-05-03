"""
Pydantic-схемы для валидации данных и обмена данных между сервисами.

"""

from typing import List, Optional

from pydantic import BaseModel


class BaseUser(BaseModel):
    """
    Базовая схема пользователя.

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

    class Config:
        orm_mode = True


class AuthorBaseSchema(BaseModel):
    """
    Базовая схема автора -  отображение в списках.

    :param id: Идентификатор пользователя.
    :param name: Имя пользователя.
    """

    id: int
    name: str

    class Config:
        orm_mode = True


class AuthorLikeSchema(BaseModel):
    """
    Схема автора для лайков.

    :param user_id: Идентификатор пользователя.
    :param name: Имя пользователя.
    """

    user_id: int
    name: str

    class Config:
        orm_mode = True


class UserOutSchema(BaseModel):
    """
    Схема пользователя для фронтенда с подписчиками и подписками.

    :param id: Идентификатор пользователя.
    :param name: Имя пользователя.
    :param followers: Список подписчиков.
    :param following: Список пользователей, за которыми следит пользователь.
    """

    id: int
    name: str
    followers: Optional[List[AuthorBaseSchema]]
    following: Optional[List[AuthorBaseSchema]]

    class Config:
        orm_mode = True


class UserResultOutSchema(BaseModel):
    """
    Схема результата поиска пользователя.

    :param result: Флаг успешности.
    :param user: Данные пользователя.
    """

    result: bool = True
    user: UserOutSchema

    class Config:
        orm_mode = True
