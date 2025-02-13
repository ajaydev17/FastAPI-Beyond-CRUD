import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from src.books.schemas import BookViewSchema


class UserViewSchema(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool
    password_hash: str = Field(exclude=True)
    created_at: datetime
    updated_at: datetime


class UserBookViewSchema(UserViewSchema):
    books: List[BookViewSchema]

class UserCreateSchema(BaseModel):
    username: str = Field(max_length=20)
    email: str = Field(max_length=40)
    first_name: str = Field(max_length=25)
    last_name: str = Field(max_length=25)
    password: str = Field(min_length=8)


class UserLoginSchema(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=8)