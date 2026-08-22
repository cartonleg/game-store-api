from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.database.models import Locations


class ImportGamesResponse(BaseModel):
    imported_count: int
    replaced_existing: bool


class GameUpdateRequest(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    description: str | None = Field(default=None, min_length=1)
    price: Decimal | None = Field(default=None, gt=0)
    location: Locations | None = None


class GameResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    price: Decimal
    location: Locations
    created_at: datetime
    updated_at: datetime
