"""
Репозиторий для работы с задачами.
Содержит методы для создания, получения и обновления задач.
"""
# pylint: disable=import-error

from sqlalchemy import insert
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
