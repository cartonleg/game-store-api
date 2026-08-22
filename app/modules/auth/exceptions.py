class AuthError(Exception):
    """base auth error."""


class InvalidCredentialsError(AuthError):
    pass


class UsernameTakenError(AuthError):
    pass
