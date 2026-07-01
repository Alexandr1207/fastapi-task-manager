from fastapi import FastAPI
from routers.tasks import router as task_router

app = FastAPI()

app.include_router(task_router)

