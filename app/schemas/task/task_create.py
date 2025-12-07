from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from dateutil import parser

VALID_STATUSES = ("todo", "doing", "done")


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=200)
    status: Optional[str] = "todo"
    deadline: datetime

    # ------------------------------
    # STATUS VALIDATOR
    # ------------------------------
    @field_validator("status")
    def validate_status(cls, value):
        if value is None:
            return "todo"
        value = value.lower().strip()
        if value not in VALID_STATUSES:
            raise ValueError(f"Status must be one of: {VALID_STATUSES}")
        return value

    # ------------------------------
    # DEADLINE FLEXIBLE PARSER
    # ------------------------------
    @field_validator("deadline", mode="before")
    def parse_deadline(cls, value):
        """
        Flexible parser:
        Accepts:
        - '2025-02-01 14:30'
        - '2025/02/01 14:30'
        - '2025-02-01T14:30'
        - and anything dateutil can parse
        """
        try:
            return parser.parse(value)
        except Exception:
            raise ValueError("Invalid deadline format. Provide a valid datetime.")

