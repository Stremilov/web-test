import logging
import os
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic.v1 import BaseSettings

load_dotenv()

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class LoggingSettings(BaseModel):
    log_level: Literal[
        "debug",
        "info",
        "warning",
        "error",
        "critical",
    ] = "info"
    log_format: str = LOG_DEFAULT_FORMAT

    @property
    def log_level_value(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level.upper()]


class RunSettings(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000


class DBSettings(BaseModel):
    DB_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    DB_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DB_NAME: str = os.getenv("DATABASE_NAME", "postgres")
    DB_USER: str = os.getenv("DATABASE_USER", "postgres")
    DB_PORT: str = os.getenv("DATABASE_PORT", "5432")
    DATABASE_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Settings(BaseSettings):
    db: DBSettings = DBSettings()
    logging: LoggingSettings = LoggingSettings()
    run: RunSettings = RunSettings()


settings = Settings()