"""
Репозиторий для работы с задачами.
Содержит методы для создания, получения и обновления задач.
"""
# pylint: disable=import-error
from datetime import date

from sqlalchemy import insert, select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.base import BaseRepository
from app.models.tasks import Task


class TaskRepository(BaseRepository[Task]):
    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)

    """Репозиторий для работы с задачами."""
    async def bulk_create(self, tasks: list[dict]) -> None:
        """Массовое создание задач в базе данных."""
        if not tasks:
            return
        # Используем SQLAlchemy Core для массовой вставки данных
        await self.session.execute(insert(Task), tasks)

    async def get_all(
        self,
        from_date: date | None = None,
        to_date: date | None = None
        ) -> list[Task]:
        """ """
        query = select(Task).options(joinedload(Task.template))

        if from_date:
            query = query.where(Task.target_date >= from_date)
        if to_date:
            query = query.where(Task.target_date <= to_date)

        query = query.order_by(Task.target_date.asc(), Task.created_at.asc())

        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_by_id(
        self,
        task_id: int,
        update_data: dict
    ) -> Task | None:
        # Формируем запрос UPDATE
        stmt = (
            update(self.model)
            .where(self.model.id == task_id)
            .values(**update_data)
            .returning(self.model) # Просим БД вернуть обновленный объект
        )

        # Выполняем запрос
        result = await self.session.execute(stmt)

        # Возвращаем первый найденный объект или None
        return result.scalar_one_or_none()

    async def get_by_id(self, task_id: int) -> Task | None:
        # Получить объект по первичному ключу в SQLAlchemy
        return await self.session.get(self.model, task_id)
