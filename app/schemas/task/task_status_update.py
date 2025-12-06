from pydantic import BaseModel, Field
from typing import Literal

class TaskStatusUpdate(BaseModel):
    status: Literal["todo", "doing", "done"] = Field(
        ...,
        description="New status for the task. Must be one of: todo, doing, done."
    )
