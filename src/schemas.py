from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserModel(BaseModel):
    username: str = Field(min_length=4, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=20)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ContactModel(BaseModel):
    firstname: str
    lastname: str = Field(min_length=2)
    birthday: datetime
    phone: str
    email: EmailStr
    notes: str = Field('')


class ContactResponse(BaseModel):
    id: int
    firstname: str
    lastname: str = Field(min_length=2)
    birthday: datetime
    phone: str
    email: EmailStr
    notes: str
    days_to_next_birthday: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True



