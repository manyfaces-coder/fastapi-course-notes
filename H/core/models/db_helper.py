# движок для создания бд
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)
from sqlalchemy.orm import sessionmaker
from asyncio import current_task

from H.core.config import settings


class DatabaseHelper:
    """
    Подключение к БД
    """

    def __init__(self, url: str, echo: bool = False):
        # движок – объект подключения к базе данных, создает и управляет подключениями к БД "фабрика подключений"
        # даёт сессиям доступ к базе
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        # фабрика сессий
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,  # подготовка к авто-коммиту
            autocommit=False,
            expire_on_commit=False,  # не должно быть автоматического удаления информации о текущих объектах из сессии
        )

    # получение актуальной сессии
    def get_scoped_session(self):
        session = async_scoped_session(
            self.session_factory,
            scopefunc=current_task,
        )  # scope - текущие пространство, получаем из текущей задачи, далее алхимия сможет проверять, что мы
        # в текущей задаче и можем взять ту же самую сессию из этой задачи
        return session

    # создание сессии для каждого запроса, со scoped_session для некоторых запросов можно будет использовать
    # одну и ту же сессию, а не создавать новую
    async def session_dependency(
        self,
    ) -> AsyncSession:  # используем во view чтобы получить сессию
        # self.get_scoped_session() – сессия создалась и далее в async with мы ее отдаем
        # async with self.get_scoped_session() as session:
        async with self.session_factory() as session:
            yield session  # yield используется, чтобы сессия не закрылась сразу после покидания контекста
            await session.close()

    async def scoped_session_dependancy(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()


# передаем нужные параметры
db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo,
)
