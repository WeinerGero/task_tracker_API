from datetime import date, timedelta
from dateutil.rrule import rrule, DAILY, MONTHLY
from typing import Literal

from pydantic import BaseModel, Field, RootModel, model_validator
from typing import Union, Annotated

from enums import DateType as RecurrenceType


class DateConfig(BaseModel):
    type: RecurrenceType
    count: int | None = Field(gt=0, default=100)
    start_date: date | None = Field(default_factory=date.today)
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
    bymonthday: list[int] = list[Annotated[int, Field(ge=1, le=31)]]
    
    
class CustomDatesConfig(BaseModel):
    type: Literal["custom_dates"]
    dates: list[date] = Field(min_length=1)
    
    @model_validator(mode='after')
    def check_dates(self):
        for date in self.dates:
            if date < date.today():
                raise ValueError("Все даты должны быть в будущем.")
        return self
    
    
class EvenConfig(DateConfig):
    type: Literal["even"]
    

class OddConfig(DateConfig):
    type: Literal["odd"]
    

RecurrenceConfig = Annotated[
    Union[DailyConfig, MonthlyConfig, CustomDatesConfig, EvenConfig, OddConfig], 
    Field(discriminator="type")
]


