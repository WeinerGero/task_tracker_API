"""
Модуль инкапсулирует логику вычисления дат для периодических задач.
Содержит классы конфигурации для различных типов повторений
(ежедневные, ежемесячные, пользовательские даты, четные и нечетные даты)
и функцию для генерации дат на основе этих конфигураций.
"""
from datetime import date, datetime, time
from typing import Literal, Union, Annotated

from pydantic import BaseModel, Field, model_validator
from dateutil.rrule import rrule, DAILY, MONTHLY

from .config import EVEN_DAYS, MAX_COUNT, ODD_DAYS
from .enums import DateType as RecurrenceType


class DateConfig(BaseModel):
    """Базовая конфигурация для генерации дат.

    Raises:
        ValueError: Если стартовая дата позже конечной даты.
    """
    type: RecurrenceType
    count: int | None = Field(default=None, le=MAX_COUNT)
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
    """Конфигурация для генерации ежедневных дат"""
    type: Literal["daily"] = "daily"
    interval: int = Field(gt=0, default=1)


class MonthlyConfig(DateConfig):
    """Конфигурация для генерации ежемесячных дат"""
    type: Literal["monthly"] = "monthly"
    bymonthday: list[Annotated[int, Field(ge=1, le=31)]] = Field(default_factory=lambda: [1])


class CustomDatesConfig(BaseModel):
    """Конфигурация для генерации пользовательских дат.

    Raises:
        ValueError: Если одна из дат в списке находится в прошлом.

    """
    type: Literal["custom_dates"] = "custom_dates"
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
    """Конфигурация для генерации четных дат"""
    type: Literal["even"] = "even"


class OddConfig(DateConfig):
    """Конфигурация для генерации нечетных дат"""
    type: Literal["odd"] = "odd"

# Объединенный тип для всех конфигураций генерации дат с дискриминатором по полю "type"
RecurrenceConfig = Annotated[
    Union[DailyConfig, MonthlyConfig, CustomDatesConfig, EvenConfig, OddConfig],
    Field(discriminator="type")
]


def _get_rrule_dates(config: RecurrenceConfig) -> list[date]:
    """Генерирует даты в зависимости от типа конфигурации.

    Returns:
        list[date]: Список сгенерированных дат.
    """
    # Генерируем даты в зависимости от типа конфигурации
    match config:
        # Генерация ежедневных дат
        case DailyConfig():
            # Параметры для rrule:
            # частота - DAILY,
            # начальная дата - start_date,
            # интервал - interval
            kwargs = {
                "freq": DAILY,
                "dtstart": datetime.combine(config.start_date, time.min),
                "interval": config.interval
            }

            # Если указано конечное число, используем его,
            # иначе - None для бесконечной генерации
            if config.end_date:
                kwargs["until"] = datetime.combine(config.end_date, time.max)
            else:
                kwargs["count"] = config.count or MAX_COUNT

            # Генерируем даты с помощью rrule
            rule = rrule(**kwargs)

        # Генерация ежемесячных дат
        case MonthlyConfig():
            # Если указаны дни месяца, фильтруем их,
            # чтобы исключить некорректные значения (29-31),
            # так как не все месяцы имеют эти дни
            bymonthday = []
            for day in config.bymonthday:
                if day in range(29, 32):
                    bymonthday.append(-1)
                    break
                bymonthday.append(day)

            # Параметры для rrule:
            # частота - MONTHLY,
            # начальная дата - start_date,
            # дни месяца - bymonthday
            kwargs = {
                "freq": MONTHLY,
                "dtstart": datetime.combine(config.start_date, time.min),
                "bymonthday": bymonthday
            }

            # Если указано конечное число, используем его,
            # иначе - None для бесконечной генерации
            if config.end_date:
                kwargs["until"] = datetime.combine(config.end_date, time.max)
            else:
                kwargs["count"] = config.count or MAX_COUNT

            # Генерируем даты с помощью rrule
            rule = rrule(**kwargs)

        # Генерация пользовательских дат
        case CustomDatesConfig():
            return config.dates

        # Генерация четных дат
        case EvenConfig():
            # Параметры для rrule:
            # частота - DAILY,
            # начальная дата - start_date,
            kwargs = {
                "freq": DAILY,
                "dtstart": datetime.combine(config.start_date, time.min)
            }

            # Если указано конечное число, используем его,
            # иначе - None для бесконечной генерации
            if config.end_date:
                kwargs["until"] = datetime.combine(config.end_date, time.max)
            else:
                kwargs["count"] = config.count or MAX_COUNT

            # Генерируем даты с помощью rrule, фильтруя по четным дням месяца
            rule = rrule(**kwargs, bymonthday=EVEN_DAYS)

        # Генерация нечетных дат
        case OddConfig():
            # Параметры для rrule:
            # частота - DAILY,
            # начальная дата - start_date
            kwargs = {
                "freq": DAILY,
                "dtstart": datetime.combine(config.start_date, time.min)
            }

            # Если указано конечное число, используем его,
            # иначе - None для бесконечной генерации
            if config.end_date:
                kwargs["until"] = datetime.combine(config.end_date, time.max)
            else:
                kwargs["count"] = config.count or MAX_COUNT

            # Генерируем даты с помощью rrule, фильтруя по нечетным дням месяца
            rule = rrule(**kwargs, bymonthday=ODD_DAYS)

        # Если тип конфигурации неизвестен, выбрасываем исключение
        case _:
            raise ValueError("Unknown config type")

    return [dt.date() for dt in rule]
