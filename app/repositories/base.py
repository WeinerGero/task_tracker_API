"""
Базовый репозиторий для работы с базой данных.
Содержит общие методы для всех репозиториев, такие как создание,
обновление, удаление и получение данных.
Каждый конкретный репозиторий будет наследоваться от этого базового класса
и реализовывать свои специфические методы для работы с определенной моделью
данных.
"""
from typing import TypeVar, Generic

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """Базовый репозиторий для работы с базой данных."""
    def __init__(self, model: type[T], session: AsyncSession):
        """Инициализация репозитория с моделью данных и сессией базы данных."""
        self.model = model
        self.session = session

    async def create(self, model: T) -> T:
        """Создание новой записи в базе данных."""
        self.session.add(model)     # Добавляем модель в сессию
        await self.session.flush()  # Сохраняем изменения в базе данных,
        return model                # чтобы получить ID новой записи

    async def delete_by_id(self, entity_id: int) -> bool:
        stmt = delete(self.model).where(self.model.id == entity_id)
        result = await self.session.execute(stmt)
        return result.rowcount > 0