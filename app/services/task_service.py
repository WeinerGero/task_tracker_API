"""
Сервис для управления задачами, включая создание
повторяющихся задач на основе шаблонов.
"""
from app.services.exceptions import ServiceError
from app.models.templates import TaskTemplate
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
        rule_config = config.rule_config.model_dump(mode='json')

        # Генерируем даты для задач на основе конфигурации
        dates = calculate_dates(
            config.type,
            rule_config
        )

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
