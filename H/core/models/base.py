from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    """
    Абстрактная модель – не добавляется в БД.
    Родительский класс, от которого другие модели будут брать одинаковые свойства
    """

    @declared_attr.directive  # указывает, что наименовние таблиц в БД будет браться от названий классов моделей
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
