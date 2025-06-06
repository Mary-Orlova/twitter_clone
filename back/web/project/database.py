"""
database.py

Модуль для база данных с настройками, классами-таблицами представлениями:
 followers, users, tweets, medias, likes.
"""

from typing import Any, Dict

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = "postgresql+asyncpg://admin:admin@db:5432/diplom_project"
engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_session():
    async with async_session() as session:
        yield session


followers = Table(
    "followers",
    Base.metadata,
    Column(
        "following_user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "followed_user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class User(Base):
    """Класс пользователя User, таблица users"""

    __tablename__: str = "users"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    name = Column(String, index=True)
    api_key = Column(String, index=True, unique=True)
    password = Column(String, index=True)

    # Пользователи, на которых подписан этот пользователь (подписки)
    following = relationship(
        "User",
        secondary=followers,
        primaryjoin=id == followers.c.following_user_id,
        secondaryjoin=id == followers.c.followed_user_id,
        back_populates="followers",
        lazy="selectin",
    )

    # Пользователи, которые подписаны на этого пользователя (подписчики)
    followers = relationship(
        "User",
        secondary=followers,
        primaryjoin=id == followers.c.followed_user_id,
        secondaryjoin=id == followers.c.following_user_id,
        back_populates="following",
        lazy="selectin",
    )

    tweets = relationship(
        "Tweet",
        back_populates="author",
        cascade="all, delete",
        passive_deletes=True,
    )

    likes = relationship(
        "Like",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"Пользователь {self.name}"

    def to_json(self) -> Dict[str, Any]:
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Tweet(Base):
    """Класс твитов - сообщений, таблица tweets"""

    __tablename__ = "tweets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content = Column(String, index=True)

    attachments = association_proxy("media", "name")

    author = relationship("User", back_populates="tweets")

    media = relationship(
        "Media",
        back_populates="tweet",
        cascade="all, delete",
        passive_deletes=True,
    )
    likes = relationship(
        "Like",
        back_populates="tweet",
        cascade="all, delete",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"Твит {self.tweet_data}"

    def to_json(self) -> Dict[str, Any]:
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Media(Base):
    """Класс медиа, таблица medias"""

    __tablename__ = "medias"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    tweet_id = Column(Integer, ForeignKey("tweets.id", ondelete="CASCADE"))
    tweet = relationship("Tweet", back_populates="media")

    def __repr__(self):
        return f"Медиа {self.name}"

    def to_json(self) -> Dict[str, Any]:
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Like(Base):
    """Класс лайков-отметки 'нравится', таблица likes"""

    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint("user_id", "tweet_id", name="_unique_who_tweet_likes"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    tweet_id = Column(ForeignKey("tweets.id", ondelete="CASCADE"), index=True)

    user = relationship("User", back_populates="likes")
    tweet = relationship("Tweet", back_populates="likes")

    name = association_proxy("user", "name")

    def __repr__(self):
        return f"Лайк {self.id}"

    def to_json(self) -> Dict[str, Any]:
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
