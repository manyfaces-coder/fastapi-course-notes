from os import getenv  # Достает параметры из переменных окружения
from pydantic_settings import BaseSettings
from pydantic import BaseModel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "db.sqlite3"


class DbSettings(BaseModel):
    url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    # нужен, чтобы видеть какие запросы выполняются
    echo: bool = (
        True  # True только в отладке, иначе будет долго грузить и это будет небезопасно
    )


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()


settings = Settings()
