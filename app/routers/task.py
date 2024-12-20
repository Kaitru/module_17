from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from app.backend.db_depends import get_db
from app.models import Task, User
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify
import random
import string

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    query = select(Task)
    tasks = db.scalars(query).all()
    return tasks

@router.get("/{task_id}")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    query = select(Task).where(Task.id == task_id)
    task = db.scalars(query).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task was not found")
    return task

@router.post("/create")
async def create_task(task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_query = select(User).where(User.id == user_id)
    user = db.scalars(user_query).first()
    
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
    query = insert(Task).values(
        title=task.title,
        content=task.content,
        priority=task.priority,
        slug=slugify(f"{task.title}-{task.content}-{random_suffix}"),
        user_id=user_id
    )
    
    db.execute(query)
    db.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

@router.put("/update")
async def update_task(task_id: int, task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    query = select(Task).where(Task.id == task_id)
    existing_task = db.scalars(query).first()

    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

    update_query = update(Task).where(Task.id == task_id).values(
        title=task.title,
        content=task.content,
        priority=task.priority,
        slug=slugify(f"{task.title}-{task.content}-{random_suffix}")
    )

    db.execute(update_query)
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "Task update is successful!"}

@router.delete("/delete")
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    # Сначала проверяем существование задачи
    check_query = select(Task).where(Task.id == task_id)
    task = db.scalars(check_query).first()

    if task is None:
        raise HTTPException(status_code=404, detail="Task was not found")

    # Затем выполняем удаление
    delete_query = delete(Task).where(Task.id == task_id)
    db.execute(delete_query)
    db.commit()
    
    return {"status_code": status.HTTP_200_OK, "transaction": "Task deletion is successful!"}
