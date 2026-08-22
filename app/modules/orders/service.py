from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Order, User, Game
from app.database.repositories.games import GameRepository
from app.database.repositories.orders import OrderRepository
from app.modules.orders.exceptions import AlreadyPurchasedError, GameNotFoundError, OrderNotFoundError
from app.modules.orders.schemas import GameSummary, OrderResponse


class OrderService:
    def __init__(
        self,
        db_session: AsyncSession,
        order_repo: OrderRepository,
        game_repo: GameRepository,
    ) -> None:
        self.db_session = db_session
        self.order_repo = order_repo
        self.game_repo = game_repo

    async def _to_response(self, order: Order, game: Game | None = None) -> OrderResponse:
        if game is None:
            game = await self.game_repo.get(order.game_id)
            if game is None:
                raise GameNotFoundError(f"Game {order.game_id} not found")

        return OrderResponse(
            id=order.id,
            game_id=order.game_id,
            price_paid=order.price_paid,
            created_at=order.created_at,
            updated_at=order.updated_at,
            game=GameSummary.model_validate(game),
        )

    async def purchase(self, user: User, game_id: int) -> OrderResponse:
        game = await self.game_repo.get(game_id)
        if game is None:
            raise GameNotFoundError(f"Game {game_id} not found")

        if await self.order_repo.exists_for_user_and_game(user.id, game_id):
            raise AlreadyPurchasedError("You have already purchased this game")

        order = Order(user_id=user.id, game_id=game_id, price_paid=game.price)
        self.order_repo.add(order)

        try:
            await self.db_session.commit()
            await self.db_session.refresh(order)
        except IntegrityError as exc:
            await self.db_session.rollback()
            raise AlreadyPurchasedError("You have already purchased this game") from exc

        return await self._to_response(order, game)

    async def list_orders(self, user: User) -> list[OrderResponse]:
        orders = await self.order_repo.list_for_user(user.id)
        return [await self._to_response(order) for order in orders]

    async def get_order(self, user: User, order_id: int) -> OrderResponse:
        order = await self.order_repo.get_for_user(user.id, order_id)
        if order is None:
            raise OrderNotFoundError(f"Order {order_id} not found")

        return await self._to_response(order)
