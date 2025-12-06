from pydantic import BaseModel, Field, validator
from datetime import datetime

class TaskCreate(BaseModel):
    description: str = Field(..., min_length=3, max_length=255)
    deadline: datetime

    @validator("deadline")
    def must_be_future(cls, v):
        if v <= datetime.utcnow():
            raise ValueError("Deadline must be a future date/time.")
        return v
