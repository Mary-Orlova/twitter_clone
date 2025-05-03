"""
Роуты/эндпоинты для работы с твитами.
"""

from typing import Union

from fastapi import APIRouter, Depends, Header, Response
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..exeptions import BackendExeption
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
    :return: твит.
    """
    try:
        result = await get_tweet(session=session, tweet_id=id)
    except BackendExeption as error:
        response.status_code = 404
        result = error
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
    api_key: str = Header(default="test"),
    session: AsyncSession = Depends(get_session),
) -> Union[TweetListOutSchema, ErrorSchema]:
    """
    Метод получения твитов пользователя по api-key.
    :param response: Объект ответа FastAPI
    :param api_key: str - API-ключ пользователя
    :param session: асинхронная сессия SQLAlchemy

    :return: Список твитов.
    """
    try:
        result = await get_tweets(session=session, api_key=api_key)
    except BackendExeption as error:
        response.status_code = 404
        result = error
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
    api_key: str = Header(default="test"),
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
    try:
        new_tweet_id = await post_tweet(
            session=session,
            api_key=api_key,
            tweet_data=tweet.tweet_data,
        )
        if tweet.tweet_media_ids:
            await insert_media(
                session=session,
                tweet_id=new_tweet_id,
                tweet_medias=tweet.tweet_media_ids,
            )
        return {"result": True, "tweet_id": new_tweet_id}
    except BackendExeption as error:
        response.status_code = 404
        return error


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
    api_key: str = Header(default="test"),
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
    try:
        await delete_tweet(session=session, api_key=api_key, tweet_id=id)
        return {"result": True}
    except BackendExeption as error:
        response.status_code = 404
        return error


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
    api_key: str = Header(default="test"),
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
    try:
        await post_like(session=session, api_key=api_key, tweet_id=id)
        return {"result": True}
    except BackendExeption as error:
        response.status_code = 404
        return error


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
    api_key: str = Header(default="test"),
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
    try:
        await delete_like(session=session, api_key=api_key, tweet_id=id)
        return {"result": True}
    except BackendExeption as error:
        response.status_code = 404
        return error
