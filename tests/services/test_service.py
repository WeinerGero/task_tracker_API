"""

"""
from unittest.mock import AsyncMock, patch
from uuid import uuid4
import pytest

from fastapi import status

from app.pkg.date_generator.calculator import RecurrenceConfig
from app.repositories.task_repo import TaskRepository
from app.repositories.template_repo import TemplateRepository
from app.services.task_service import TaskService
from app.models.templates import TaskTemplate
from app.services.exceptions import ServiceError


@pytest.mark.asyncio
async def test_create_recurring_task_success():
    # Создаем моки репозиториев
    task_repo = AsyncMock()
    template_repo = AsyncMock()

    # Настраиваем поведение: создание шаблона возвращает объект с ID
    template_repo.create.return_value = TaskTemplate(id=uuid4())

    service = TaskService(task_repo, template_repo)

    # Вызываем сервис
    await service.create_recurring_task(
        title="Test Task",
        description="Test Description",
        config=RecurrenceConfig(
            type="daily",
            rule_config={
                "start_date": "2026-04-12",
                "end_date": "2026-04-14",
                "interval": 1
            }
        )
    )

    # Проверяем, что данные дошли до репозитория задач в нужном виде
    args, _ = task_repo.bulk_create.call_args
    tasks_list = args[0]
    assert len(tasks_list) == 3
    assert tasks_list[0]["template_id"] == template_repo.create.return_value.id

async def get_task_service(session: AsyncSession = Depends(get_db_session)):
    return TaskService(
        task_repository=TaskRepository(session),
        template_repository=TemplateRepository(session)
    )

@router.post(
    "/tasks",
    status_code=status.HTTP_201_CREATED,
    response_model=TaskTemplate
)
async def create_task(
    payload: TaskCreateSchema,
    service: TaskService = Depends(get_task_service)
    ):
    if payload.config:
        # Логика для периодических задач
        result = await service.create_recurring_task(
            title=payload.title,
            description=payload.description,

        )
    else:
        # Логика для обычной задачи
        result = await service.create_simple_task(
            title=payload.title,
            description=payload.description
        )

    return result

@app.exception_handler(ServiceError)
async def service_error_handler(request: Request, exc: ServiceError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )
