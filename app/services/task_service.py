"""
Сервис для управления задачами, включая создание
повторяющихся задач на основе шаблонов.
"""
# pylint: disable=import-error
from uuid import UUID
from datetime import date

from app.services.exceptions import ServiceError
from app.models.templates import TaskTemplate
from app.models.tasks import Task
from app.schemas.enums import TaskStatus
from app.pkg.date_generator.calculator import RecurrenceConfig, calculate_dates


class TaskService:
    """
    Сервис для управления задачами,
    включая создание повторяющихся задач на основе шаблонов.
    """
    def __init__(self, task_repository, template_repository):
        self.task_repository = task_repository
        self.template_repository = template_repository

    async def create_recurring_task(
            self,
            title: str,
            description: str | None,
            config: RecurrenceConfig
        ):
        """Создает повторяющиеся задачи на основе шаблона и конфигурации."""
        # Преобразуем конфигурацию в формат,
        # который можно сохранить в базе данных
        rule_config = config.model_dump(mode='json')

        # Генерируем даты для задач на основе конфигурации
        dates = calculate_dates(config)


        # Если генерация дат не удалась, выбрасываем исключение
        if not dates:
            raise ServiceError("Генерация дат не удалась. Проверьте конфигурацию шаблона.")

        # Сохраняем шаблон задачи и связанные задачи в базе данных
        async with self.task_repository.session.begin():
            # Сохраняем шаблон задачи в базе данных
            template = await self.template_repository.create(TaskTemplate(
            title=title,
            description=description,
            rule_type=config.type,
            rule_config=rule_config
            ))

            # Создаем задачи для каждой сгенерированной даты
            tasks = [
                {
                    "title": title,
                    "description": description,
                    "status": "new",
                    "template_id": template.id,
                    "target_date": dt
                } for dt in dates
            ]

            # Сохраняем задачи в базе данных
            await self.task_repository.bulk_create(tasks)

        return template

    async def create_simple_task(
            self,
            title: str,
            description: str | None,
            target_date: date | None
        ):
        """Создает простую задачу без повторения."""
        task_obj = Task(
            title=title,
            description=description,
            status=TaskStatus.NEW,
            target_date=target_date or date.today()
        )

        return await self.task_repository.create(task_obj)


    async def get_tasks(
        self,
        from_date: date | None = None,
        to_date: date | None = None
        ) -> list[Task]:
        # ограничение диапазона (защита от DoS)
        if from_date and to_date:
            delta = to_date - from_date
            if delta.days > 366:
                raise ServiceError("Нельзя запрашивать задачи более чем за один год")

        # Вызов репозитория
        return await self.task_repository.get_all(
            from_date=from_date,
            to_date=to_date
        )

    async def delete_template(self, template_id: UUID) -> None:
        async with self.template_repository.session.begin():
            deleted = await self.template_repository.delete_by_id(template_id)
            if not deleted:
                raise ServiceError(f"Шаблон с ID {template_id} не найден")
