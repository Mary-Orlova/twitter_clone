"""
routes.py

Модуль Роуты/эндпоинты для работы с пользователями и подписками.
"""

from typing import Union

from fastapi import APIRouter, Depends, HTTPException, Response, Security
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import User, get_session
from ..logging_config import setup_custom_logger
from ..schemas_overal import ErrorSchema, OnlyResult
from ..users.schemas import (
    UserIn,
    UserOut,
    UserResultOutSchema,
)
from ..users.user_services import (
    api_key_header,
    delete_follow_to_user,
    get_current_user,
    get_user,
    get_user_me,
    post_follow_to_user,
    post_user,
)

logger = setup_custom_logger(__name__)
router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/{id}/follow",
    summary="Подписаться на пользователя",
    response_description="Результат подписки",
    response_model=Union[OnlyResult, ErrorSchema],
    status_code=200,
)
async def post_follow_to_user_handler(
    id: int,
    response: Response,
    session: AsyncSession = Depends(get_session),
    api_key: str = Security(api_key_header),
) -> Union[OnlyResult, ErrorSchema]:
    """
    Метод подписки текущего пользователя на пользователя с заданным id.

    :param response: Объект ответа FastAPI.
    :param id: ID пользователя, на которого подписываются.
    :param api_key: API-ключ пользователя, который подписывается.
    :param session: Асинхронная сессия SQLAlchemy.
    :return: Результат операции или ошибка.
    """

    current_user = await get_current_user(api_key=api_key, session=session)
    await post_follow_to_user(session=session, follower_id=current_user.id, user_id=id)
    return {"result": True}


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
    api_key: str = Security(api_key_header),
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
    current_user = await get_current_user(api_key=api_key, session=session)
    await delete_follow_to_user(
        session=session, follower_id=current_user.id, user_id=id
    )
    return {"result": True}


@router.get("/check-user/")
async def check_user(
    api_key: str = Security(api_key_header),
    session: AsyncSession = Depends(get_session),
):
    logger.info(f"Проверка пользователя api_key: {api_key}")
    result = await session.execute(select(User).where(User.api_key == api_key))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=404, detail="Пользователь с таким api-key не найден"
        )
    return {"id": user.id, "name": user.name, "api_key": user.api_key}


@router.get(
    "/me",
    summary="Получение информации о себе",
    response_description="Информация о текущем пользователе",
    response_model=Union[UserResultOutSchema, ErrorSchema],
    status_code=200,
)
async def get_user_me_handler(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> Union[UserResultOutSchema, ErrorSchema]:
    """
    Метод получения информации о текущем пользователе по api_key.
    """
    return await get_user_me(session, current_user.api_key)


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
    return await get_user(session=session, user_id=id)


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
