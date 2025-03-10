from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import datetime, date
import uuid
import sqlalchemy.dialects.postgresql as pg
from typing import List, Optional


class User(SQLModel, table=True):

    __tablename__ = "users"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            nullable=False
        )
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(
        sa_column=Column(
            pg.VARCHAR,
            nullable=False,
            server_default='user'
        )
    )
    is_verified: bool = Field(default=False)
    password_hash: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False),
        exclude=True)
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
    books: List['Book'] = Relationship(
        back_populates='user', sa_relationship_kwargs={'lazy': 'selectin'}
    )
    reviews: List['Review'] = Relationship(
        back_populates='user', sa_relationship_kwargs={'lazy': 'selectin'}
    )

    def __repr__(self):
        return f"<User: {self.username}>"


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
    reviews: List['Review'] = Relationship(
        back_populates='book', sa_relationship_kwargs={'lazy': 'selectin'}
    )

    def __repr__(self):
        return f"<Book: {self.title}>"
    

class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            default=uuid.uuid4,
            nullable=False
        )
    )
    rating: int = Field(lt=5)
    review_text: str
    user_uid: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key='users.uid'
    )
    book_uid: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key='books.uid'
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
    user: Optional[User] = Relationship(back_populates="reviews")
    book: Optional[Book] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for {self.book_uid} by user {self.user_uid}>"