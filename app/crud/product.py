from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, data: ProductCreate) -> Product:
    obj = Product(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_product(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()


def list_products(db: Session, skip: int = 0, limit: int = 50) -> list[Product]:
    return db.query(Product).offset(skip).limit(limit).all()


def list_products_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 50) -> list[Product]:
    return (
        db.query(Product)
        .filter(Product.category_id == category_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_product(db: Session, obj: Product, data: ProductUpdate) -> Product:
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_product(db: Session, obj: Product) -> None:
    db.delete(obj)
    db.commit()