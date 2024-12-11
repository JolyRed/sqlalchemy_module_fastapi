from app.backend.db import engine, Base
from app.models import User, Task 

Base.metadata.create_all(bind=engine)
print("Таблицы успешно созданы!")
