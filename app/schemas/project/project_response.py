# from pydantic import BaseModel, ConfigDict

# class ProjectResponse(BaseModel):
#     id: int
#     name: str
#     description: str | None = None

#     model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel, ConfigDict, Field

class ProjectResponse(BaseModel):
    """
    Schema for returning project details in API responses.

    This model is configured to load data directly from ORM objects
    and represents the immutable view of Project entities.
    """

    id: int = Field(
        ...,
        title="Project ID",
        description="Unique identifier of the project.",
        example=1
    )

    name: str = Field(
        ...,
        title="Project Name",
        description="Name of the project (3–50 characters).",
        example="Machine Learning Lab"
    )

    description: str | None = Field(
        None,
        title="Project Description",
        description="Detailed optional description for the project.",
        example="A research unit focusing on developing deep neural architectures."
    )

    # ---------------------------
    # Model configuration
    # ---------------------------
    model_config = ConfigDict(
        from_attributes=True,   # allows ORM → model conversion
        json_schema_extra={     # examples for Swagger/Postman
            "example": {
                "id": 7,
                "name": "AI Healthcare Toolkit",
                "description": "Applied AI tools for medical data analytics."
            }
        }
    )
