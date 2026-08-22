from app.database.models import Locations, User
from app.database.repositories.games import GameRepository
from app.modules.games.exceptions import GameNotFoundError
from app.modules.games.schemas import GameResponse, PaginatedGamesResponse


class GameService:
    def __init__(self, game_repo: GameRepository) -> None:
        self.game_repo = game_repo

    async def list_games(
        self,
        *,
        page: int,
        size: int,
        location: Locations | None = None,
    ) -> PaginatedGamesResponse:
        games, total = await self.game_repo.list_page(page=page, size=size, location=location)
        return PaginatedGamesResponse(
            items=[GameResponse.model_validate(game) for game in games],
            total=total,
            page=page,
            size=size,
        )

    async def get_game(self, game_id: int) -> GameResponse:
        game = await self.game_repo.get(game_id)
        if game is None:
            raise GameNotFoundError(f"Game {game_id} not found")

        return GameResponse.model_validate(game)

    async def list_purchased_games(self, user: User) -> list[GameResponse]:
        games = await self.game_repo.list_purchased_games_for_user(user.id)
        return [GameResponse.model_validate(game) for game in games]
