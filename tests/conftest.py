"""
Тесты для репозиториев.
Здесь мы будем проверять, что наши методы взаимодействия с базой данных
работают корректно. Например, мы можем проверить, что при добавлении новой
задачи она действительно сохраняется в базе, или что при удалении
задачи она больше не доступна.
"""
import asyncio
import sys
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings
from app.core.database import get_db
from app.main import app
from app.models.base import Base

# Настройка для Windows (SelectorEventLoop необходим для некоторых драйверов БД)
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


engine = create_async_engine(settings.DATABASE_URL)
TestingSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Фикстура для создания чистой базы перед каждым тестом."""
    async with engine.begin() as conn:
        # Создаем таблицы (в 2025 году в тестах обычно используют Base.metadata)
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session
        # Очистка сессии после теста
        await session.rollback()

    async with engine.begin() as conn:
        # Удаляем таблицы, чтобы тесты были изолированы
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Фикстура для HTTP-клиента с подменой зависимости БД."""

    # Внутренняя функция для переопределения get_db
    async def _get_test_db():
        yield db_session

    app.dependency_overrides[get_db] = _get_test_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    # Очищаем переопределения, чтобы не аффектить другие тесты
    app.dependency_overrides.clear()
