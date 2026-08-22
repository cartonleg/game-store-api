from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.database.models import Roles


class RegisterRequest(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=20)
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    role: Roles
    created_at: datetime
