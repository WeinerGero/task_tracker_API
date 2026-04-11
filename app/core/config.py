"""

"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    DB_ECHO: bool = False
    model_config = SettingsConfigDict(
        # Указываем имя файла
        env_file=".env",
        # Указываем кодировку (стандарт для Linux/Docker)
        env_file_encoding="utf-8",
        # Если файла .env нет, Pydantic не упадет, а попробует взять из системных переменных
        extra="ignore"
    )

settings = Settings()
