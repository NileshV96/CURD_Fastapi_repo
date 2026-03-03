from fastapi import FastAPI
from app.core.config import settings
from app.api.routes.api import api_router
from app.db.session import engine
from app.db.base import Base

# Import models so SQLAlchemy knows them before create_all
from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.order import Order

app = FastAPI(title=settings.app_name)

# Create DB tables (simple approach for beginner tasks)
Base.metadata.create_all(bind=engine)

app.include_router(api_router)


@app.get("/")
def health():
    return {"status": "ok", "app": settings.app_name}

