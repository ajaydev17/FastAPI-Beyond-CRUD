from pydantic import BaseModel, Field
import uuid
from typing import Optional
from datetime import datetime


class ReviewViewSchema(BaseModel):
    uid: uuid.UUID
    rating: int
    review_text: str
    user_uid: Optional[uuid.UUID]
    book_uid: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime


class ReviewCreateSchema(BaseModel):
    rating: int = Field(lt=5)
    review_text: str