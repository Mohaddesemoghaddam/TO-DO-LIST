from pydantic import BaseModel
from typing import Optional


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True
