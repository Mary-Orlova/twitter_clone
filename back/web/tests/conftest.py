"""
Модуль конфигурационного файла в pytest
-Создание и управление асинхронной сессией базы данных для тестов
-Настраивает асинхронный движок SQLAlchemy с in-memory SQLite для изоляции тестов.
-Создаёт и очищает таблицы перед и после тестов.
-Предоставляет фикстуру session - асинхронную сессию для каждого теста, которая автоматически откатывается после теста.
-Переопределение зависимости FastAPI get_session для использования тестовой сессии
-Фикстура client создаёт тестовый HTTP-клиент FastAPI (TestClient), переопределяет зависимость get_session,
чтобы все запросы в тестах использовали тестовую сессию.
-Настройка асинхронного event loop для pytest-asyncio - запускает все асинхронные тесты в одном event loop
-Фикстура test_user создаёт и возвращает тестового пользователя, чтобы переиспользовать её в разных тестах.
"""

import asyncio

import pytest
from fastapi.testclient import TestClient
from project.database import Base, get_session
from project.main import app
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from back.web.project.users.schemas import UserIn
from back.web.project.users.user_services import post_user

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Асинхронный движок и сессия для тестов
engine_test = create_async_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def session_event_loop():
    """
    Создаёт и предоставляет один общий asyncio event loop на всю сессию тестирования.
    После завершения тестов цикл закрывается.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """Метод создаёт таблицы перед тестами и удаляет после"""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True)
async def cleanup_tables(session):
    """Метод удаление данных из всех таблиц после каждого теста"""
    yield
    for table in reversed(Base.metadata.sorted_tables):
        await session.execute(table.delete())
    await session.commit()


@pytest.fixture()
async def session():
    """Метод создания сессии для каждого теста"""
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()  # Откатываем все изменения после теста


@pytest.fixture()
def client(session: AsyncSession):
    """Метод клиента - Переопределение зависимости get_session в приложении"""

    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as connect:
        yield connect
    app.dependency_overrides.clear()


@pytest.fixture()
async def test_user(session: AsyncSession):
    """Фикстура для тестового пользователя"""
    user_data = UserIn(name="Test User", api_key="testkey", password="testpass")
    user = await post_user(session, user_data)
    return user
