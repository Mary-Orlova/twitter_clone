"""
routes.py

Модуль Роуты/эндпоинты для работы с твитами.
"""

from typing import Union

from fastapi import APIRouter, Depends, Response, Security
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..schemas_overal import ErrorSchema, OnlyResult
from ..tweets.schemas import (
    BaseAnsTweet,
    TweetIn,
    TweetListOutSchema,
    TweetSchema,
)
from ..tweets.tweets_services import (
    delete_like,
    delete_tweet,
    get_tweet,
    get_tweets,
    insert_media,
    post_like,
    post_tweet,
)
from ..users.user_services import api_key_header

router = APIRouter(prefix="/tweets", tags=["Tweets"])


@router.get(
    "/{id}",
    summary="Получение твита по id",
    response_description="Твит",
    response_model=Union[TweetSchema, ErrorSchema],
    status_code=200,
)
async def get_tweet_handler(
    response: Response,
    id: int,
    session: AsyncSession = Depends(get_session),
) -> Union[TweetSchema, ErrorSchema]:
    """
    Метод получения твита по id.
    :param  response: Объект ответа FastAPI
    :param id: int - идентификатор твита в БД
    :param  session: асинхронная сессия SQLAlchemy
    :return: твит или ошибка.
    """
    result = await get_tweet(session=session, tweet_id=id)
    return result


@router.get(
    "/",
    summary="Получение твитов пользователя по api-key",
    response_description="Список твитов",
    response_model=Union[TweetListOutSchema, ErrorSchema],
    status_code=200,
)
async def get_tweets_handler(
    response: Response,
    api_key: str = Security(api_key_header),
    session: AsyncSession = Depends(get_session),
) -> Union[TweetListOutSchema, ErrorSchema]:
    """
    Метод получения твитов пользователя по api-key.
    :param response: Объект ответа FastAPI
    :param api_key: str - API-ключ пользователя
    :param session: асинхронная сессия SQLAlchemy

    :return: Список твитов.
    """
    result = await get_tweets(api_key=api_key, session=session)
    return result


@router.post(
    "/",
    summary="Публикация твита",
    response_description="Результат публикации твита",
    response_model=Union[BaseAnsTweet, ErrorSchema],
    status_code=200,
)
async def post_tweets_handler(
    response: Response,
    tweet: TweetIn,
    api_key: str = Security(api_key_header),
    session: AsyncSession = Depends(get_session),
) -> Union[BaseAnsTweet, ErrorSchema]:
    """
    Метод публикации твита пользователя по api-key.

    :param response: Объект ответа FastAPI
    :param tweet: TweetIn - данные твита (текст, медиа)
    :param api_key: str - API-ключ пользователя
    :param session: асинхронная сессия SQLAlchemy

    :return: Результат публикации твита.
    """
    new_tweet_id = await post_tweet(
        api_key=api_key,
        session=session,
        tweet_data=tweet.tweet_data,
    )
    if tweet.tweet_media_ids:
        await insert_media(
            session=session,
            tweet_id=new_tweet_id,
            tweet_medias=tweet.tweet_media_ids,
        )
    return {"result": True, "tweet_id": new_tweet_id}


@router.delete(
    "/{id}",
    summary="Удаление твита",
    response_description="Результат удаления твита",
    response_model=Union[OnlyResult, ErrorSchema],
    status_code=200,
)
async def delete_tweets_handler(
    response: Response,
    id: int,
    api_key: str = Security(api_key_header),
    session: AsyncSession = Depends(get_session),
) -> Union[OnlyResult, ErrorSchema]:
    """
    Метод удаления твита пользователя по api-key и id твита.

    :param response: объект ответа FastAPI
    :param id: int - идентификатор твита
    :param api_key: str - API-ключ пользователя
    :param session: асинхронная сессия SQLAlchemy

    :return: Результат удаления твита.
    """
    await delete_tweet(api_key=api_key, session=session, tweet_id=id)
    return {"result": True}


@router.post(
    "/{id}/likes",
    summary="Поставить лайк твиту",
    response_description="Результат операции или сообщение об ошибке",
    response_model=Union[OnlyResult, ErrorSchema],
    status_code=200,
)
async def post_like_to_tweet_handler(
    response: Response,
    id: int,
    api_key: str = Security(api_key_header),
    session: AsyncSession = Depends(get_session),
) -> Union[OnlyResult, ErrorSchema]:
    """
    Метод установки лайка твиту по api-key и id твита.

    :param  response: Объект ответа FastAPI
    :param  id: int - идентификатор твита
    :param  api_key: str - API-ключ пользователя
    :param  session: асинхронная сессия SQLAlchemy

    :return: Результат операции установки лайка.
    """
    await post_like(api_key=api_key, session=session, tweet_id=id)
    return {"result": True}


@router.delete(
    "/{id}/likes",
    summary="Удалить лайк с твита",
    response_description="Результат удаления лайка",
    response_model=Union[OnlyResult, ErrorSchema],
    status_code=200,
)
async def delete_like_to_tweet_handler(
    response: Response,
    id: int,
    api_key: str = Security(api_key_header),
    session: AsyncSession = Depends(get_session),
) -> Union[OnlyResult, ErrorSchema]:
    """
    Метод удаления лайка по api-key и id твита.

    :param  response: Объект ответа FastAPI
    :param  id: int - идентификатор твита
    :param api_key: str - API-ключ пользователя
    :param  session: асинхронная сессия SQLAlchemy

    :return: Результат удаления лайка с твита.
    """
    await delete_like(api_key=api_key, session=session, tweet_id=id)
    return {"result": True}
