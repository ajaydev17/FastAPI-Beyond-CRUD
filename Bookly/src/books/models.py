from sqlmodel import Field, SQLModel, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date
import uuid
from typing import Optional
from src.auth.models import User


class Book(SQLModel, table=True):

    # table name in the database
    __tablename__ = "books"

    # define the columns of the table

    # creating an id field as postgresql UUID
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            nullable=False
        )
    )

    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key='users.uid'
    )
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            default=datetime.now
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            default=datetime.now,
            onupdate=datetime.now
        )
    )
    user: Optional[User] = Relationship(back_populates="books")

    def __repr__(self):
        return f"<Book: {self.title}>"
