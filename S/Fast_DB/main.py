from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated
"""
В видосе не запустилось т к не была установлена библиотека greenlet
"""
app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///books.db')

#Транзакция в БД чтобы открыть сделать запросы и закрыть
new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass


class BookModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    #маппед - обязательная
    title: Mapped[str]
    author: Mapped[str]

@app.post("/setup_database")#post потому что создаем таблицы и тд
async def setup_database():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata) #в аттрибут metadata записываются все метаданные какие есть таблицы/поля/связи
        await conn.run_sync(Base.metadata.drop_all) #сначала очищаем
        await conn.run_sync(Base.metadata.create_all) #создать все таблицы/столбцы/...
    return {"ok": True}


class BookAddSchema(BaseModel):
    title: str
    author: str


class BookSchema(BaseModel):
    id: int

@app.post("/books")
async def add_book(data: BookAddSchema, session: SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author
    )
    session.add(new_book)
    await session.commit()
    return {"ok": True}


@app.get("/books")
async def get_book(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)

    return result.scalars().all()