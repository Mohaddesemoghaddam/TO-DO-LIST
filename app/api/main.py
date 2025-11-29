from fastapi import FastAPI
from app.api.routers.users_router import router as users_router
from app.api.routers.projects_router import router as projects_router
from app.api.routers.tasks_router import router as tasks_router

app = FastAPI(
    title="ToDoList API",
    description="Phase 3 - Web API (FastAPI)",
    version="1.0.0"
)

# Register Routers
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(projects_router, prefix="/projects", tags=["Projects"])
app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
