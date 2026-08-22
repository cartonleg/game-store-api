from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.auth.security import decode_access_token
from app.database.models import Roles, User
from app.database.repositories import UserRepoDep


bearer_schema = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_schema)],
    user_repo: UserRepoDep,
) -> User:
    token = credentials.credentials
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    try:
        uid = int(user_id)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await user_repo.get(uid)

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


async def require_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    if user.role is not Roles.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
AdminUserDep = Annotated[User, Depends(require_admin)]
