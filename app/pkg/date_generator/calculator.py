from datetime import date
from enums import DateType as RecurrenceType


def _get_daily_dates(start_date: date, config: dict) -> list[date]:
    next_dates = []
    date_count = config.get("count", 0)
    interval = config.get("interval", 1)
    
    
    # Implement logic to generate daily dates based on start_date and config
    pass

def _get_monthly_dates(start_date: date, config: dict) -> list[date]:
    # Implement logic to generate monthly dates based on start_date and config
    pass

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
    start_date = date(2024, 1, 1)
    config = {"count": 5,
              "interval": 1
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