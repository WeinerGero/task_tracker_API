"""
Репозиторий для работы с задачами.
Содержит методы для создания, получения и обновления задач.
"""
# pylint: disable=import-error

from sqlalchemy import insert

from app.repositories.base import BaseRepository
from app.models.tasks import Task


class TaskRepository(BaseRepository[Task]):
    """Репозиторий для работы с задачами."""
    async def bulk_create(self, tasks: list[dict]) -> None:
        """Массовое создание задач в базе данных."""
        if not tasks:
            return
        # Используем SQLAlchemy Core для массовой вставки данных
        await self.session.execute(insert(Task), tasks)
