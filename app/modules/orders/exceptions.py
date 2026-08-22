class OrderError(Exception):
    """Base orders module error."""


class GameNotFoundError(OrderError):
    pass


class AlreadyPurchasedError(OrderError):
    pass


class OrderNotFoundError(OrderError):
    pass
