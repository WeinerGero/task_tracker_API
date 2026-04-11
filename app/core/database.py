"""

"""
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=settings.DB_ECHO)

async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=False
)

async def get_db():
    async with async_session_maker() as session:
        yield session
