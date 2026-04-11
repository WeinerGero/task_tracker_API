"""
Тесты для репозиториев.
Здесь мы будем проверять, что наши методы взаимодействия с базой данных
работают корректно. Например, мы можем проверить, что при добавлении новой
задачи она действительно сохраняется в базе, или что при удалении
задачи она больше не доступна.
"""
import pytest
from datetime import date

from sqlalchemy import select, insert

from app.models.templates import TaskTemplate
from app.models.tasks import Task
from app.repositories.task_repo import TaskRepository
from app.repositories.template_repo import TemplateRepository


@pytest.mark.asyncio
async def test_template_repository(db_session):
    repo = TemplateRepository(db_session)
    template = TaskTemplate(
        title = "Daily Task Template",
        description = "Template for daily tasks",
        rule_type = "daily",
        rule_config = {
            "start_date": "2026-04-12",
            "end_date": "2026-05-12",
            "interval": 4
        }
    )
    await repo.create(template)
    assert template.id is not None


@pytest.mark.asyncio
async def test_bulk_create_tasks(db_session):
    template_repo = TemplateRepository(db_session)
    template = TaskTemplate(title="Test", rule_type="daily", rule_config={})
    await template_repo.create(template)

    task_repo = TaskRepository(db_session)
    tasks_data =[
    {
        "template_id": template.id,
        "title": "Task 1",
        "description": "Description 1",
        "status": "new",
        "target_date": date(2026, 4, 12)
    },
    {
        "template_id": template.id,
        "title": "Task 2",
        "description": "Description 2",
        "status": "new",
        "target_date": date(2026, 4, 13)
    }
    ]
    await task_repo.bulk_create(tasks_data)

    # Проверяем, что задачи были добавлены в базу данных
    result = await db_session.execute(select(Task.title, Task.description))
    tasks_in_db = result.fetchall()
    assert len(tasks_in_db) == 2
    assert ("Task 1", "Description 1") in tasks_in_db
    assert ("Task 2", "Description 2") in tasks_in_db

@pytest.mark.asyncio
async def test_bulk_create_empty_list_does_not_crash(db_session):
    repo = TaskRepository(db_session)
    # Если условие if not tasks не работает, SQLAlchemy выбросит ошибку
    await repo.bulk_create(
        []
    )
    # Проверяем, что в базе данных нет новых задач
    result = await db_session.execute(select(Task))
    tasks_in_db = result.fetchall()
    assert len(tasks_in_db) == 0

@pytest.mark.asyncio
async def test_get_all_filtering(db_session):
    repo = TaskRepository(db_session)
    # Arrange: создаем задачи на разные даты
    dates = [date(2025, 1, 1), date(2025, 1, 2), date(2025, 1, 3)]
    for d in dates:
        await repo.session.execute(insert(Task).values(
            title=f"Task {d}",
            target_date=d,
            status="new"
        ))

    # Act: фильтруем только за 2-е число
    tasks = await repo.get_all(from_date=date(2025, 1, 2), to_date=date(2025, 1, 2))

    # Assert
    assert len(tasks) == 1
    assert tasks[0].target_date == date(2025, 1, 2)
