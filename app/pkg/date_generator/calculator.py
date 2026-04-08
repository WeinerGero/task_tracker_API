from datetime import date, timedelta
from dateutil.rrule import rrule, DAILY, MONTHLY
from typing import Literal

from pydantic import BaseModel, Field, RootModel, model_validator
from typing import Union, Annotated

from enums import DateType as RecurrenceType


class DateConfig(BaseModel):
    type: RecurrenceType
    count: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    
    @model_validator(mode='after')
    def check_dates(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValueError("Стартовая дата не может быть позже конечной даты.")
        return self

    
class DailyConfig(DateConfig):
    type: Literal["daily"]
    interval: int = Field(gt=0, default=1)
    
    
class MonthlyConfig(DateConfig):
    type: Literal["monthly"]
    bymonthday: int = Field(gt=0, lt=31, default=1)
    
    
class CustomDatesConfig(DateConfig):
    type: Literal["custom_dates"]
    dates: list[date] = Field(min_items=1)


class EvenOddConfig(MonthlyConfig):
    type: Literal["even"]
    odd: bool = Field(default=False)


RecurrenceConfig = Annotated[
    Union[DailyConfig, MonthlyConfig, CustomDatesConfig, EvenOddConfig], 
    Field(discriminator="type")
]


