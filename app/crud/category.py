from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def create_category(db: Session, data: CategoryCreate) -> Category:
    obj = Category(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_category(db: Session, category_id: int) -> Category | None:
    return db.query(Category).filter(Category.id == category_id).first()


def list_categories(db: Session, skip: int = 0, limit: int = 50) -> list[Category]:
    return db.query(Category).offset(skip).limit(limit).all()


def update_category(db: Session, obj: Category, data: CategoryUpdate) -> Category:
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


def delete_category(db: Session, obj: Category) -> None:
    db.delete(obj)
    db.commit()