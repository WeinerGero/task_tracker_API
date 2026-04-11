"""
Модуль, содержащий базовый класс для моделей SQLAlchemy.
"""
# pylint: disable=not-callable

from datetime import datetime
import uuid

from sqlalchemy import func, BigInteger
from sqlalchemy.types import String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy,
    содержащий общие поля и конфигурацию.
    """
    # Уникальный идентификатор для каждой записи, генерируемый автоматически
    id: Mapped[uuid.UUID] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
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
    """
    Базовый класс для моделей, содержащих метаданные задач,
    таких как шаблоны и задачи.

    __abstract__ = True означает, что этот класс не будет создавать свою
    собственную таблицу в базе данных, а будет использоваться только для
    наследования общих полей и конфигурации.
    """
    __abstract__ = True
    # Название задачи
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    # Описание задачи, может быть null для задач без описания
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
