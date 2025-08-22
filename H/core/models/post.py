from enum import unique

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Post(Base):

    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(Text, default="", server_default="")
    # разница между default="" и server_default="", в первом случае применяется, когда мы создаем экземпляр
    # прямо в alchemy, а во втором сервером у нас выступает БД и если мы будем создавать запись прямо там
    # вручную, то default применится и там

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
