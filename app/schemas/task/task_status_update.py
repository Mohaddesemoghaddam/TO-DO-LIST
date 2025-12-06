# from pydantic import BaseModel, Field
# from typing import Literal

# class TaskStatusUpdate(BaseModel):
#     status: Literal["todo", "doing", "done"] = Field(
#         ...,
#         description="New status for the task. Must be one of: todo, doing, done."
#     )
from pydantic import BaseModel, field_validator

VALID_STATUSES = ("todo", "doing", "done")

class TaskStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    def validate_status(cls, v):
        v = v.lower().strip()
        if v not in VALID_STATUSES:
            raise ValueError(f"Invalid status. Choose one of: {', '.join(VALID_STATUSES)}")
        return v

