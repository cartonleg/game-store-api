from fastapi import APIRouter, HTTPException

from app.core.auth.dependencies import CurrentUserDep
from app.database.database import SessionDep
from app.database.repositories import GameRepoDep, OrderRepoDep
from app.modules.orders.exceptions import AlreadyPurchasedError, GameNotFoundError, OrderNotFoundError
from app.modules.orders.schemas import CreateOrderRequest, OrderResponse
from app.modules.orders.service import OrderService

router = APIRouter()


@router.post("", response_model=OrderResponse, status_code=201)
async def purchase_game(
    body: CreateOrderRequest,
    user: CurrentUserDep,
    session: SessionDep,
    order_repo: OrderRepoDep,
    game_repo: GameRepoDep,
) -> OrderResponse:
    service = OrderService(session, order_repo, game_repo)
    try:
        return await service.purchase(user, body.game_id)
    except GameNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AlreadyPurchasedError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("", response_model=list[OrderResponse])
async def list_orders(
    user: CurrentUserDep,
    session: SessionDep,
    order_repo: OrderRepoDep,
    game_repo: GameRepoDep,
) -> list[OrderResponse]:
    return await OrderService(session, order_repo, game_repo).list_orders(user)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    user: CurrentUserDep,
    session: SessionDep,
    order_repo: OrderRepoDep,
    game_repo: GameRepoDep,
) -> OrderResponse:
    service = OrderService(session, order_repo, game_repo)
    try:
        return await service.get_order(user, order_id)
    except OrderNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except GameNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
