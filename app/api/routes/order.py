from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import order as crud
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Order"])


@router.post("/", response_model=OrderOut)
def create(data: OrderCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_order(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{order_id}", response_model=OrderOut)
def get_one(order_id: int, db: Session = Depends(get_db)):
    obj = crud.get_order(db, order_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Order not found")
    return obj


@router.get("/", response_model=list[OrderOut])
def list_all(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_orders(db, skip, limit)


@router.get("/by-user/{user_id}", response_model=list[OrderOut])
def list_by_user(user_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_orders_by_user(db, user_id, skip, limit)


@router.put("/{order_id}", response_model=OrderOut)
def update(order_id: int, data: OrderUpdate, db: Session = Depends(get_db)):
    obj = crud.get_order(db, order_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Order not found")
    return crud.update_order(db, obj, data)


@router.delete("/{order_id}")
def delete(order_id: int, db: Session = Depends(get_db)):
    obj = crud.get_order(db, order_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Order not found")
    crud.delete_order(db, obj)
    return {"message": "Order deleted"}