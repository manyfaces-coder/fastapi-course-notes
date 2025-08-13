# через сессию будут запрашиваться данные из базы
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from H.api_v1.products.schemas import ProductCreate, ProductUpdate, ProductUpdatePartial
from H.core.models import Product
from sqlalchemy.engine import Result  # нужен для аннотации всех свойст


async def get_products(session: AsyncSession) -> list[Product]:
    # запрос всех товаров(products)
    stmt = select(Product).order_by(Product.id)
    # выполнение запроса
    result: Result = await session.execute(
        stmt
    )  # Сессия знает как подключиться к бд, т.к. в db_helper указали через какой движок работает в session_factory
    # элементы добавляются не по одному, а все сразу при помощи сессии
    products = (
        result.scalars().all()
    )  # scalars получает скалярные значения, .all() превратит генератор в список
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(
        **product_in.model_dump()
    )  # model_dump() — преобразуют модель в словарь Python
    # добавляем объект product в отслеживание
    session.add(product)
    # сохраняем полученный товар в БД
    await session.commit()
    # в некоторых случаях нужно будет обновить товар, поэтому обновляем его:
    # например в настройках бд, что-то может создавать/меняться при создании объекта
    # в комментарии т.к. при создании у нас ничего не меняется
    # await session.refresh(product)
    # в синхронной алхимии по умолчанию делается expire_on_commit=True, то есть когда делаем коммит,
    # сначала все свойства на объекте сгорают, а когда мы к нему обращаемся, объект запрашивается из бд заново,
    # а так как запрос из бд это ассинхронное взаимодействие, то теперь автоматический запрос пройти не может и
    # будет ошибка, поэтому либо обновляем вручную через await session.refresh(product), либо работаем не с самыми
    # актуальными данными, если, например, в настройках бд, что-то может создаваться/меняться при сохранении объекта
    return product


# PUT и PATCH в одной функции, если partial = False, то объект обновляется целиком, если True,
# то частично исключая не переданные поля
async def update_product(
    session: AsyncSession,
    product: Product,
    product_update: ProductUpdate | ProductUpdatePartial,
    partial: bool = False,
) -> Product:
    for key, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, key, value)
    await session.commit()
    return product


# Удаление
async def delete_product(
    session: AsyncSession,
    product: Product,
) -> None:
    await session.delete(product)
    await session.commit()


# PUT (обновление объекта целиком)
# async def update_product(
#     session: AsyncSession,
#     product: Product,
#     product_update: ProductUpdate,
# ) -> Product:
#     for key, value in product_update.model_dump().items():
#         setattr(product, key, value)
#     await session.commit()
#     return product
#
#
# # PATCH (обновление полей объекта)
# async def update_product_partial(
#     session: AsyncSession, product: Product, product_update: ProductUpdatePartial
# ):
#     # исключаем не переданное поле в exclude_unset
#     for key, value in product_update.model_dump(exclude_unset=True).items():
#         setattr(product, key, value)
#     await session.commit()
#     return product
