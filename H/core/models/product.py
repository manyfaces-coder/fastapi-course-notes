from sqlalchemy.orm import Mapped

from .base import Base


class Product(Base):

    name: Mapped[str]  # Mapped указывает, что поле связано с колонкой таблицы в БД
    description: Mapped[str]
    price: Mapped[int]
