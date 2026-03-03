from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1


class OrderUpdate(BaseModel):
    quantity: int | None = None
    status: str | None = None


class OrderOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    total_amount: float
    status: str

    model_config = {"from_attributes": True}