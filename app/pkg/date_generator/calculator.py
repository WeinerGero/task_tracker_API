from datetime import date, timedelta
from enums import DateType as RecurrenceType


def _check_date_validity(start_date: date, end_date: date) -> None:
    """
    Проверяет валидность начальной и конечной дат.
    
    Args:
        start_date (date): Начальная дата.
        end_date (date): Конечная дата.

    Raises:
        ValueError: Если начальная дата больше конечной даты.
    """
    if start_date > end_date:
        raise ValueError("Начальная дата должна быть меньше или равна конечной дате.")
    if (end_date - start_date).days > 365 * 2:
        raise ValueError("Разница между начальной и конечной датой не должна превышать 5 лет.")
    
def _get_daily_dates(start_date: date, config: dict) -> list[date]:
    """
    Генерирует следующие даты на основе ежедневного правила.
    
    Args:
        start_date (date): Дата, с которой начинается генерация.
        config (dict): Конфигурация, содержащая необходимые параметры для генерации дат (например, количество дат, интервалы и т.д.).

    Raises:
        ValueError: Если дата окончания меньше начальной даты.
    
    Returns:
        list[date]: Список сгенерированных дат.
    """
    date_count = config.get("count", 1)
    interval = config.get("interval", 1)

    if config.get("end_date"):
        days_left = (config["end_date"] - start_date).days + 1
        date_count = (days_left + interval - 1) // interval
    
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
    
    if config.get("end_date"):
        days_left = (config["end_date"] - start_date).days + 1
        date_count = (days_left + 29) // 30
    
    return [
        date(
            start_date.year + (start_date.month + i) // 12,
            (start_date.month + i) % 12 or 12,
            min(start_date.day, month_days[(start_date.month + i) % 12 or 12])
            )
        for i in range(date_count)
    ]

def _get_custom_dates(start_date: date, config: dict) -> list[date]:
    """
    Генерирует следующие даты на основе пользовательских дат, указанных в конфигурации.
    
    Args:
        start_date (date): Дата, с которой начинается генерация.
        config (dict): Конфигурация, содержащая необходимые параметры для генерации дат (например, список пользовательских дат).

    Raises:
        ValueError: Если пользовательские даты меньше начальной даты.

    Returns:
        list[date]: Список сгенерированных дат.
    """
    for date in config["custom_dates"]:
        if date < start_date:
            raise ValueError("Кастомные даты должны быть больше или равны начальной дате.")

    return config["custom_dates"]
    
def _get_even_dates(start_date: date, config: dict) -> list[date]:
    """
    Генерирует следующие даты на основе правила четных дней.
    
    Args:
        start_date (date): Дата, с которой начинается генерация.
        config (dict): Конфигурация, содержащая необходимые параметры для генерации дат (например, количество дат).

    Returns:
        list[date]: Список сгенерированных дат.
    """
    start_date = start_date if start_date.day % 2 == 0 else start_date + timedelta(days=1)
    date_count = config.get("count", 1)    

    if config.get("end_date"):
        days_left = (config["end_date"] - start_date).days + 1
        date_count = (days_left) // 2

    return [
        start_date + timedelta(days=i * 2) 
        if (start_date + timedelta(days=i * 2)).day % 2 == 0 
        else start_date + timedelta(days=(i * 2) + 1) 
        for i in range(date_count)
    ]
    
def _get_odd_dates(start_date: date, config: dict) -> list[date]:
    """
    Генерирует следующие даты на основе правила нечетных дней.
    
    Args:
        start_date (date): Дата, с которой начинается генерация.
        config (dict): Конфигурация, содержащая необходимые параметры для генерации дат (например, количество дат).

    Returns:
        list[date]: Список сгенерированных дат.
    """
    start_date = start_date if start_date.day % 2 != 0 else start_date + timedelta(days=1)
    date_count = config.get("count", 1)  
    
    if config.get("end_date"):
        days_left = (config["end_date"] - start_date).days + 1
        date_count = (days_left) // 2
    
    return [
        start_date + timedelta(days=i)
        for i in range((1+date_count) * 2)
        if (start_date + timedelta(days=i)).day % 2 != 0
    ][:date_count]


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
    if config.get("end_date"):
        _check_date_validity(start_date, config["end_date"])
    
    if rule_type == RecurrenceType.DAILY:
        return _get_daily_dates(start_date, config)
    elif rule_type == RecurrenceType.MONTHLY:
        return _get_monthly_dates(start_date, config)
    elif rule_type == RecurrenceType.CUSTOM_DATES:
        return _get_custom_dates(start_date, config)
    elif rule_type == RecurrenceType.EVEN:
        return _get_even_dates(start_date,config)
    elif rule_type == RecurrenceType.ODD:
        return _get_odd_dates(start_date, config)
    else:
        raise ValueError(f"Неподдерживаемый тип правила: {rule_type}")


if __name__ == "__main__":
    # Example usage
    start_date = date(2024, 12, 30)
    config = {"count": 5,
              "interval": 5,
              "end_date": date(2025, 1, 15),
              "custom_dates": [date(2025, 1, 10), date(2025, 1, 20)],
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