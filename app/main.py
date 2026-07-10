from fastapi import FastAPI
from database.database import Base, engine
import database.models

from routers.tasks import router as task_router
from routers.categories import router as category_router

app = FastAPI()

app.include_router(task_router)
app.include_router(category_router)