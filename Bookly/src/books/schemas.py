from pydantic import BaseModel
from datetime import datetime, date
import uuid


# create a schema for book model
class BookView(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime


class BookCreate(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdate(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
