from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.database import engine, get_db
from app.db.base import Base
from app.models import product
from app.api import home  # import home router
from app.api import product
from app.api import auth_routes
from app.api import user_routes

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

#default router
@app.get("/")
def default_page():
    return{
        "message":"this is default page"
    }

#include router
app.include_router(home.router)
app.include_router(product.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)