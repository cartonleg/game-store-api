class AdminError(Exception):
    """Base admin module error."""


class CatalogReplaceError(AdminError):
    pass


class GameNotFoundError(AdminError):
    pass
