from fastapi import APIRouter, HTTPException, Query

from app.core.auth.dependencies import CurrentUserDep
from app.database.models import Locations
from app.database.repositories import GameRepoDep
from app.modules.games.exceptions import GameNotFoundError
from app.modules.games.schemas import GameResponse, PaginatedGamesResponse
from app.modules.games.service import GameService

router = APIRouter()


@router.get("", response_model=PaginatedGamesResponse)
async def list_games(
    _user: CurrentUserDep,
    game_repo: GameRepoDep,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    location: Locations | None = None,
) -> PaginatedGamesResponse:
    return await GameService(game_repo).list_games(page=page, size=size, location=location)


@router.get("/purchased", response_model=list[GameResponse])
async def list_purchased_games(
    user: CurrentUserDep,
    game_repo: GameRepoDep,
) -> list[GameResponse]:
    return await GameService(game_repo).list_purchased_games(user)


@router.get("/{game_id}", response_model=GameResponse)
async def get_game(
    game_id: int,
    _user: CurrentUserDep,
    game_repo: GameRepoDep,
) -> GameResponse:
    try:
        return await GameService(game_repo).get_game(game_id)
    except GameNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
