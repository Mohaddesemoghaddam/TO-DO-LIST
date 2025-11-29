from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    deadline: Optional[datetime]
    status: str
    project_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
