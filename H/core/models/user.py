from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .post import Post


class User(Base):

    username: Mapped[str] = mapped_column(String(32), unique=True)
    # Mapped указывает, что поле связано с колонкой таблицы в БД, mapped_column uniq - username уникальное,
    # String(32) – ограничение по длине
    posts: Mapped[list[Post]] = relationship(back_populates="user")
