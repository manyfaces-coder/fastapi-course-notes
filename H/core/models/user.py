from enum import unique

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class User(Base):

    username: Mapped[str] = mapped_column(String(32), unique=True)
    # Mapped указывает, что поле связано с колонкой таблицы в БД, mapped_column uniq - username уникальное,
    # String(32) – ограничение по длине
