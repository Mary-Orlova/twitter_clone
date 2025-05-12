"""
Pydantic-схемы для валидации и обмена данными между твитами.
"""

from typing import List, Optional, Sequence

from pydantic import BaseModel, ConfigDict, Field, validator
from sqlalchemy.ext.associationproxy import _AssociationList

from ..users.schemas import AuthorBaseSchema, AuthorLikeSchema


class TweetIn(BaseModel):
    """
    Схема для создания твита (входные данные).

    :param tweet_data: str - текст твита.
    :param tweet_media_ids: List[int], optional - список ID медиафайлов.
    """

    tweet_data: str = Field(..., description="Содержание твита")
    tweet_media_ids: Optional[List[int]] = Field(
        default=None, description="Список идентификаторов картинок"
    )

    model_config = ConfigDict(from_attributes=True)


class BaseAnsTweet(BaseModel):
    """
    Схема базового ответа при публикации твита.

    :param None
    :return: bool, tweet_id
    """

    result: bool = Field(..., description="Флаг успешного добавления твита")
    tweet_id: int = Field(..., description="Идентификатор твита в СУБД")


class TweetSchema(BaseModel):
    """
    Схема базового твита.

    :param id: int - идентификатор твита.
    :param content: str - текст твита.
    :param attachments: List[str], optional - список вложений.
    :param author: AuthorBaseSchema - автор твита.
    :param likes: List[AuthorLikeSchema], optional - пользователи, поставившие лайк.
    """

    id: int = Field(..., description="Идентификатор твита")
    content: str = Field(..., example="супер твит", description="Содержание твита")
    attachments: Optional[Sequence[str]] = Field(
        default=None, description="Список вложений"
    )
    author: AuthorBaseSchema = Field(..., description="Автор твита")
    likes: Optional[List[AuthorLikeSchema]] = Field(
        default=None, description="Пользователи, поставившие лайк"
    )

    @validator("attachments", pre=True)
    def validate_attachments(cls, v):
        """
        Валидирует, что attachments - это последовательность.
        """
        if isinstance(v, _AssociationList) or isinstance(v, (list, tuple, set)):
            return list(v)
        raise ValueError("Вложения должны иметь допустимую последовательность.")

    model_config = ConfigDict(from_attributes=True)


class TweetListOutSchema(BaseModel):
    """
    Схема ответа со списком твитов.

    :param result: bool.
    :param tweets: List[TweetSchema], optional - список твитов.
    """

    result: bool = Field(True, description="Флаг успешного выполнения")
    tweets: Optional[List[TweetSchema]] = Field(
        default=None, description="Список твитов"
    )
