"""
Асинхронные сервисные функции для работы с пользователями и подписками (users и followers).
Для пользователя: Метод получения пользователя по API-ключу,
                    создание, получение, оформление и удаление подписки, получение информации о себе.
"""

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..database import User, followers, get_session
from ..exeptions import BackendExeption
from ..logging_config import setup_custom_logger
from .schemas import UserOutSchema, UserResultOutSchema

logger = setup_custom_logger(__name__)

api_key_header = APIKeyHeader(name="api-key", auto_error=True)


async def get_current_user(
    api_key: str = Security(api_key_header),
    session: AsyncSession = Depends(get_session),
) -> User:
    """
    Метод получения пользователя по API-ключу.
    Зависимость аутентификации.

    :param session: Асинхронная сессия SQLAlchemy.
    :param api_key: API-ключ пользователя.
    :return: Объект пользователя (User).
    """

    logger.info(f"Метод get_current_user API key: {api_key}")

    # Запрос к БД для поиска пользователя по api_key
    result = await session.execute(select(User).where(User.api_key == api_key))

    user = result.scalars().first()

    # Если пользователь не найден - выбрасываем исключение
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Не валидный API Key"
        )
    return user


async def post_follow_to_user(session: AsyncSession, follower_id: int, user_id: int):
    """
    Метод оформления подписки на пользователя
    :param session: асинхронная сессия SQLAlchemy.
    :param follower_id: id пользователя, который подписывается.
    :param user_id: id пользователя, на которого подписываются.
    :return: None
    """
    if follower_id == user_id:
        raise BackendExeption(
            error_type="BAD FOLLOW",
            error_message="Пользователь не может подписаться на самого себя",
            status_code=400,
        )

    query_result = await session.execute(select(User).where(User.id == user_id))
    user_followed = query_result.scalars().one_or_none()
    if not user_followed:
        raise BackendExeption(
            error_type="NO USER",
            error_message="Нет пользователя с user_id для подписки",
        )
    try:
        await session.execute(
            insert(followers).values(
                following_user_id=follower_id,
                followed_user_id=user_id,
            )
        )
    except IntegrityError:
        raise BackendExeption(
            error_type="BAD FOLLOW",
            error_message="Такая подписка уже существует",
            status_code=400,
        )
    await session.commit()


async def delete_follow_to_user(session: AsyncSession, follower_id: int, user_id: int):
    """
    Метод отмены подписки на пользователя
    :param session: асинхронная сессия SQLAlchemy.
    :param follower_id: ID пользователя, который отписывается.
    :param user_id: ID пользователя, от которого отписываются.
    :return: None
    """

    # Проверка существует ли такая подписка
    query_result = await session.execute(
        select(followers).where(
            followers.columns.following_user_id == follower_id,
            followers.columns.followed_user_id == user_id,
        )
    )
    follower = query_result.scalars().one_or_none()
    if not follower:
        raise BackendExeption(
            error_type="BAD FOLLOW DELETE", error_message="Нет такого фолловера"
        )

    # Удаление записи о подписке
    await session.execute(
        delete(followers).where(
            followers.columns.following_user_id == follower_id,
            followers.columns.followed_user_id == user_id,
        )
    )
    await session.commit()


async def get_user_me(session: AsyncSession, api_key: str) -> UserResultOutSchema:
    """
    Метод получения информации о текущем пользователе по api-key
    :param session: асинхронная сессия SQLAlchemy.
    :param api_key: API-ключ текущего пользователя.
    :return: Объект пользователя
    """
    query_result = await session.execute(
        select(User)
        .options(selectinload(User.followers))
        .options(selectinload(User.following))
        .where(User.api_key == api_key)
    )
    user = query_result.scalars().one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Преобразование ORM-модель в Pydantic-схему с вложенными подписчиками и подписками
    user_schema = UserOutSchema.from_orm(user)
    return UserResultOutSchema(result=True, user=user_schema)


async def get_user(session: AsyncSession, user_id: int):
    """
    Метод получения пользователя по id
    :param session: асинхронная сессия SQLAlchemy.
    :param user_id: ID пользователя.
    :return: Объект пользователя.
    """
    query_result = await session.execute(
        select(User)
        .options(selectinload(User.following))
        .options(selectinload(User.followers))
        .where(User.id == user_id)
    )

    user = query_result.scalars().one_or_none()
    if not user:
        raise BackendExeption(
            error_type="NO USER", error_message="Нет пользователя с таким id"
        )
    user_schema = UserOutSchema.from_orm(user)
    return UserResultOutSchema(result=True, user=user_schema)


async def post_user(session: AsyncSession, user) -> User:
    """
    Метод создания нового пользователя
    :param session: Асинхронная сессия SQLAlchemy.
    :param user: Объект данных пользователя (pydantic-модель).
    :return: Созданный объект пользователя.
    """
    new_user = User(**user.dict())
    async with session.begin():
        session.add(new_user)
        await session.commit()
    return new_user
