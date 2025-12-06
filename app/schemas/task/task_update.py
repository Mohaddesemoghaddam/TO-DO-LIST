from pydantic import BaseModel, Field, validator
from datetime import datetime

class TaskUpdate(BaseModel):
    new_description: str | None = Field(None, min_length=3, max_length=255)
    new_deadline: datetime | None = None

    @validator("new_deadline")
    def must_be_future(cls, v):
        if v is None:
            return v
        if v <= datetime.utcnow():
            raise ValueError("Deadline must be a future date/time.")
        return v
