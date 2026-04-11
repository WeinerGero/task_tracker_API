import pytest
from datetime import date, timedelta

from sqlalchemy import select

from app.models.tasks import Task
from app.services.task_service import TaskTemplate
from app.schemas.enums import TaskStatus


@pytest.mark.asyncio
async def test_create_resource_api(client, db_session):
    payload = {
        "title": "New Item",
        "recurrence": {"type": "daily", "interval": 1}
    }

    response = await client.post("/api/v1/tasks/", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data

@pytest.mark.asyncio
async def test_get_tasks_filtering_by_date(client, db_session):
    # Наполняем базу тестовыми данными
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)

    # Создаем 3 задачи через репозиторий или напрямую
    tasks_to_create = [
        Task(
            title=f"Task for {d}",
            description="Test",
            status=TaskStatus.NEW,
            target_date=d
        ) for d in [yesterday, today, tomorrow]
    ]
    # Массово добавляем в сессию
    db_session.add_all(tasks_to_create)
    # Фиксируем в базе, чтобы другие сессии (API) увидели данные
    await db_session.commit()

    # Запрашиваем задачи только на "сегодня"
    # Передаем параметры в query string: ?from_date=...&to_date=...
    params = {
        "from_date": today.isoformat(),
        "to_date": today.isoformat()
    }
    response = await client.get("/api/v1/tasks/", params=params)

    # Assert
    assert response.status_code == 200
    data = response.json()

    # Проверяем, что фильтр сработал
    assert len(data) == 1
    assert data[0]["target_date"] == today.isoformat()

@pytest.mark.asyncio
async def test_delete_template_success(client, db_session):
    # 1. Arrange: Создаем данные
    template = TaskTemplate(title="To be deleted", rule_type="daily", rule_config={})
    db_session.add(template)
    await db_session.flush() # Получаем ID

    # Добавляем связанные задачи
    task = Task(title="Task", target_date=date.today(), template_id=template.id, status="new")
    db_session.add(task)
    await db_session.commit()

    # 2. Act: Удаляем
    response = await client.delete(f"/api/v1/tasks/templates/{template.id}")

    # 3. Assert
    assert response.status_code == 204

    # Проверяем отсутствие в базе
    res_template = await db_session.get(TaskTemplate, template.id)
    assert res_template is None

    # Проверяем отсутствие задач (каскад)
    res_tasks = await db_session.execute(
        select(Task).where(Task.template_id == template.id)
    )
    assert len(res_tasks.scalars().all()) == 0

@pytest.mark.asyncio
async def test_get_single_task_success(client, db_session):
    # 1. Arrange
    task = Task(
        title="Test Get Task",
        description="Desc",
        status=TaskStatus.NEW,
        target_date=date.today()
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task) # Получаем сгенерированный ID

    # 2. Act
    response = await client.get(f"/api/v1/tasks/{task.id}")

    # 3. Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task.id
    assert data["title"] == "Test Get Task"

@pytest.mark.asyncio
async def test_update_task_success(client, db_session):
    # 1. Arrange
    task = Task(
        title="Old Title",
        description="Old Desc",
        status=TaskStatus.NEW,
        target_date=date.today()
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    await db_session.commit()

    # 2. Act: Обновляем только статус и описание
    payload = {
        "description": "New Desc",
        "status": "done"
    }
    response = await client.put(f"/api/v1/tasks/{task.id}", json=payload)

    # 3. Assert
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "done"
    assert data["description"] == "New Desc"
    assert data["title"] == "Old Title" # Название не должно было измениться

    # Убеждаемся, что в базе данные тоже обновились
    await db_session.refresh(task)
    assert task.status == TaskStatus.DONE

@pytest.mark.asyncio
async def test_delete_single_task_success(client, db_session):
    # 1. Arrange
    task = Task(
        title="Task to delete",
        status=TaskStatus.NEW,
        target_date=date.today()
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    await db_session.commit()

    # 2. Act
    response = await client.delete(f"/api/v1/tasks/{task.id}")

    # 3. Assert
    assert response.status_code == 204 # 204 No Content

    # Проверяем, что задача реально исчезла из БД
    deleted_task = await db_session.get(Task, task.id)
    assert deleted_task is None

@pytest.mark.asyncio
async def test_get_task_not_found(client):
    # Act: Запрашиваем несуществующий ID (например, 999999)
    response = await client.get("/api/v1/tasks/999999")

    # Assert: Ожидаем ошибку от нашего exception_handler
    assert response.status_code == 400 # Или 404, смотря как ты настроил ServiceError
    data = response.json()
    assert "detail" in data # Проверяем, что вернулась структура ошибки



