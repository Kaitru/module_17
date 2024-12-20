from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from app.backend.db_depends import get_db
from app.models import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify
router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    query = select(User)
    users = db.scalars(query).all()
    return users

@router.get("/{user_id}")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    query = select(User).where(User.id == user_id)
    user = db.scalars(query).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    else:
        return user

@router.post("/create")
async def create_user(user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    slug = slugify(f"{user.firstname}-{user.lastname}")
    query = insert(User).values(username=user.username,
                                firstname=user.firstname,
                                lastname=user.lastname,
                                age=user.age,
                                slug=slug)
    db.execute(query)
    db.commit()

    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

@router.put("/{user_id}")
async def update_user(user_id: int, user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    query = update(User).where(User.id == user.id).values(username=user.username,
                                                         firstname=user.firstname,
                                                         lastname=user.lastname,
                                                         age=user.age,
                                                         slug=slugify(f"{user.firstname}-{user.lastname}"))
    if user.id is None:
        raise HTTPException(status_code=404, detail="User was not found")
    else:
        db.execute(query)
        db.commit()

@router.delete("/{user_id}")
async def delete_user(userdb: Annotated[Session, Depends(get_db)]):
    pass
