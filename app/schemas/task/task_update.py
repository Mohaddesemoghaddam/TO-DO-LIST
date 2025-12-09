# from pydantic import BaseModel, field_validator
# from typing import Optional
# from dateutil import parser

# class TaskUpdate(BaseModel):
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
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from dateutil import parser

VALID_STATUSES = ("todo", "doing", "done")


class TaskUpdate(BaseModel):
    """
    Schema for updating (partially) an existing Task.

    All fields are optional. Each provided field is validated
    and normalized (spaces trimmed, lowercase for status, etc.).
    """

    title: Optional[str] = Field(
        None,
        title="Task Title",
        description="New title for the task (3–50 characters).",
        example="Update API documentation"
    )

    description: Optional[str] = Field(
        None,
        title="Task Description",
        description="New detailed description (3–200 characters).",
        example="Ensure all endpoints include proper 200/400/404 examples."
    )

    status: Optional[str] = Field(
        None,
        title="Task Status",
        description="New status for the task — must be one of: todo, doing, done.",
        example="doing"
    )

    deadline: Optional[str] = Field(
        None,
        title="Deadline",
        description="New deadline in a valid date/time format (e.g. '2025-07-22').",
        example="2025-07-22"
    )

    # ------------------------------
    # VALIDATORS
    # ------------------------------
    @field_validator("title")
    def validate_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = value.strip()
        if not (3 <= len(value) <= 50):
            raise ValueError("Title must be between 3 and 50 characters long.")
        return value

    @field_validator("description")
    def validate_description(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = value.strip()
        if not (3 <= len(value) <= 200):
            raise ValueError("Description must be between 3 and 200 characters long.")
        return value

    @field_validator("status")
    def validate_status(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        value = value.lower().strip()
        if value not in VALID_STATUSES:
            raise ValueError(f"Invalid status. Choose one of: {', '.join(VALID_STATUSES)}.")
        return value

    @field_validator("deadline")
    def validate_deadline(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return None
        try:
            return parser.parse(value)
        except Exception:
            raise ValueError("Invalid format for deadline. Use a valid date string (e.g. '2025-07-22').")

    # ------------------------------
    # CONFIGURATION
    # ------------------------------
    model_config = ConfigDict(
        str_strip_whitespace=True,  # trim whitespace globally
        extra="forbid",             # reject extra/unknown fields
        json_schema_extra={
            "example": {
                "title": "Refactor Task API",
                "description": "Add unified error handling and update Swagger docs.",
                "status": "doing",
                "deadline": "2025-07-22"
            }
        },
    )
