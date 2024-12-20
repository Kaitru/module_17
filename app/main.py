from fastapi import FastAPI
from app.routers import user, task

app = FastAPI()

app.include_router(user.router)
app.include_router(task.router)
