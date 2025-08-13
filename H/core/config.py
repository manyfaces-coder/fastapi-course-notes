from os import getenv  # Достает параметры из переменных окружения
from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db_url: str = f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    # нужен, чтобы видеть какие запросы выполняются
    db_echo: bool = (
        False  # True только в отладке, иначе будет долго грузить и это будет небезопасно
    )


settings = Setting()
