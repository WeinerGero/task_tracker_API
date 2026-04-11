"""
Тесты для репозиториев.
Здесь мы будем проверять, что наши методы взаимодействия с базой данных
работают корректно. Например, мы можем проверить, что при добавлении новой
задачи она действительно сохраняется в базе, или что при удалении
задачи она больше не доступна.
"""
import sys
import asyncio

# Настройка для Windows, чтобы избежать проблем с асинхронностью
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.models.base import Base

TEST_DB_URL = "postgresql+psycopg://postgres:postgres@127.0.0.1:5433/taskservice"

engine = create_async_engine(TEST_DB_URL)
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@pytest_asyncio.fixture
async def db_session():
    # 1. Создаем таблицы перед тестом
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2. Выдаем сессию
    async with TestingSessionLocal() as session:
        yield session

    # 3. Удаляем таблицы после теста (очистка)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)