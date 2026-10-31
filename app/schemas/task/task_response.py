# # app/schemas/task/task_response.py

# from datetime import datetime
# from pydantic import BaseModel, Field, ConfigDict


# class TaskResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)

#     id: int
#     title: str
#     description: str
#     status: str
#     deadline: datetime | None = Field(None)
#     project_id: int
#     created_at: datetime
#     updated_at: datetime
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TaskResponse(BaseModel):
    """
    Schema for returning task details in API responses.

    This model represents the complete task entity,
    including metadata and project reference.
    """

    id: int = Field(
        ...,
        title="Task ID",
        description="Unique identifier of the task.",
        example=12
    )

    title: str = Field(
        ...,
        title="Task Title",
        description="Short descriptive title for the task.",
        example="Train neural network"
    )

    description: str = Field(
        ...,
        title="Task Description",
        description="Detailed explanation of what the task is about.",
        example="Optimize the CNN training pipeline and report accuracy."
    )

    status: str = Field(
        ...,
        title="Status",
        description="Current status of the task (todo, doing, done).",
        example="doing"
    )

    deadline: datetime | None = Field(
        None,
        title="Deadline",
        description="Deadline for completing the task (optional).",
        example="2025-07-20T18:00:00"
    )

    project_id: int = Field(
        ...,
        title="Project ID",
        description="Identifier for the project this task belongs to.",
        example=3
    )

    created_at: datetime = Field(
        ...,
        title="Creation Timestamp",
        description="Datetime when the task was created.",
        example="2025-06-11T14:22:00"
    )

    updated_at: datetime = Field(
        ...,
        title="Last Update Timestamp",
        description="Datetime when the task was last updated.",
        example="2025-06-11T16:45:00"
    )

    # ---------------------------
    # MODEL CONFIGURATION
    # ---------------------------
    model_config = ConfigDict(
        from_attributes=True,       # allows ORM → model conversion
        json_schema_extra={
            "example": {
                "id": 12,
                "title": "Train CNN model",
                "description": "Perform training phase using augmented dataset.",
                "status": "doing",
                "deadline": "2025-07-20T18:00:00",
                "project_id": 3,
                "created_at": "2025-06-11T14:22:00",
                "updated_at": "2025-06-11T16:45:00"
            }
        }
    )
