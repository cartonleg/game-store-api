from pydantic import computed_field, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.config.utils import resolve_env_files


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=resolve_env_files(),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    POSTGRES_USER: str = Field(...)
    POSTGRES_PASSWORD: str = Field(...)
    POSTGRES_DB: str = Field(...)
    POSTGRES_PORT: int = Field(...)
    POSTGRES_HOST: str = Field(...)

    ALLOWED_ORIGINS: str = Field(...)

    SECRET_KEY: str = Field(...)
    ALGORITHM: str = Field(...)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(...)

    ADMIN_USERNAME: str | None = None
    ADMIN_PASSWORD: str | None = None

    @computed_field
    @property
    def POSTGRES_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )

settings = Settings()
