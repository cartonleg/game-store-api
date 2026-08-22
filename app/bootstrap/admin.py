import logging

from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.core.auth.security import hash_password
from app.database.database import async_session_factory
from app.database.models import Roles, User
from app.database.repositories.users import UserRepository


async def ensure_admin_user() -> None:
    if not settings.ADMIN_USERNAME or not settings.ADMIN_PASSWORD:
        return

    async with async_session_factory() as session:
        user_repo = UserRepository(session)
        existing = await user_repo.get_by_username(settings.ADMIN_USERNAME)
        if existing is not None:
            if existing.role is not Roles.ADMIN:
                existing.role = Roles.ADMIN
                await session.commit()
                logging.info("Promoted user %s to admin", settings.ADMIN_USERNAME)
            return

        user = User(
            username=settings.ADMIN_USERNAME,
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            role=Roles.ADMIN,
        )
        user_repo.add(user)
        try:
            await session.commit()
            logging.info("Seeded admin user %s", settings.ADMIN_USERNAME)
        except IntegrityError:
            await session.rollback()
