from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock_qty: int = 0
    category_id: int
    is_active: bool = True


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock_qty: int | None = None
    category_id: int | None = None
    is_active: bool | None = None


class ProductOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock_qty: int
    category_id: int
    is_active: bool

    model_config = {"from_attributes": True}