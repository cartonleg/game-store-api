from collections.abc import Sequence

from sqlalchemy import func
from sqlmodel import select

from app.database.models import Game, Locations, Order
from app.database.repositories.base import BaseRepository


class GameRepository(BaseRepository[Game]):
    model = Game

    async def list_page(
        self, *, page: int, size: int, location: Locations | None = None
    ) -> tuple[Sequence[Game], int]:
        filters = []
        if location is not None:
            filters.append(Game.location == location)

        total = await self.session.scalar(
            select(func.count()).select_from(Game).where(*filters)
        ) or 0

        statement = (
            select(Game)
            .where(*filters)
            .order_by(Game.id)
            .offset((page - 1) * size)
            .limit(size)
        )
        items = (await self.session.exec(statement)).all()
        return items, total

    def add_multiple(self, entities: Sequence[Game]) -> Sequence[Game]:
        self.session.add_all(entities)
        return entities

    async def list_purchased_games_for_user(self, user_id: int) -> Sequence[Game]:
        statement = (
            select(Game)
            .join(Order, Order.game_id == Game.id)
            .where(Order.user_id == user_id)
        )
        return (await self.session.exec(statement)).all()
