"""

"""
from typing import TypeVar, Generic

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, model: T) -> T:
        self.session.add(model)
        await self.session.flush()
        return model
