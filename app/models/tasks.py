"""
Модель данных для задач (Tasks) в системе управления задачами.
"""
# pylint: disable=import-error

from datetime import date
import uuid

from sqlalchemy import ForeignKey, UniqueConstraint, BigInteger
from sqlalchemy.types import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Metadata


class Task(Metadata):
    """
    Модель данных для задач, содержащая информацию о статусе,
    целевой дате и связи с шаблоном задачи.
    Каждая задача может быть связана с шаблоном задачи,
    который определяет правила генерации дат для этой задачи.
    """
    __tablename__ = "tasks"
    # Уникальное ограничение на сочетание template_id и target_date,
    # чтобы избежать создания нескольких задач с одинаковой датой
    # для одного шаблона
    __table_args__ = (
        UniqueConstraint(
            'template_id',
            'target_date',
            name='uq_task_template_date'
        ),
    )

    # Статус задачи, например: "new", "in_progress", "done"
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    # Внешний ключ на шаблон задачи,
    # может быть null для задач без шаблона
    template_id: Mapped[uuid.UUID] = mapped_column(
        BigInteger,
        ForeignKey("task_templates.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    # Целевая дата выполнения задачи,
    # которая может быть сгенерирована на основе шаблона
    target_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )

    # Отношение к шаблону задачи
    template: Mapped["TaskTemplate"] = relationship(
        "TaskTemplate",
        back_populates="tasks"
    )
