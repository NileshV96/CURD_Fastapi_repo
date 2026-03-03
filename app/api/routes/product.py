from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import product as crud
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate

router = APIRouter(prefix="/products", tags=["Product"])


@router.post("/", response_model=ProductOut)
def create(data: ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, data)


@router.get("/{product_id}", response_model=ProductOut)
def get_one(product_id: int, db: Session = Depends(get_db)):
    obj = crud.get_product(db, product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    return obj


@router.get("/", response_model=list[ProductOut])
def list_all(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_products(db, skip, limit)


@router.get("/by-category/{category_id}", response_model=list[ProductOut])
def list_by_category(category_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_products_by_category(db, category_id, skip, limit)


@router.put("/{product_id}", response_model=ProductOut)
def update(product_id: int, data: ProductUpdate, db: Session = Depends(get_db)):
    obj = crud.get_product(db, product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    return crud.update_product(db, obj, data)


@router.delete("/{product_id}")
def delete(product_id: int, db: Session = Depends(get_db)):
    obj = crud.get_product(db, product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.delete_product(db, obj)
    return {"message": "Product deleted"}