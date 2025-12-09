# from pydantic import BaseModel, Field, validator

# class ProjectUpdate(BaseModel):
#     new_name: str | None = Field(None, min_length=3, max_length=50)
#     new_description: str | None = Field(None, max_length=255)

#     @validator("new_name")
#     def no_special_chars(cls, v):
#         if v is None:
#             return v
#         forbidden = [",", "/", "\\"]
#         if any(c in v for c in forbidden):
#             raise ValueError("Project name cannot contain ',', '/', '\\'")
#         return v
from pydantic import BaseModel, Field, ConfigDict, field_validator

class ProjectUpdate(BaseModel):
    """
    Schema used for partial updates to a project.

    All fields are optional — only provided values will be updated.
    Includes validation for naming conventions and field lengths.
    """

    new_name: str | None = Field(
        None,
        title="New Project Name",
        description="Optional new name for the project (3–50 characters).",
        min_length=3,
        max_length=50,
        example="AI Research Hub"
    )

    new_description: str | None = Field(
        None,
        title="New Project Description",
        description="Optional new description for the project (up to 255 characters).",
        max_length=255,
        example="This project focuses on developing machine learning tools for neuroscience data."
    )

    # ---------------------------
    # 🔍 Field-level validator (Pydantic v2)
    # ---------------------------
    @field_validator("new_name")
    def validate_name_chars(cls, value: str | None) -> str | None:
        """Ensure no special characters are used in project names."""
        if value is None:
            return value
        forbidden_chars = [",", "/", "\\"]
        if any(char in value for char in forbidden_chars):
            raise ValueError("Project name cannot contain ',', '/', '\\'.")
        return value

    # ---------------------------
    # ⚙️ Model configuration
    # ---------------------------
    model_config = ConfigDict(
        from_attributes=True,
        str_strip_whitespace=True,  # trims surrounding spaces
        extra="forbid",             # forbids unexpected input keys
        json_schema_extra={
            "example": {
                "new_name": "Deep Learning Toolkit",
                "new_description": "Toolkit for managing advanced neural network experiments."
            }
        }
    )

