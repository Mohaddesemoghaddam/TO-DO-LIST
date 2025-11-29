from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    deadline: Optional[datetime] = None
    status: Optional[str] = "todo"
    project_id: int
