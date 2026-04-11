"""

"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4
from datetime import date


@patch("app.services.task_service.calculate_dates")
@pytest.mark.asyncio
async def test_create_recurring_task_logic(mock_calculate):
    # Настраиваем калькулятор
    mock_calculate.return_value = [date(2025, 1, 1), date(2025, 1, 2)]

    # Настройка транзакции (async with session.begin())
    mock_session = MagicMock()
    # Создаем AsyncMock для самого контекстного менеджера.
    cms = AsyncMock()
    # Настраиваем: вызов .begin() возвращает наш контекстный менеджер
    mock_session.begin.return_value = cms

    # Мокаем репозитории
    template_repo = AsyncMock()
    task_repo = AsyncMock()
    # оба репозитория на одной и той же сессии
    template_repo.session = mock_session
    task_repo.session = mock_session

    # Имитируем создание шаблона и возврат ID
    fake_template_id = uuid4()
    template_repo.create.return_value = MagicMock(id=fake_template_id)

    # Инициализируем сервис
    from app.services.task_service import TaskService
    service = TaskService(task_repo, template_repo)

    # Подготовим mock_config (просто объект с нужными атрибутами)
    mock_config = MagicMock()
    mock_config.type = "daily"
    mock_config.rule_config.model_dump.return_value = {"some": "config"}

    await service.create_recurring_task(
        title="Test Title",
        description="Test Desc",
        config=mock_config
    )

    # ПРОВЕРКИ
    # А. Проверяем, что шаблон создался один раз
    template_repo.create.assert_called_once()

    # Б. Проверяем, что задачи ушли в bulk_create
    task_repo.bulk_create.assert_called_once()

    # В. Проверяем, что в задачах ПРАВИЛЬНЫЙ template_id
    args, _ = task_repo.bulk_create.call_args
    tasks_to_insert = args[0]
    assert len(tasks_to_insert) == 2
    for t in tasks_to_insert:
        assert t["template_id"] == fake_template_id
        assert t["title"] == "Test Title"
