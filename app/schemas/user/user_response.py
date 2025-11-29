from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: EmailStr

    class Config:
        orm_mode = True
