from fastapi import FastAPI

from app.api.routes.project_router import router as project_router
from app.api.routes.task_router import router as task_router

app = FastAPI(
    title="ToDoList API",
    description="Phase 3 - Web API (FastAPI)",
    version="1.0.0"
)


app.include_router(project_router)
app.include_router(task_router)
