"""
Асинхронные сервисные функции для работы с пользователями и подписками (users и followers).
Для пользователя: Метод получения пользователя по API-ключу,
                    создание, получение, оформление и удаление подписки, получение информации о себе.
"""

from sqlalchemy import delete, insert, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .schemas import UserResultOutSchema
from ..database import User, followers
from ..exeptions import BackendExeption


async def get_user_by_api_key(session: AsyncSession, api_key: str) -> User:
    """
    Метод получения пользователя по API-ключу.

    :param session: Асинхронная сессия SQLAlchemy.
    :param api_key: API-ключ пользователя.
    :return: Объект пользователя (User).
    """

    # Запрос к БД для поиска пользователя по api_key
    result = await session.execute(select(User).where(User.api_key == api_key))
    user = result.scalars().one_or_none()

    # Если пользователь не найден - выбрасываем исключение
    if not user:
        raise BackendExeption(
            error_type="NO USER", error_message="Нет пользователя с таким api-key"
        )

    return user


async def post_follow_to_user(session: AsyncSession, api_key: str, user_id: int):
    """
    Метод оформления подписки на пользователя
    :param session: асинхронная сессия SQLAlchemy.
    :param api_key: API-ключ пользователя, который подписывается.
    :param user_id: id пользователя, на которого подписываются.
    :return: None
    """

    # Получение пользователя по api_key
    following_user = await get_user_by_api_key(session=session, api_key=api_key)

    # Запрет подписки на самого себя
    if following_user.id == user_id:
        raise BackendExeption(
            error_type="BAD FOLLOW",
            error_message="Пользователь не может подписаться на самого себя",
        )

    # Проверка существует ли пользователь, на которого планируется подписка
    query_result = await session.execute(select(User).where(User.id == user_id))
    user_followed = query_result.scalars().one_or_none()
    if not user_followed:
        raise BackendExeption(
            error_type="NO USER",
            error_message="Нет пользователя с user_id для подписки",
        )
    try:
        # Запись о подписке
        await session.execute(
            insert(followers).values(
                following_user_id=following_user.id,
                followed_user_id=user_id,
            )
        )
    except IntegrityError:
        # Исключение - подписка уже существует
        raise BackendExeption(
            error_type="BAD FOLLOW", error_message="Такая подписка уже существует"
        )
    await session.commit()


async def delete_follow_to_user(session: AsyncSession, api_key: str, user_id: int):
    """
    Метод отмены подписки на пользователя
    :param session: асинхронная сессия SQLAlchemy.
    :param api_key: API-ключ пользователя, который отписывается.
    :param user_id: id пользователя, от которого отписываются.
    :return: None
    """

    # Получение пользователя по api_key, который хочет отписаться
    following_user = await get_user_by_api_key(session=session, api_key=api_key)

    # Проверка существует ли такая подписка
    query_result = await session.execute(
        select(followers).where(
            followers.columns.following_user_id == following_user.id,
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
            followers.columns.following_user_id == following_user.id,
            followers.columns.followed_user_id == user_id,
        )
    )
    await session.commit()


async def get_user_me(session: AsyncSession, api_key: str):
    # Получить информацию о себе (по api_key)
    """
    Метод получения информации о себе
    :param session: асинхронная сессия SQLAlchemy.
    :param api_key: API-ключ текущего пользователя.
    :return: Словарь с результатом и объектом пользователя.
    """
    # user = await get_user_by_api_key(session=session, api_key=api_key)
    #
    # query_result = await session.execute(
    #     select(User)
    #     .options(selectinload(User.following))
    #     .options(selectinload(User.followers))
    #     .where(User.api_key == api_key)
    # )
    #
    # user = query_result.scalars().one_or_none()
    #
    # return {"result": True, "user": user}
    query_result = await session.execute(
        select(User)
        .options(selectinload(User.following))
        .options(selectinload(User.followers))
        .where(User.api_key == api_key)
    )
    user = query_result.scalars().one_or_none()
    if not user:
        raise BackendExeption(error_type="NO USER", error_message="Пользователь не найден")

    # Возвращаем Pydantic-модель, которая сериализует ORM-объект
    return UserResultOutSchema(result=True, user=user)


async def get_user(session: AsyncSession, user_id: int):
    """
    Метод получения пользователя
    :param session: асинхронная сессия SQLAlchemy.
    :param user_id: ID пользователя.
    :return: Словарь с результатом и объектом пользователя.
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

    return {"result": True, "user": user}


async def post_user(session: AsyncSession, user) -> User:
    """
    Метод создания нового пользователя
    :param session: Асинхронная сессия SQLAlchemy.
    :param user: Объект данных пользователя (обычно pydantic-модель).
    :return: Созданный объект пользователя.
    """
    new_user = User(**user.dict())
    async with session.begin():
        session.add(new_user)
        await session.commit()
    return new_user
