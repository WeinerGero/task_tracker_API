"""

"""
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.task_repo import TaskRepository
from app.services.task_service import TaskService
from app.repositories.task_repo import TaskRepository
from app.repositories.template_repo import TemplateRepository
from app.core.database import get_db


async def get_task_service(session: AsyncSession = Depends(get_db)):
    return TaskService(
        task_repository=TaskRepository(session),
        template_repository=TemplateRepository(session)
    )
