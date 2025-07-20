from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str
    status_code: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
