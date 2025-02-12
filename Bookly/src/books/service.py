from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import BookCreateSchema, BookUpdateSchema
from sqlmodel import select, desc
from .models import Book
from datetime import datetime


class BookService:

    async def get_all_books(self, session: AsyncSession):
        statement = select(Book).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_books_by_user(self, user_uid: str, session: AsyncSession):
        statement = select(Book).where(
            Book.user_uid == user_uid).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_book(self, book_uid: str, session: AsyncSession):
        statement = select(Book).where(Book.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()

        return book if book else None

    async def create_book(self,
                          book_data: BookCreateSchema,
                          user_uid: str,
                          session: AsyncSession):
        book_data_dict = book_data.model_dump()
        book = Book(**book_data_dict)
        book.published_date = datetime.strptime(
            book_data_dict['published_date'],
            "%Y-%m-%d")
        book.user_uid = user_uid
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def update_book(
        self, book_uid: str, book_data: BookUpdateSchema, session: AsyncSession
    ):
        book = await self.get_book(book_uid, session)

        if not book:
            return None

        book_data_dict = book_data.model_dump()
        for key, value in book_data_dict.items():
            setattr(book, key, value)

        await session.commit()
        await session.refresh(book)
        return book

    async def delete_book(self, book_uid: str, session: AsyncSession):
        book = await self.get_book(book_uid, session)

        if not book:
            return None

        await session.delete(book)
        await session.commit()
        return book
