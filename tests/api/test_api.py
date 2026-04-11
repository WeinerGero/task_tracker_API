import pytest
from datetime import date, timedelta

from app.models.tasks import Task
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
