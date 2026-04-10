"""
Модуль, содержащий модели данных для шаблонов задач.
"""
# pylint: disable=import-error

from sqlalchemy.types import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Metadata


class TaskTemplate(Metadata):
    """
    Модель данных для шаблонов задач, содержащая информацию
    о типе правила генерации дат и конфигурации для генерации дат.
    Каждая задача может быть связана с шаблоном задачи,
    который определяет правила генерации дат для этой задачи.
    """
    __tablename__ = "task_templates"

    # Тип правила генерации дат, например:
    # "daily", "monthly", "custom_dates", "even", "odd"
    rule_type: Mapped[str] = mapped_column(String(20), nullable=False)

    # Конфигурация для генерации дат, хранящаяся в формате JSON
    rule_config: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Отношение к задачам, которые были сгенерированы на основе этого шаблона
    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="template",
        passive_deletes=True
    )
