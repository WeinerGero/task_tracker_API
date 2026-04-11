"""
Этот модуль содержит репозиторий для работы с шаблонами задач.
Репозиторий предоставляет методы для создания, получения,
обновления и удаления шаблонов задач в базе данных.
Он наследуется от базового репозитория, который обеспечивает
общие операции для всех моделей.
"""
# pylint: disable=import-error
from uuid import UUID

from sqlalchemy import delete

from app.models.templates import TaskTemplate
from app.repositories.base import BaseRepository


class TemplateRepository(BaseRepository[TaskTemplate]):
    """Репозиторий для работы с шаблонами задач."""
    def __init__(self, session):
        super().__init__(TaskTemplate, session)

    async def delete_by_id(self, entity_id: UUID) -> bool:
        stmt = delete(self.model).where(self.model.id == entity_id)
        result = await self.session.execute(stmt)
        return result.rowcount > 0
