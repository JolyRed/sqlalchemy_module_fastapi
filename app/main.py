from fastapi import FastAPI
from app.routes import user_routes, task_routes

app = FastAPI()
app.include_router(user_routes.router)
app.include_router(task_routes.router)
