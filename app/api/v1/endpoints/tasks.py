"""

"""
from fastapi import APIRouter, Depends, status

from app.services.task_service import TaskService
from app.schemas.task import TaskCreateSchema
from app.api.dependencies import get_task_service


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreateSchema,
    service: TaskService = Depends(get_task_service)
    ):
    if payload.recurrence:
        # Передаем всё: и метаданные задачи, и конфиг периодичности
        return await service.create_recurring_task(
            title=payload.title,
            description=payload.description,
            config=payload.recurrence
        )
    else:
        # Передаем только то, что нужно для одиночной задачи
        return await service.create_simple_task(
            title=payload.title,
            description=payload.description,
            target_date=payload.target_date
        )

