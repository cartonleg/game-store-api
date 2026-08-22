from typing import Generic, TypeVar

from sqlalchemy import func
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession


ModelT = TypeVar("ModelT", bound=SQLModel)


class BaseRepository(Generic[ModelT]):
    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, entity_id: int) -> ModelT | None:
        return await self.session.get(self.model, entity_id)

    async def count(self) -> int:
        return await self.session.scalar(
            select(func.count()).select_from(self.model)
        ) or 0

    def add(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        return entity
