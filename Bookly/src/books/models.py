from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid


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
    published_date: str
    page_count: int
    language: str
    created_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            default_factory=datetime.now
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            default_factory=datetime.now,
            onupdate=datetime.now
        )
    )

    def __repr__(self):
        return f"<Book: {self.title}>"
