# from pydantic import BaseModel, Field, field_validator
# from datetime import datetime
# from typing import Optional
# from dateutil import parser

# VALID_STATUSES = ("todo", "doing", "done")


# class TaskCreate(BaseModel):
#     title: str = Field(..., min_length=1, max_length=30)
#     description: str = Field(..., min_length=1, max_length=150)
#     status: Optional[str] = "todo"
#     deadline: datetime

#     # ------------------------------
#     # STATUS VALIDATOR
#     # ------------------------------
#     @field_validator("status")
#     def validate_status(cls, value):
#         if value is None:
#             return "todo"
#         value = value.lower().strip()
#         if value not in VALID_STATUSES:
#             raise ValueError(f"Status must be one of: {VALID_STATUSES}")
#         return value

#     # ------------------------------
#     # DEADLINE FLEXIBLE PARSER
#     # ------------------------------
#     @field_validator("deadline", mode="before")
#     def parse_deadline(cls, value):
#         """
#         Flexible parser:
#         Accepts:
#         - '2025-02-01 14:30'
#         - '2025/02/01 14:30'
#         - '2025-02-01T14:30'
#         - and anything dateutil can parse
#         """
#         try:
#             return parser.parse(value)
#         except Exception:
#             raise ValueError("Invalid deadline format. Provide a valid datetime.")
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from dateutil import parser

VALID_STATUSES = ("todo", "doing", "done")


class TaskCreate(BaseModel):
    """
    Schema for creating a new task within a project.

    Includes validation for title/description length,
    flexible datetime parsing for the deadline,
    and strict status choices.
    """

    title: str = Field(
        ...,
        title="Task Title",
        description="Short descriptive name (1–30 characters).",
        min_length=1,
        max_length=30,
        example="Train Model on Dataset A"
    )

    description: str = Field(
        ...,
        title="Task Description",
        description="Detailed description (1–150 characters).",
        min_length=1,
        max_length=150,
        example="Run experiments on the new convolutional architecture."
    )

    status: Optional[str] = Field(
        default="todo",
        title="Task Status",
        description="One of: todo, doing, done.",
        example="todo"
    )

    deadline: datetime = Field(
        ...,
        title="Deadline",
        description="Deadline as a datetime string or object.",
        example="2025-02-01T14:30:00"
    )

    # ------------------------------
    # VALIDATORS
    # ------------------------------
    @field_validator("status")
    def validate_status(cls, value: Optional[str]) -> str:
        """Allow lowercase flexible status validation."""
        if value is None:
            return "todo"
        value = value.lower().strip()
        if value not in VALID_STATUSES:
            raise ValueError(f"Status must be one of: {VALID_STATUSES}")
        return value

    @field_validator("deadline", mode="before")
    def parse_deadline(cls, value):
        """Parse flexible datetimes like '2025-02-01 14:30' or ISO strings."""
        if isinstance(value, datetime):
            return value
        try:
            return parser.parse(value)
        except Exception:
            raise ValueError("Invalid deadline format. Provide a valid datetime.")

    # ------------------------------
    # MODEL CONFIGURATION
    # ------------------------------
    model_config = ConfigDict(
        str_strip_whitespace=True,   # trims whitespace from strings
        extra="forbid",              # prevents unknown fields
        json_schema_extra={
            "example": {
                "title": "Train model on dataset A",
                "description": "Run experiments on new CNN architecture.",
                "status": "doing",
                "deadline": "2025-02-01T14:30:00"
            }
        }
    )

