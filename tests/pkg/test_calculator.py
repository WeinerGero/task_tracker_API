"""
Тесты для функции генерации дат на основе различных конфигураций.
"""
from datetime import date
import pytest
from freezegun import freeze_time

from app.pkg.date_generator.calculator import (
    DailyConfig, MonthlyConfig, CustomDatesConfig, EvenConfig, OddConfig,
     _get_rrule_dates
)


# Тесты для генерации дат на основе различных конфигураций
@freeze_time("2025-12-01")
@pytest.mark.parametrize(
    "config_class, params, expected_dates",
    [
        ( # Генерация ежедневных дат с интервалом 1 день и количеством 3
            DailyConfig,
            {
                "type": "daily",
                "start_date": date(2026, 1, 1),
                "interval": 1,
                "count": 3
            },
            [
                date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 3)
            ]
        ),
        ( # Генерация ежедневных дат с интервалом 2 дня и конечной датой
            DailyConfig,
            {
                "type": "daily",
                "start_date": date(2026, 1, 1),
                "interval": 2,
                "end_date": date(2026, 1, 3)
             },
            [
                date(2026, 1, 1), date(2026, 1, 3)
            ]
        ),

        ################################################################
        ( # Генерация месячных дат
            MonthlyConfig,
            {
                "type": "monthly",
                "start_date": date(2026, 1, 1),
                "bymonthday": [1, 15],
                "count": 4
            },
            [
                date(2026, 1, 1), date(2026, 1, 15), date(2026, 2, 1),
                date(2026, 2, 15)
            ]
        ),

        ################################################################
        ( # Генерация пользовательских дат
            CustomDatesConfig,
            {
                "type": "custom_dates",
                "dates": [date(2026, 1, 1), date(2026, 1, 15)]
            },
            [
                date(2026, 1, 1), date(2026, 1, 15)
            ]
        ),

        ################################################################
        ( # Генерация четных дат
            EvenConfig,
            {
                "type": "even",
                "start_date": date(2026, 1, 1),
                "end_date": date(2026, 1, 10)
            },
            [
                date(2026, 1, 2), date(2026, 1, 4), date(2026, 1, 6),
                date(2026, 1, 8), date(2026, 1, 10)
            ]
        ),

        ################################################################
        ( # Генерация нечетных дат
            OddConfig,
            {
                "type": "odd",
                "start_date": date(2026, 1, 1),
                "end_date": date(2026, 1, 10)
            },
            [
                date(2026, 1, 1), date(2026, 1, 3), date(2026, 1, 5),
                date(2026, 1, 7), date(2026, 1, 9)
            ]
        )
    ]
)
def test_successful_date_generation(config_class, params, expected_dates):
    """Тестирует успешную генерацию дат на основе различных конфигураций."""
    # Создаем конфигурацию для генерации дат
    config = config_class(**params)

    # Генерируем даты на основе конфигурации
    result = _get_rrule_dates(config)

    # Проверяем, что сгенерированные даты совпадают с ожидаемыми
    assert result == expected_dates
    assert len(result) == len(expected_dates)

def test_validation_fails_if_start_greater_than_end():
    """
    Тестирует, что валидация конфигурации не проходит,
    если начальная дата больше конечной.
    """
    with pytest.raises(ValueError, match="не может быть позже"):
        DailyConfig(
            start_date=date(2026, 5, 10),
            end_date=date(2026, 5, 1),
            interval=1
        )
        MonthlyConfig(
            start_date=date(2026, 5, 10),
            end_date=date(2026, 5, 1),
            bymonthday=[10]
        )
        EvenConfig(
            start_date=date(2026, 5, 10),
            end_date=date(2026, 5, 1)
        )
        CustomDatesConfig(
            dates=[date(2026, 5, 10), date(2026, 5, 1)]
        )
