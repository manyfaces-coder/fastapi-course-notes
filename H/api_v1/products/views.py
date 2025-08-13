from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from watchfiles import awatch

from H.core.models import db_helper
from . import crud
from .schemas import ProductCreate, Product, ProductUpdate, ProductUpdatePartial
from .dependencies import product_by_id

router = APIRouter(tags=["Products"])


# запрос на получение списка товаров
@router.get("/", response_model=list[Product])
async def get_products(
    # получаем сессию
    session: AsyncSession = Depends(db_helper.scoped_session_dependancy),
):
    return await crud.get_products(
        session=session
    )  # возвращаем объекты, которые сделаны в sqlalchemy, а надо объекты pydantic далее в schemas -> в class Product


# создание товара
@router.post(
    "/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_in: ProductCreate,  # получаем данные из тела запроса
    session: AsyncSession = Depends(db_helper.scoped_session_dependancy),
):
    return await crud.create_product(session=session, product_in=product_in)


# получение товаров по id
@router.get("/{products_id}/", response_model=Product)
async def get_product(
    product: Product = Depends(product_by_id),
):
    return product


@router.put("/{products_id}/")
async def update_product(
    product_update: ProductUpdate,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependancy),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
    )


@router.patch("/{products_id}/")
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependancy),
):
    return await crud.update_product(
        session=session,
        product=product,
        product_update=product_update,
        partial=True,
    )


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product: Product = Depends(product_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependancy),
) -> None:
    return await crud.delete_product(session=session, product=product)


# Создана БД с использованием SQLAlchemy 2.0
# Создан DatabaseHelper, который умеет создавать движок для подключений к БД и фабрику для сессий
# Реализованы сессия для управления данными в БД, создана сессия с привязкой к контексту
# Реализован стандартный CRUD в ассинхронном виде
