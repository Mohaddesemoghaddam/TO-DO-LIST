# app/schemas/task/task_response.py

from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    status: str
    deadline: datetime | None = Field(None)
    project_id: int
    created_at: datetime
    updated_at: datetime
