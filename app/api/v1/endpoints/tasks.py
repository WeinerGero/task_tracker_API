"""

"""
from uuid import UUID
from datetime import date

from fastapi import APIRouter, status, Depends, Query

from app.services.task_service import TaskService
from app.schemas.task import TaskCreateSchema, TaskReadSchema
from app.api.dependencies import get_task_service


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreateSchema,
    service: TaskService = Depends(get_task_service)
):
    if payload.recurrence:
        # Передаем config=payload.recurrence
        return await service.create_recurring_task(
            title=payload.title,
            description=payload.description,
            config=payload.recurrence
        )

    return await service.create_simple_task(
        title=payload.title,
        description=payload.description,
        target_date=payload.target_date
    )

@router.get("/", response_model=list[TaskReadSchema])
async def get_tasks(
    from_date: date | None = Query(None, description="Начало периода"),
    to_date: date | None = Query(None, description="Конец периода"),
    service: TaskService = Depends(get_task_service)
    ):

    return await service.get_tasks(from_date=from_date, to_date=to_date)

@router.delete(
    "/templates/{template_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_task_template(
    template_id: UUID,
    service: TaskService = Depends(get_task_service)
):
    """Удаляет шаблон и все связанные задачи (каскадно)."""
    await service.delete_template(template_id)
