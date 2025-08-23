from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from .mixins import UserRelationMixin


class Post(UserRelationMixin, Base):
    _user_back_populates = "posts"

    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    # разница между default="" и server_default="", в первом случае применяется, когда мы создаем экземпляр
    # прямо в alchemy, а во втором сервером у нас выступает БД и если мы будем создавать запись прямо там
    # вручную, то default применится и там

    # Перенесли в mixins.py так как здесь и в profile.py повторяются
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user: Mapped[User] = relationship(
    #     back_populates="posts"
    # )  # ссылаем на объект User и нужно указать, какое поле используем, чтобы попасть сюда с юзера
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.title!r}, user_id={self.user_id})"

    def __repr__(self):
        return str(self)
