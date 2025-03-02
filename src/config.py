from typing import ClassVar
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

from enum import Enum

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    BOT_TOKEN: str

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_tasks: ClassVar[list[str]] = [
        "CROSSWORD", "TEXT", "MUSIC", "MUSIC", "PIC", "PIC", "TEXT", "TEXT", "TEXT"]

    ADMINS: ClassVar[list[int]] = [2075302695]

    @property
    def POSTGRES_URI(self) -> str:
        return f"asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

TORTOISE_ORM: dict = {
        "connections": {"default": settings.POSTGRES_URI},
        "apps": {
            "models": {
                "models": ["db", "aerich.models"],
                "default_connection": "default",
            }
        },
    }

AERICH_CONFIG: dict = {
    "connections": {"default": settings.POSTGRES_URI},
    "apps": {
        "models": {
            "models": ["src.db", "aerich.models"],
            "default_connection": "default",
        }
    },
}


class ScoringRules():
    CROSSWORD = 10
    TEXT = 3
    MUSIC = 6
    PIC = 8
    VIDEO = 20

