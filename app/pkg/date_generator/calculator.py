from datetime import date, datetime, time
from dateutil.rrule import rrule, DAILY, MONTHLY
from typing import Literal

from pydantic import BaseModel, Field, model_validator
from typing import Union, Annotated

from config import EVEN_DAYS, MAX_COUNT, ODD_DAYS
from enums import DateType as RecurrenceType


class DateConfig(BaseModel):
    """Базовая конфигурация для генерации дат.

    Args:
        BaseModel (_type_): Базовый класс для моделей данных в Pydantic.

    Raises:
        ValueError: Если стартовая дата позже конечной даты.

    Returns:
        _type_: Проверенная конфигурация для генерации дат.
    """
    type: RecurrenceType
    count: int | None = Field(le=MAX_COUNT)
    start_date: date | None = Field(default_factory=date.today)
    end_date: date | None = None
    
    @model_validator(mode='after')
    def check_dates(self):
        """Проверяет, что стартовая дата не позже конечной даты.

        Raises:
            ValueError: Если стартовая дата позже конечной даты.

        Returns:
            _type_: Проверенная конфигурация для генерации дат.
        """
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValueError("Стартовая дата не может быть позже конечной даты.")
        return self
    
    
class DailyConfig(DateConfig):
    """Конфигурация для генерации ежедневных дат.
    
    Args:
        DateConfig (_type_): Базовая конфигурация для генерации дат.
    """
    type: Literal["daily"]
    interval: int = Field(gt=0, default=1)
    
    
class MonthlyConfig(DateConfig):
    """Конфигурация для генерации ежемесячных дат.

    Args:
        DateConfig (_type_): Базовая конфигурация для генерации дат.
    """
    type: Literal["monthly"]
    bymonthday: list[Annotated[int, Field(ge=1, le=31)]] = Field(default_factory=lambda: [1])
    
    
class CustomDatesConfig(BaseModel):
    """Конфигурация для генерации пользовательских дат.

    Args:
        BaseModel (_type_): Базовый класс для моделей данных в Pydantic.

    Raises:
        ValueError: Если одна из дат в списке находится в прошлом.

    Returns:
        _type_: Проверенная конфигурация для генерации пользовательских дат.
    """
    type: Literal["custom_dates"]
    dates: list[date] = Field(min_length=1)
    
    @model_validator(mode='after')
    def check_dates(self):
        """Проверяет, что все даты в списке находятся в будущем.

        Raises:
            ValueError: Если одна из дат в списке находится в прошлом.

        Returns:
            _type_: Проверенная конфигурация для генерации пользовательских дат.
        """
        for dt in self.dates:
            if dt < date.today():
                raise ValueError("Все даты должны быть в будущем.")
        return self
    
    
class EvenConfig(DateConfig):
    """Конфигурация для генерации четных дат.

    Args:
        DateConfig (_type_): Базовая конфигурация для генерации дат.
    """
    type: Literal["even"]
    

class OddConfig(DateConfig):
    """Конфигурация для генерации нечетных дат.

    Args:
        DateConfig (_type_): Базовая конфигурация для генерации дат.
    """
    type: Literal["odd"]
    
# Объединенный тип для всех конфигураций генерации дат с дискриминатором по полю "type"
RecurrenceConfig = Annotated[
    Union[DailyConfig, MonthlyConfig, CustomDatesConfig, EvenConfig, OddConfig], 
    Field(discriminator="type")
]


def _get_rrule_dates(config: DateConfig) -> list[date]:
    """Генерирует даты в зависимости от типа конфигурации.

    Args:
        config (DateConfig): Конфигурация для генерации дат.

    Returns:
        list[date]: Список сгенерированных дат.
    """
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
                    bymonthday=config.bymonthday,
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