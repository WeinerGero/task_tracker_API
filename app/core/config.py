"""

"""
from pydantic import BaseModel

class Settings(BaseModel):
    DATABASE_URL: str
    DB_ECHO: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
