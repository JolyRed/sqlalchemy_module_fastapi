from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db 
from typing import Annotated, List
from models.task import Task  
from models.user import User 
from routes.schemas import CreateTask, UpdateTask  
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/tasks")

@router.get("/", response_model=List[Task])
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.execute(select(Task)).scalars().all()
    return tasks

@router.get("/{task_id}", response_model=Task)
async def task_by_id(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")
    return task

@router.post("/create", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_task(new_task: CreateTask, user_id: int, db: Annotated[Session, Depends(get_db)]):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    
    new_task_dict = new_task.dict()
    new_task_dict["user_id"] = user_id
    db.execute(insert(Task).values(new_task_dict))
    db.commit()
    return {"status_code": status.HTTP_201_CREATED, "transaction": "Successful"}

@router.put("/update/{task_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def update_task(task_id: int, updated_task: UpdateTask, db: Annotated[Session, Depends(get_db)]):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")
    
    updated_task_dict = updated_task.dict(exclude={"id"})
    db.execute(update(Task).where(Task.id == task_id).values(updated_task_dict))
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "Task update is successful!"}

@router.delete("/delete/{task_id}", response_model=dict, status_code=status.HTTP_200_OK)
async def delete_task(task_id: int, db: Annotated[Session, Depends(get_db)]):
    task = db.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")
    
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {"status_code": status.HTTP_200_OK, "transaction": "Task deleted successfully!"}
