from enum import StrEnum


class DateType(StrEnum):
    """
    Enum для типов генерации дат.

    Args:
        StrEnum (_type_): Базовый класс для строковых перечислений.
    """
    DAILY = "daily"
    MONTHLY = "monthly"
    CUSTOM_DATES = "custom_dates"
    EVEN = "even"
    ODD = "odd"