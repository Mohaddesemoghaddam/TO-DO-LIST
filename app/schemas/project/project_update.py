from pydantic import BaseModel, Field, validator

class ProjectUpdate(BaseModel):
    new_name: str | None = Field(None, min_length=3, max_length=50)
    new_description: str | None = Field(None, max_length=255)

    @validator("new_name")
    def no_special_chars(cls, v):
        if v is None:
            return v
        forbidden = [",", "/", "\\"]
        if any(c in v for c in forbidden):
            raise ValueError("Project name cannot contain ',', '/', '\\'")
        return v

