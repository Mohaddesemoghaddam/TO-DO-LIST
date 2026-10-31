# from pydantic import BaseModel, Field, validator

# class ProjectCreate(BaseModel):
#     name: str = Field(..., min_length=3, max_length=50)
#     description: str | None = Field(None, max_length=255)

#     @validator("name")
#     def no_special_chars(cls, v):
#         forbidden = [",", "/", "\\"]
#         if any(c in v for c in forbidden):
#             raise ValueError("Project name cannot contain ',', '/', '\\'")
#         return v
from pydantic import BaseModel, Field, field_validator

class ProjectCreate(BaseModel):
    """
    Schema for creating a new Project.
    
    Includes validation for name length, allowed characters, 
    and optional description length.
    """
    
    name: str = Field(
        ...,
        title="Project Name",
        description="Unique name of the project (3–50 characters). Special characters ',', '/', '\\' are not allowed.",
        min_length=3,
        max_length=50,
        example="AI Research Plan"
    )
    
    description: str | None = Field(
        None,
        title="Project Description",
        description="Optional detailed description of the project (up to 255 characters).",
        max_length=255,
        example="A study on neural learning patterns."
    )

    # ---------------------------
    # Field-Level Validation
    # ---------------------------
    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        """
        Ensure that project name does not contain forbidden special characters.
        """
        forbidden_chars = {",", "/", "\\"}
        if any(char in v for char in forbidden_chars):
            raise ValueError(f"Project name cannot contain any of: {forbidden_chars}")
        return v

    # ---------------------------
    # Model Config (for Swagger)
    # ---------------------------
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Data Science Sprint",
                "description": "Weekly sprint focusing on data preprocessing and model experiments."
            }
        }

