from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.database.models import Locations


class GameResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    price: Decimal
    location: Locations
    created_at: datetime
    updated_at: datetime


class PaginatedGamesResponse(BaseModel):
    items: list[GameResponse]
    total: int
    page: int
    size: int
