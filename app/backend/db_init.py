from app.models.db import Base, engine
from app.models.user import User
from app.models.task import Task

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


def drop_tables():
    Base.metadata.drop_all(bind=engine)
    print("Tables dropped successfully.")

if __name__ == "__main__":
    create_tables()
