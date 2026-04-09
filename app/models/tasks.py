"""
Модель данных для задач (Tasks) в системе управления задачами.
"""
from datetime import date, datetime
import uuid

from sqlalchemy import (
    ForeignKey,
    String,
    DateTime,
    Date,
    UniqueConstraint,
    func
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.templates import TaskTemplate

from .base import Base


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        UniqueConstraint(
            'template_id',
            'target_date',
            name='uq_task_template_date'
        )
    )

    # Статус задачи, например: "new", "in_progress", "done"
    status: Mapped[str] = mapped_column(String(20), nullable=False)

    # Дата и время последнего обновления задачи
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True
    )

    # Внешний ключ на шаблон задачи,
    # может быть null для задач без шаблона
    template_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("task_templates.id"),
        nullable=True,
        index=True,
    )
    # Целевая дата выполнения задачи,
    # которая может быть сгенерирована на основе шаблона
    target_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
    )
    # Отношение к шаблону задачи
    template: Mapped["TaskTemplate"] = relationship(back_populates="tasks")

