from datetime import date, datetime, time
from logging import config
from dateutil.rrule import rrule, DAILY, MONTHLY
from typing import Literal

from pydantic import BaseModel, Field, RootModel, model_validator
from typing import Union, Annotated

from config import EVEN_DAYS, MAX_COUNT, ODD_DAYS
from enums import DateType as RecurrenceType


class DateConfig(BaseModel):
    type: RecurrenceType
    count: int | None = Field(le=MAX_COUNT)
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


def _get_rrule_dates(config: DateConfig) -> list[date]:    
    # Генерируем даты в зависимости от типа конфигурации
    match config:
        # Генерация ежедневных дат
        case DailyConfig():
            rule = rrule(
                    freq=DAILY,
                    dtstart=datetime.combine(config.start_date, time.min),
                    interval=config.interval,
                    # Если указано конечное число, используем его, иначе - None для бесконечной генерации
                    until=datetime.combine(config.end_date, time.max) 
                    if config.end_date else None,
                    count=config.count or MAX_COUNT
                )
            
        # Генерация ежемесячных дат
        case MonthlyConfig():
            rule = rrule(
                    freq=MONTHLY,
                    dtstart=datetime.combine(config.start_date, time.min),
                    # Если указано число месяца, используем его, иначе -1 для последнего дня месяца
                    bymonthday=config.bymonthday 
                    if config.bymonthday not in [29, 30, 31] else [-1],
                    # Если указано конечное число, используем его, иначе - None для бесконечной генерации
                    until=datetime.combine(config.end_date, time.max)
                    if config.end_date else None,
                    count=config.count or MAX_COUNT
                )
            
        # Генерация пользовательских дат
        case CustomDatesConfig():
            return config.dates 
              
        # Генерация четных дат
        case EvenConfig():
            rule = rrule(
                    freq=DAILY,
                    dtstart=datetime.combine(config.start_date, time.min),
                    # Если указано конечное число, используем его, иначе - None для бесконечной генерации
                    until=datetime.combine(config.end_date, time.max)
                    if config.end_date else None,
                    bymonthday=EVEN_DAYS,
                    count=config.count or MAX_COUNT
                )
            
        # Генерация нечетных дат
        case OddConfig():
            rule = rrule(
                    freq=DAILY,
                    dtstart=datetime.combine(config.start_date, time.min),
                    # Если указано конечное число, используем его, иначе - None для бесконечной генерации
                    until=datetime.combine(config.end_date, time.max)
                    if config.end_date else None,
                    bymonthday=ODD_DAYS,
                    count=config.count or MAX_COUNT
                )
            
        # Если тип конфигурации неизвестен, выбрасываем исключение
        case _:
            raise ValueError("Unknown config type")
            
    return [dt.date() for dt in rule]


