from typing import Annotated

from fastapi import Depends

from app.database.database import SessionDep
from app.database.repositories.games import GameRepository
from app.database.repositories.orders import OrderRepository
from app.database.repositories.users import UserRepository


def get_user_repository(session: SessionDep) -> UserRepository:
    return UserRepository(session)


def get_game_repository(session: SessionDep) -> GameRepository:
    return GameRepository(session)


def get_order_repository(session: SessionDep) -> OrderRepository:
    return OrderRepository(session)


UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
GameRepoDep = Annotated[GameRepository, Depends(get_game_repository)]
OrderRepoDep = Annotated[OrderRepository, Depends(get_order_repository)]
