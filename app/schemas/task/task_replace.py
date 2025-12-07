from pydantic import BaseModel, field_validator
from typing import Optional
from dateutil import parser

class TaskReplace(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    deadline: Optional[str] = None

    @field_validator("title")
    def validate_title(cls, value):
        if value is None:
            return None
        value = value.strip()
        if not (3 <= len(value) <= 50):
            raise ValueError("Title must be 3–50 characters.")
        return value

    @field_validator("description")
    def validate_description(cls, value):
        if value is None:
            return None
        value = value.strip()
        if not (3 <= len(value) <= 200):
            raise ValueError("Description must be 3–200 characters.")
        return value

    @field_validator("status")
    def validate_status(cls, value):
        if value is None:
            return None
        value = value.lower().strip()
        if value not in ("todo", "doing", "done"):
            raise ValueError("Status must be: todo, doing, done.")
        return value

    @field_validator("deadline")
    def validate_deadline(cls, value):
        if value is None:
            return None
        try:
            return parser.parse(value)
        except Exception:
            raise ValueError("Invalid deadline format.")
