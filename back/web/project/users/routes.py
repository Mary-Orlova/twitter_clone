"""
Роуты/эндпоинты для работы с пользователями и подписками.
"""

from typing import Union

from fastapi import APIRouter, Depends, Header, Response
from sqlalchemy.ext.asyncio import AsyncSession

from project.database import get_session

from ..exeptions import BackendExeption
from ..schemas_overal import ErrorSchema, OnlyResult
from ..users.schemas import UserIn, UserOut, UserResultOutSchema
from ..users.user_services import (
    delete_follow_to_user,
    get_user,
    get_user_me,
    post_follow_to_user,
    post_user,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/{id}/follow",
    summary="Подписаться на пользователя",
    response_description="Результат подписки",
    response_model=Union[OnlyResult, ErrorSchema],
    status_code=200,
)
async def post_follow_to_user_handler(
    response: Response,
    id: int,
    api_key: str = Header(default="test"),
    session: AsyncSession = Depends(get_session),
) -> Union[OnlyResult, ErrorSchema]:
    """
    Метод подписки текущего пользователя на пользователя с заданным id.

    :param response: Объект ответа FastAPI.
    :param id: ID пользователя, на которого подписываются.
    :param api_key: API-ключ пользователя, который подписывается.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Результат операции или ошибка.
    """

    try:
        await post_follow_to_user(session=session, api_key=api_key, user_id=id)
        return {"result": True}
    except BackendExeption as error:
        response.status_code = 404
        return error


@router.delete(
    "/{id}/follow",
    summary="Отписаться от пользователя",
    response_description="Результат отписки",
    response_model=Union[OnlyResult, ErrorSchema],
    status_code=200,
)
async def delete_follow_to_user_handler(
    response: Response,
    id: int,
    api_key: str = Header(default="test"),
    session: AsyncSession = Depends(get_session),
) -> Union[OnlyResult, ErrorSchema]:
    """
    Метод отписки текущего пользователя от пользователя с заданным id

    :param response: Объект ответа FastAPI.
    :param id: ID пользователя, от которого отписываются.
    :param api_key: API-ключ пользователя, который отписывается.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Результат операции или ошибка.
    """
    try:
        await delete_follow_to_user(session=session, api_key=api_key, user_id=id)
        return {"result": True}
    except BackendExeption as error:
        response.status_code = 404
        return error


@router.get(
    "/me",
    summary="Получение информации о себе",
    response_description="Информация о текущем пользователе",
    response_model=Union[UserResultOutSchema, ErrorSchema],
    status_code=200,
)
async def get_user_me_handler(
    response: Response,
    api_key: str = Header(),
    session: AsyncSession = Depends(get_session),
) -> Union[UserResultOutSchema, ErrorSchema]:
    """
    Метод получения информации о текущем пользователе по api_key.

    :param response: Объект ответа FastAPI.
    :param api_key: API-ключ пользователя.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Данные пользователя или ошибка.
    """
    try:
        return await get_user_me(session=session, api_key=api_key)
    except BackendExeption as error:
        response.status_code = 404
        return error


@router.get(
    "/{id}",
    summary="Получение информации о пользователе по id",
    response_description="Информация о пользователе",
    response_model=Union[UserResultOutSchema, ErrorSchema],
    status_code=200,
)
async def get_user_by_id_handler(
    response: Response, id: int, session: AsyncSession = Depends(get_session)
) -> Union[UserResultOutSchema, ErrorSchema]:
    """
    Метод возвращения информации о пользователе по его id.

    :param response: Объект ответа FastAPI.
    :param id: ID пользователя.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Данные пользователя или ошибка.
    """
    try:
        return await get_user(session=session, user_id=id)
    except BackendExeption as error:
        response.status_code = 404
        return error


@router.post(
    "/",
    summary="Регистрация нового пользователя",
    response_description="Данные нового пользователя",
    response_model=UserOut,
)
async def post_users_handler(
    user: UserIn, session: AsyncSession = Depends(get_session)
) -> UserOut:
    """
    Метод создания нового пользователя.

    :param user: Данные пользователя (Pydantic-схема).
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Данные созданного пользователя.
    """

    return await post_user(session=session, user=user)
