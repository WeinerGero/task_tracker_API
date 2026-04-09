"""
Модуль, содержащий модели данных для шаблонов задач.
"""
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class TaskTemplate(Base):
    __tablename__ = "task_templates"

    # Тип правила генерации дат, например:
    # "daily", "monthly", "custom_dates", "even", "odd"
    rule_type: Mapped[str] = mapped_column(String(20), nullable=False)

    # Конфигурация для генерации дат, хранящаяся в формате JSON
    rule_config: Mapped[dict] = mapped_column(JSONB, nullable=False)
