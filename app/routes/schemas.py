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
        orm_mode = True
