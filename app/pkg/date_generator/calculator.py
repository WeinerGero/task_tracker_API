from datetime import date, timedelta
from enums import DateType as RecurrenceType


def _get_daily_dates(start_date: date, config: dict) -> list[date]:
    """
    Генерирует следующие даты на основе ежедневного правила.
    
    Args:
        start_date (date): Дата, с которой начинается генерация.
        config (dict): Конфигурация, содержащая необходимые параметры для генерации дат (например, количество дат, интервалы и т.д.).

    Returns:
        list[date]: Список сгенерированных дат.
    """
    date_count = config.get("count", 1)
    interval = config.get("interval", 1)
    return [start_date + timedelta(days=i * interval) for i in range(date_count)]

def _get_monthly_dates(start_date: date, config: dict) -> list[date]:
    """
    Генерирует следующие даты на основе ежемесячного правила.
    
    Args:
        start_date (date): Дата, с которой начинается генерация.
        config (dict): Конфигурация, содержащая необходимые параметры для генерации дат (например, количество дат, интервалы и т.д.).

    Returns:
        list[date]: Список сгенерированных дат.
    """
    date_count = config.get("count", 1)
    month_days = {
        1: 31,
        2: 29,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }
    if year := start_date.year:
        month_days[2] = 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28
    
    return [
        date(start_date.year + (start_date.month + i) // 12, (start_date.month + i) % 12 or 12, min(start_date.day, month_days[(start_date.month + i) % 12 or 12]))
        for i in range(date_count)
    ]

def _get_custom_dates(config: dict) -> list[date]:
    # Implement logic to return custom dates based on config
    pass

def _get_even_dates(config: dict) -> list[date]:
    # Implement logic to return even dates based on config
    pass

def _get_odd_dates(config: dict) -> list[date]:
    # Implement logic to return odd dates based on config
    pass


def get_next_dates(start_date: date, rule_type: RecurrenceType, config: dict) -> list[date]:
    """
    Считывает следующие даты на основе типа правила и конфигурации.
    
    Args:
        start_date (date): Дата, с которой начинается генерация.
        rule_type (RecurrenceType): Тип правила (ежедневное, ежемесячное, пользовательские даты).
        config (dict): Конфигурация, содержащая необходимые параметры для генерации дат (например, количество дат, интервалы и т.д.).

    Raises:
        ValueError: Если тип правила не поддерживается.

    Returns:
        list[date]: Список сгенерированных дат.
    """
    if rule_type == RecurrenceType.DAILY:
        return _get_daily_dates(start_date, config)
    elif rule_type == RecurrenceType.MONTHLY:
        return _get_monthly_dates(start_date, config)
    elif rule_type == RecurrenceType.CUSTOM_DATES:
        return _get_custom_dates(config)
    elif rule_type == RecurrenceType.EVEN:
        return _get_even_dates(config)
        pass
    elif rule_type == RecurrenceType.ODD:
        return _get_odd_dates(config)
        pass
    else:
        raise ValueError(f"Unsupported rule type: {rule_type}")


if __name__ == "__main__":
    # Example usage
    start_date = date(2024, 1, 31)
    config = {"count": 5,
              "interval": 2,
              "custom_dates": [date(2024, 1, 10), date(2024, 1, 20)],
              }  # Example configuration
    print(get_next_dates(start_date, RecurrenceType.DAILY, config))
    print("_" * 20)
    print(get_next_dates(start_date, RecurrenceType.MONTHLY, config))
    print("_" * 20)
    print(get_next_dates(start_date, RecurrenceType.CUSTOM_DATES, config))
    print("_" * 20)
    print(get_next_dates(start_date, RecurrenceType.EVEN, config))
    print("_" * 20)
    print(get_next_dates(start_date, RecurrenceType.ODD, config))