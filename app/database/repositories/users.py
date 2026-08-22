from sqlmodel import select

from app.database.models import User
from app.database.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    model = User

    async def get_by_username(self, username: str) -> User | None:
        return (
            await self.session.exec(select(User).where(User.username == username))
        ).first()
