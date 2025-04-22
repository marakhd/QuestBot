from typing import ClassVar
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

DIR = Path(__file__).parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=DIR / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    BOT_TOKEN: str

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    model_tasks_primary: ClassVar[list[str]] = [
        "CROSSWORD",
        "TEXT",
        "MUSIC",
        "MUSIC",
        "PIC",
        "PIC",
        "TEXT",
        "TEXT",
        "TEXT",
    ]
    model_tasks_high: ClassVar[list[str]] = [
        "CROSSWORD",
        "TEXT",
        "MUSIC",
        "MUSIC",
        "PIC",
        "PIC",
        "TEXT",
        "TEXT",
        "TEXT",
    ]

    ADMINS: ClassVar[list[int]] = [2075302695]

    # @property
    # def URI_DB(self) -> str:
    #     return f"sqlite://./{self.DB_NAME}"

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
            "models": ["db", "aerich.models"],
            "default_connection": "default",
        }
    },
}

