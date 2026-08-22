class GameError(Exception):
    """Base games module error."""


class GameNotFoundError(GameError):
    pass
