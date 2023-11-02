from datetime import datetime, date
from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    name: str = Field(max_length=100)
    surname: str = Field(max_length=100)
    email: str = Field(max_length=100)
    phone: str = Field(max_length=100)
    birthday: date = Field()
    description: str = Field(max_length=150)

class ContactResponse(ContactModel):
    id: int

    class Config:
        # orm_mode = True
        from_attributes=True

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        # orm_mode = True
        from_attributes=True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr