"""
Модуль, содержащий базовый класс для моделей SQLAlchemy.
"""
from datetime import datetime
import uuid

from sqlalchemy import func
from sqlalchemy.types import String, DateTime, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    # Уникальный идентификатор для каждой записи, генерируемый автоматически
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid()
    )
    # Дата и время создания записи
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    # Дата и время последнего обновления задачи
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=False,
        server_default=func.now()
    )


class Metadata(Base):
    __abstract__ = True
    # Название задачи
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    # Описание задачи, может быть null для задач без описания
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
