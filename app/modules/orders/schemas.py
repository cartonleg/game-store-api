from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.database.models import Locations


class CreateOrderRequest(BaseModel):
    game_id: int = Field(gt=0)


class GameSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    price: Decimal
    location: Locations


class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    game_id: int
    price_paid: Decimal
    created_at: datetime
    updated_at: datetime
    game: GameSummary
