from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ContactModel(BaseModel):
    name: str = Field(max_length=100)
    surname: str = Field(max_length=100)
    email: str = Field(max_length=100)
    phone: str = Field(max_length=100)
    birthday: datetime = Field()
    description: str = Field(max_length=150)

class ContactResponse(ContactModel):
    id: int

    class Config:
        orm_mode = True