from sqlite3 import connect
from urllib.request import Request

from app.routers import user, task
from fastapi import FastAPI, APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from app.models import User
from app.schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify


app = FastAPI()

@app.get("/")
async def all_users(request: Request):
    pass

app.include_router(user.router)
app.include_router(task.router)
