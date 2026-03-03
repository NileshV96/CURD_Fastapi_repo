from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud import user as crud
from app.schemas.user import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/", response_model=UserOut)
def create(data: UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    return crud.create_user(db, data)


@router.get("/{user_id}", response_model=UserOut)
def get_one(user_id: int, db: Session = Depends(get_db)):
    obj = crud.get_user(db, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    return obj


@router.get("/", response_model=list[UserOut])
def list_all(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return crud.list_users(db, skip, limit)


@router.put("/{user_id}", response_model=UserOut)
def update(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    obj = crud.get_user(db, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db, obj, data)


@router.delete("/{user_id}")
def delete(user_id: int, db: Session = Depends(get_db)):
    obj = crud.get_user(db, user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, obj)
    return {"message": "User deleted"}