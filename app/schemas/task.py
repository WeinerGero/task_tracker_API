"""

"""
from datetime import date, datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .enums import TaskStatus
from app.pkg.date_generator.calculator import RecurrenceConfig


class TaskCreateSchema(BaseModel):
    title: Annotated[str, Field(max_length=255)]
    description: Annotated[str, Field(max_length=1024)] | None = None
    target_date: date | None = None
    recurrence: RecurrenceConfig | None = None

    @model_validator(mode="after")
    def check_date_or_recurrence(self):
        if not self.target_date and not self.recurrence:
            raise ValueError("Необходимо указать либо дату задачи, либо настройки периодичности")
        elif self.target_date and self.recurrence:
            raise ValueError("Необходимо указать только дату задачи или только настройки периодичности")
        return self


class TaskReadSchema(BaseModel):
    id: int
    template_id: int | None
    title: Annotated[str, Field(max_length=255)]
    description: Annotated[str, Field(max_length=1024)] | None = None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    target_date: date

    model_config = ConfigDict(from_attributes=True)
