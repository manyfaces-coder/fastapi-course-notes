from fastapi import Depends, Path, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from H.core.models import db_helper, Product

from . import crud


# функция получает текущий id продукта и сессию и возвращает продукт
async def product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependancy),
) -> Product:
    product = await crud.get_product(session=session, product_id=product_id)
    if product is not None:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found :(",
    )
