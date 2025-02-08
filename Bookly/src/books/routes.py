from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from typing import List
from src.books.schemas import BookView, BookCreate, BookUpdate
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.service import BookService


# create a router
book_router = APIRouter()

# create an instance of the BookService
book_service = BookService()


# get all the books
@book_router.get('', response_model=List[BookView],
                 status_code=status.HTTP_200_OK)
async def get_all_books(session: AsyncSession = Depends(get_session)) -> List:
    books = await book_service.get_all_books(session)
    return books


# get the book by ID
@book_router.get('/{book_uid}', response_model=BookView,
                 status_code=status.HTTP_200_OK)
async def get_book(book_uid: str,
                   session: AsyncSession = Depends(get_session)) -> BookView:
    book = await book_service.get_book(book_uid, session)

    if book:
        return book
    else:
        raise HTTPException(detail='Item not found',
                            status_code=status.HTTP_404_NOT_FOUND)


# add a book to the list
@book_router.post('',
                  response_model=BookView,
                  status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookCreate,
                      session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.create_book(book_data, session)
    return book


# update a book
@book_router.patch('/{book_uid}',
                   response_model=BookView,
                   status_code=status.HTTP_200_OK)
async def update_book(book_uid: str, book_data: BookUpdate,
                      session: AsyncSession = Depends(get_session)) -> dict:
    book = await book_service.update_book(book_uid, book_data, session)

    if book:
        return book
    else:
        raise HTTPException(detail='Book not found',
                            status_code=status.HTTP_404_NOT_FOUND)


# delete a book
@book_router.delete('/{book_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid: str,
                      session: AsyncSession = Depends(get_session)) -> None:
    book = await book_service.delete_book(book_uid, session)

    if not book:
        raise HTTPException(detail='Book not found',
                            status_code=status.HTTP_404_NOT_FOUND)
    else:
        return None
