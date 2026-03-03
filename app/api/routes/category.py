from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import category as crud
from app.schemas.category import CategoryCreate, CategoryOut, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Category"])


@router.post("/", response_model=CategoryOut)
def create(data: CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, data)


@router.get("/{category_id}", response_model=CategoryOut)
def get_one(category_id: int, db: Session = Depends(get_db)):
    obj = crud.get_category(db, category_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return obj


@router.get("/", response_model=list[CategoryOut])
def list_all(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_categories(db, skip, limit)


@router.put("/{category_id}", response_model=CategoryOut)
def update(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    obj = crud.get_category(db, category_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.update_category(db, obj, data)


@router.delete("/{category_id}")
def delete(category_id: int, db: Session = Depends(get_db)):
    obj = crud.get_category(db, category_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Category not found")
    crud.delete_category(db, obj)
    return {"message": "Category deleted"}