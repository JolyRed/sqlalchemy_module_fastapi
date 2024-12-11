from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db 
from typing import Annotated, List
from models.user import User
from routes.schemas import CreateUser, UpdateUser 
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/users")

@router.get("/", response_model=List[UpdateUser]) 
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.execute(select(User)).scalars().all()
    return users

@router.get("/{user_id}", response_model=UpdateUser)
async def user_by_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    return user

@router.post("/create", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user(new_user: CreateUser, db: Annotated[Session, Depends(get_db)]):
    try:
        new_user_dict = new_user.dict()
        new_user_dict["slug"] = slugify(new_user_dict["username"]) 
        db.execute(insert(User).values(new_user_dict))
        db.commit()
        return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}
    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

@router.put("/update/{user_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, updated_user: UpdateUser, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    updated_user_dict = updated_user.dict(exclude={"id"}) 
    updated_user_dict["slug"] = slugify(updated_user_dict["username"]) 
    db.execute(update(User).where(User.id == user_id).values(updated_user_dict))
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User update is successful!"}


@router.delete("/delete/{user_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "User deleted successfully!"}
