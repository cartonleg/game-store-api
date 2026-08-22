from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import Column, DateTime, Enum as SAEnum, func, UniqueConstraint
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def timestamp_column(*, auto_update: bool = False) -> Column:
    return Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=utc_now if auto_update else None,
    )


class Roles(StrEnum):
    USER = "user"
    ADMIN = "admin"


class Locations(StrEnum):
    JORDAN = "JO"
    SAUDI_ARABIA = "SA"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True, max_length=20)
    password_hash: str
    role: Roles = Field(
        default=Roles.USER,
        sa_column=Column(
            SAEnum(Roles, values_callable=lambda e: [m.value for m in e]),
            nullable=False,
            server_default=Roles.USER.value,
        ),
    )
    created_at: datetime = Field(default_factory=utc_now, sa_column=timestamp_column())


class Game(SQLModel, table=True):
    __tablename__ = "games"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str
    price: Decimal = Field(max_digits=10, decimal_places=2)
    location: Locations = Field(
        sa_column=Column(SAEnum(Locations, values_callable=lambda e: [m.value for m in e]), nullable=False)
    )
    created_at: datetime = Field(default_factory=utc_now, sa_column=timestamp_column())
    updated_at: datetime = Field(default_factory=utc_now, sa_column=timestamp_column(auto_update=True))


class Order(SQLModel, table=True):
    __tablename__ = "orders"
    __table_args__ = (UniqueConstraint("user_id", "game_id", name="uq_orders_user_game"),)

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    game_id: int = Field(foreign_key="games.id", index=True)
    price_paid: Decimal = Field(max_digits=10, decimal_places=2)
    created_at: datetime = Field(default_factory=utc_now, sa_column=timestamp_column())
    updated_at: datetime = Field(default_factory=utc_now, sa_column=timestamp_column(auto_update=True))
