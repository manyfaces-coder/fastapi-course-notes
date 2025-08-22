from typing import TYPE_CHECKING
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:  # спрашиваем идет ли проверка типов, а не выполнение кода
    # (при этом импорт не происходит -> не будет циклических импортов)
    from .user import User


class Post(Base):

    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(Text, default="", server_default="")
    # разница между default="" и server_default="", в первом случае применяется, когда мы создаем экземпляр
    # прямо в alchemy, а во втором сервером у нас выступает БД и если мы будем создавать запись прямо там
    # вручную, то default применится и там

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(
        back_populates="posts"
    )  # ссылаем на объект User и нужно указать, какое поле используем, чтобы попасть сюда с юзера
