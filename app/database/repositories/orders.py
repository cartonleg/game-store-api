from collections.abc import Sequence

from sqlmodel import select

from app.database.models import Order
from app.database.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    model = Order

    async def list_for_user(self, user_id: int) -> Sequence[Order]:
        statement = (
            select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc())
        )
        return (await self.session.exec(statement)).all()

    async def exists_for_user_and_game(self, user_id: int, game_id: int) -> bool:
        statement = select(Order.id).where(
            Order.user_id == user_id,
            Order.game_id == game_id,
        )
        return (await self.session.scalar(statement)) is not None

    async def get_for_user(self, user_id: int, order_id: int) -> Order | None:
        statement = select(Order).where(
            Order.user_id == user_id,
            Order.id == order_id,
        )
        return (await self.session.exec(statement)).first()
