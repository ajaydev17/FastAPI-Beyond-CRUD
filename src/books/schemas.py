from pydantic import BaseModel
from datetime import datetime, date
import uuid
from typing import List
from src.reviews.schemas import ReviewViewSchema


# create a schema for book model
class BookViewSchema(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime


class BookReviewViewSchema(BookViewSchema):
    reviews: List[ReviewViewSchema]


class BookCreateSchema(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateSchema(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
