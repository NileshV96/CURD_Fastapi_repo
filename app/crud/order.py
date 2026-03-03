from decimal import Decimal
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdate


def create_order(db: Session, data: OrderCreate) -> Order:
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise ValueError("Product not found")

    total = Decimal(str(product.price)) * Decimal(data.quantity)

    obj = Order(
        user_id=data.user_id,
        product_id=data.product_id,
        quantity=data.quantity,
        total_amount=total,
        status="PLACED",
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_order(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.id == order_id).first()


def list_orders(db: Session, skip: int = 0, limit: int = 50) -> list[Order]:
    return db.query(Order).offset(skip).limit(limit).all()


def list_orders_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 50) -> list[Order]:
    return db.query(Order).filter(Order.user_id == user_id).offset(skip).limit(limit).all()


def update_order(db: Session, obj: Order, data: OrderUpdate) -> Order:
    payload = data.model_dump(exclude_unset=True)

    # If quantity changes, recompute total_amount
    if "quantity" in payload:
        product = db.query(Product).filter(Product.id == obj.product_id).first()
        total = Decimal(str(product.price)) * Decimal(payload["quantity"])
        obj.total_amount = total
        obj.quantity = payload["quantity"]

    if "status" in payload:
        obj.status = payload["status"]

    db.commit()
    db.refresh(obj)
    return obj


def delete_order(db: Session, obj: Order) -> None:
    db.delete(obj)
    db.commit()