# from pydantic import BaseModel, Field
# from typing import Literal

# class TaskStatusUpdate(BaseModel):
#     status: Literal["todo", "doing", "done"] = Field(
#         ...,
#         description="New status for the task. Must be one of: todo, doing, done."
#     )
# from pydantic import BaseModel, field_validator

# VALID_STATUSES = ("todo", "doing", "done")

# class TaskStatusUpdate(BaseModel):
#     status: str

#     @field_validator("status")
#     def validate_status(cls, v):
#         v = v.lower().strip()
#         if v not in VALID_STATUSES:
#             raise ValueError(f"Invalid status. Choose one of: {', '.join(VALID_STATUSES)}")
#         return v

from pydantic import BaseModel, Field, ConfigDict, field_validator

VALID_STATUSES = ("todo", "doing", "done")


class TaskStatusUpdate(BaseModel):
    """
    Schema for updating only the status of a task (used in PATCH endpoints).

    Ensures the status value is clean, lowercase, trimmed, and restricted
    to 'todo', 'doing', or 'done'.
    """

    status: str = Field(
        ...,
        title="Task Status",
        description="New status for the task. Must be one of: todo, doing, done.",
        example="done"
    )

    # ------------------------------
    # VALIDATOR
    # ------------------------------
    @field_validator("status")
    def validate_status(cls, value: str) -> str:
        """Validate the task status for allowable values."""
        value = value.lower().strip()
        if value not in VALID_STATUSES:
            raise ValueError(f"Invalid status. Choose one of: {', '.join(VALID_STATUSES)}.")
        return value

    # ------------------------------
    # MODEL CONFIGURATION
    # ------------------------------
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Trim input whitespace globally
        extra="forbid",             # Reject unexpected fields in request body
        json_schema_extra={
            "example": {
                "status": "done"
            }
        }
    )
