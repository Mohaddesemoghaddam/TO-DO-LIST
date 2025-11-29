from fastapi import FastAPI

from app.api.routers.user_router import router as user_router
from app.api.routers.projects_router import router as projects_router
from app.api.routers.tasks_router import router as tasks_router
from app.api.routers.project_router import router as project_router


app = FastAPI(
    title="ToDoList API",
    description="Phase 3 - Web API (FastAPI)",
    version="1.0.0"
)

# Register Routers
app.include_router(user_router)
app.include_router(projects_router)
app.include_router(tasks_router)
app.include_router(project_router)
