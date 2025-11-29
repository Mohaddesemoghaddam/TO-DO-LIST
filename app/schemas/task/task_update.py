from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    deadline: Optional[datetime] = None
    status: Optional[str] = None
