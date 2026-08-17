from fastapi import FastAPI
from app.database.database import Base, engine
import app.database.models

from app.routers.tasks import router as task_router
from app.routers.categories import router as category_router
from app.routers.users import router as user_router
from app.routers.auth import router as auth_router

app = FastAPI()

app.include_router(task_router)
app.include_router(category_router)
app.include_router(user_router)
app.include_router(auth_router)