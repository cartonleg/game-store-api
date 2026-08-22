from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.auth.dependencies import AdminUserDep
from app.database.database import SessionDep
from app.database.repositories import GameRepoDep
from app.modules.admin.exceptions import CatalogReplaceError, GameNotFoundError
from app.modules.admin.schemas import GameResponse, GameUpdateRequest, ImportGamesResponse
from app.modules.admin.service import AdminService
from app.utils.csv_parser import CsvParseError


router = APIRouter()


@router.post("/games/import", response_model=ImportGamesResponse)
async def import_games(
    _admin: AdminUserDep,
    session: SessionDep,
    game_repo: GameRepoDep,
    file: UploadFile = File(...),
    replace: bool = False,
) -> ImportGamesResponse:
    if file.content_type not in {None, "text/csv", "application/csv", "application/vnd.ms-excel"}:
        raise HTTPException(status_code=400, detail="File must be a CSV")

    raw = await file.read()
    try:
        content = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 encoded") from exc

    service = AdminService(session, game_repo)
    try:
        return await service.import_games_csv(content, replace=replace)
    except CsvParseError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except CatalogReplaceError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.patch("/games/{game_id}", response_model=GameResponse)
async def update_game(
    game_id: int,
    body: GameUpdateRequest,
    _admin: AdminUserDep,
    session: SessionDep,
    game_repo: GameRepoDep,
) -> GameResponse:
    updates = body.model_dump(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    service = AdminService(session, game_repo)
    try:
        return await service.update_game(game_id, updates)
    except GameNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except CatalogReplaceError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
