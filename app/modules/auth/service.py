import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.security import create_access_token, DUMMY_PASSWORD_HASH, hash_password, verify_password
from app.database.models import User
from app.database.repositories.users import UserRepository
from app.modules.auth.exceptions import UsernameTakenError, InvalidCredentialsError
from app.modules.auth.schemas import TokenResponse, UserResponse


class AuthService:
    def __init__(self, db_session: AsyncSession, user_repo: UserRepository) -> None:
        self.db_session = db_session
        self.user_repo = user_repo

    async def register(self, username: str, password: str) -> UserResponse:
        if await self.user_repo.get_by_username(username):
            logging.error(f"User {username} already exists")
            raise UsernameTakenError(f"User {username} is already taken")

        user = User(username=username, password_hash=hash_password(password))
        self.user_repo.add(user)
        try:
            await self.db_session.commit()
            await self.db_session.refresh(user)
        except IntegrityError:
            await self.db_session.rollback()
            raise UsernameTakenError(f"User {username} is already taken")

        logging.info(f"User {username} registered successfully")
        return UserResponse.model_validate(user)

    async def login(self, username: str, password: str) -> TokenResponse:
        user = await self.user_repo.get_by_username(username)
        
        stored_password_hash = user.password_hash if user else DUMMY_PASSWORD_HASH
        if not verify_password(password, stored_password_hash) or user is None:
            logging.error(f"Invalid credentials for user {username}")
            raise InvalidCredentialsError(f"Invalid credentials")
        
        return TokenResponse(
            access_token=create_access_token(username=user.username, role=user.role)
        )
