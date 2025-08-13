from pydantic import BaseModel, ConfigDict


# превращает свойства таблиц в json чтобы вернуть обратно пользователю
class ProductBase(BaseModel):
    name: str
    description: str
    price: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    pass


class ProductUpdatePartial(ProductCreate):
    name: str | None = None
    description: str | None = None
    price: int | None = None


class Product(ProductBase):
    # конвертация данных в объекты pydantic
    model_config = ConfigDict(
        from_attributes=True
    )  # конфигурация, указывающая, что нужно брать свойства с аттрибутов.
    id: int  # Вынесли отдельно, чтобы id создавался сам и не давало создавать его пользоватьлям
