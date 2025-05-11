import asyncio
from database import async_session
from database import User, followers
from sqlalchemy.future import select
from sqlalchemy import insert
from logging_config import setup_custom_logger

logger = setup_custom_logger(__name__)

async def init_data():
    async with async_session() as session:
        # Проверка, есть ли тестовый пользователь
        result = await session.execute(select(User).filter_by(api_key="test"))
        test_user = result.scalars().first()
        if test_user:
            logger.info("Тестовый пользователь уже существует, пропускаем инициализацию.")
            return

        # Создаём пользователей
        users_data = [
            {"name": "Тестовый пользователь", "api_key": "test", "password": "testpass"},
            {"name": "Александр", "api_key": "xsan", "password": "passalex"},
            {"name": "Алексей", "api_key": "lexy", "password": "passalexey"},
            {"name": "Евгений", "api_key": "gaw", "password": "passevg"},
            {"name": "Александра", "api_key": "yoyo", "password": "passalexandra"},
            {"name": "Евгения", "api_key": "woppy", "password": "passevgys"},
            {"name": "Дарья", "api_key": "toradora", "password": "passdaria"},
            {"name": "Иван", "api_key": "ivolga", "password": "passivano"},
        ]

        # Вставка пользователей через bulk insert
        await session.execute(insert(User), users_data)
        await session.commit()

        # Получаем всех пользователей с именами, чтобы получить их id
        result = await session.execute(select(User))
        users = result.scalars().all()

        # Нахожу тестового пользователя и его друзей
        test_user = next(user for user in users if user.api_key == "test")
        friend_names = {"Александр", "Алексей", "Евгений", "Александра"}
        friends = [user for user in users if user.name in friend_names]

        # Добавляем связи followers
        followers_data = [
            {"following_user_id": test_user.id,
             "followed_user_id": friend.id}
            for friend in friends
        ]

        await session.execute(insert(followers), followers_data)
        await session.commit()

        logger.info("Тестовые данные успешно добавлены.")

if __name__ == "__main__":
    asyncio.run(init_data())
