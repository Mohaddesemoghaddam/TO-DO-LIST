# from pydantic import BaseModel, Field, validator

# class ProjectReplace(BaseModel):
#     name: str | None = Field(None, min_length=3, max_length=50)
#     description: str | None = Field(None, max_length=255)

#     @validator("name")
#     def no_special_chars(cls, v):
#         if v is None:
#             return v
#         forbidden = [",", "/", "\\"]
#         if any(c in v for c in forbidden):
#             raise ValueError("Project name cannot contain ',', '/', '\\'")
#         return v
from pydantic import BaseModel, Field, field_validator

class ProjectReplace(BaseModel):
    """
    Schema for fully replacing (PUT) an existing project.
    
    All fields are optional, allowing selective updates,
    but when provided, they must follow validation rules.
    """

    name: str | None = Field(
        None,
        title="Project Name",
        description="Updated project name (3–50 characters). Special characters ',', '/', '\\' are not allowed.",
        min_length=3,
        max_length=50,
        example="Deep Learning Journal"
    )

    description: str | None = Field(
        None,
        title="Project Description",
        description="Updated project description (up to 255 characters).",
        max_length=255,
        example="An ongoing log of model experiments and analyses."
    )

    # ---------------------------
    # Field-Level Validation
    # ---------------------------
    @field_validator("name")
    def validate_name(cls, v: str | None) -> str | None:
        """
        Remove or reject forbidden special characters in the project's name.
        """
        if v is None:
            return v

        forbidden_chars = {",", "/", "\\"}
        if any(char in v for char in forbidden_chars):
            raise ValueError(f"Project name cannot contain any of: {forbidden_chars}")
        return v

    # ---------------------------
    # Example Configuration for Swagger
    # ---------------------------
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Neural Forecasting App",
                "description": "Rebuilding the ML model repository with improved data sources."
            }
        }
