"""
Модуль, содержащий базовый класс для моделей SQLAlchemy.
"""
import uuid
from datetime import datetime

from sqlalchemy import UUID, DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        index=True,
        default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )