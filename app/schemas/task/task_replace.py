# from pydantic import BaseModel, field_validator
# from typing import Optional
# from dateutil import parser

# class TaskReplace(BaseModel):
#     title: Optional[str] = None
#     description: Optional[str] = None
#     status: Optional[str] = None
#     deadline: Optional[str] = None

#     @field_validator("title")
#     def validate_title(cls, value):
#         if value is None:
#             return None
#         value = value.strip()
#         if not (3 <= len(value) <= 50):
#             raise ValueError("Title must be 3–50 characters.")
#         return value

#     @field_validator("description")
#     def validate_description(cls, value):
#         if value is None:
#             return None
#         value = value.strip()
#         if not (3 <= len(value) <= 200):
#             raise ValueError("Description must be 3–200 characters.")
#         return value

#     @field_validator("status")
#     def validate_status(cls, value):
#         if value is None:
#             return None
#         value = value.lower().strip()
#         if value not in ("todo", "doing", "done"):
#             raise ValueError("Status must be: todo, doing, done.")
#         return value

#     @field_validator("deadline")
#     def validate_deadline(cls, value):
#         if value is None:
#             return None
#         try:
#             return parser.parse(value)
#         except Exception:
#             raise ValueError("Invalid deadline format.")
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from dateutil import parser


VALID_STATUSES = ("todo", "doing", "done")


class TaskReplace(BaseModel):
    """
    Schema for fully replacing an existing task (used in PUT requests).

    All fields are optional but expected to provide full new values when used.
    Includes strong validation for length, status, and flexible date parsing.
    """

    title: Optional[str] = Field(
        None,
        title="Task Title",
        description="Optional title for the task. Must be between 3 and 50 characters.",
        min_length=3,
        max_length=50,
        example="Data preprocessing"
    )

    description: Optional[str] = Field(
        None,
        title="Task Description",
        description="Optional description. Must be between 3 and 200 characters.",
        min_length=3,
        max_length=200,
        example="Clean and prepare raw data before training."
    )

    status: Optional[str] = Field(
        None,
        title="Task Status",
        description="Optional task status; must be one of (todo, doing, done).",
        example="doing"
    )

    deadline: Optional[datetime] = Field(
        None,
        title="Deadline",
        description="Task deadline. Accepts flexible date formats like 'YYYY-MM-DD HH:MM'.",
        example="2025-05-20T14:30:00"
    )

    # ------------------------------
    # VALIDATORS
    # ------------------------------
    @field_validator("title")
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        """Ensure title length and trimming."""
        if value is None:
            return value
        value = value.strip()
        if not (3 <= len(value) <= 50):
            raise ValueError("Title must be between 3 and 50 characters.")
        return value

    @field_validator("description")
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        """Ensure description length and trimming."""
        if value is None:
            return value
        value = value.strip()
        if not (3 <= len(value) <= 200):
            raise ValueError("Description must be between 3 and 200 characters.")
        return value

    @field_validator("status")
    def validate_status(cls, value: Optional[str]) -> Optional[str]:
        """Validate that status belongs to the defined set."""
        if value is None:
            return value
        value = value.lower().strip()
        if value not in VALID_STATUSES:
            raise ValueError(f"Status must be one of: {VALID_STATUSES}.")
        return value

    @field_validator("deadline", mode="before")
    def parse_deadline(cls, value):
        """Flexibly parse a datetime string or object into a Python datetime."""
        if value is None or isinstance(value, datetime):
            return value
        try:
            return parser.parse(value)
        except Exception:
            raise ValueError("Invalid deadline format. Expected something like '2025-05-20T14:30:00'.")

    # ------------------------------
    # MODEL CONFIGURATION
    # ------------------------------
    model_config = ConfigDict(
        str_strip_whitespace=True,  # clean input strings
        extra="forbid",             # block unexpected fields
        json_schema_extra={
            "example": {
                "title": "Train transformer model",
                "description": "Fine-tune transformer architecture on clinical dataset.",
                "status": "doing",
                "deadline": "2025-06-10T18:00:00"
            }
        }
    )
