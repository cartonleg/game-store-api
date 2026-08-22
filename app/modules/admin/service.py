from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.games import GameRepository
from app.modules.admin.exceptions import CatalogReplaceError, GameNotFoundError
from app.modules.admin.schemas import GameResponse, ImportGamesResponse
from app.utils.csv_parser import parse_games_csv


class AdminService:
    def __init__(self, db_session: AsyncSession, game_repo: GameRepository) -> None:
        self.db_session = db_session
        self.game_repo = game_repo

    async def import_games_csv(self, content: str, *, replace: bool = True) -> ImportGamesResponse:
        games = parse_games_csv(content)

        if replace:
            try:
                await self.game_repo.delete_all()
            except IntegrityError as exc:
                await self.db_session.rollback()
                raise CatalogReplaceError(
                    "Cannot replace the catalog while orders reference existing games"
                ) from exc

        self.game_repo.add_multiple(games)
        await self.db_session.commit()

        return ImportGamesResponse(imported_count=len(games), replaced_existing=replace)

    async def update_game(self, game_id: int, updates: dict[str, object]) -> GameResponse:
        game = await self.game_repo.get(game_id)
        if game is None:
            raise GameNotFoundError(f"Game {game_id} not found")

        for field, value in updates.items():
            setattr(game, field, value)

        try:
            await self.db_session.commit()
            await self.db_session.refresh(game)
        except IntegrityError as exc:
            await self.db_session.rollback()
            raise CatalogReplaceError("Game update conflicts with existing data") from exc

        return GameResponse.model_validate(game)
