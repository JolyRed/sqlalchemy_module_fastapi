from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int

class UpdateUser(CreateUser):
    id: int
    slug: str

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    content: str
    priority: int = 0
    completed: bool = False

class TaskCreate(TaskBase):
    user_id: int 

class TaskUpdate(TaskBase):
    pass 

class TaskResponse(TaskBase):
    id: int
    slug: str

    class Config:
        from_attributes = True