from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from typing import List
from src.books.book_data import books
from src.books.schemas import BookListingSerializer, BookUpdateSerializer


# create a router
book_router = APIRouter()



# get all the books
@book_router.get('', response_model=List[BookListingSerializer],
         status_code=status.HTTP_200_OK)
async def get_all_books() -> List:
    return books


# get the book by ID
@book_router.get('/{book_id}', response_model=BookListingSerializer,
         status_code=status.HTTP_200_OK)
async def get_book(book_id: int) -> BookListingSerializer:
    for book in books:
        if book['id'] == book_id:
            return book

    raise HTTPException(detail='Item not found', status_code=status.HTTP_404_NOT_FOUND)


# add a book to the list
@book_router.post('', status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookListingSerializer) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book


# update a book
@book_router.patch('/{book_id}', response_model=BookListingSerializer, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book_data: BookUpdateSerializer) -> dict:
    for book in books:
        if book['id'] == book_id:
            book['title'] = book_data.title
            book['author'] = book_data.author
            book['publisher'] = book_data.publisher
            book['page_count'] = book_data.page_count
            book['language'] = book_data.language

            return book

    raise HTTPException(detail='Book not found', status_code=status.HTTP_404_NOT_FOUND)


# delete a book
@book_router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int) -> None:
    for book in books:
        if book['id'] == book_id:
            books.remove(book)

            return {}

    raise HTTPException(detail='Book not found', status_code=status.HTTP_404_NOT_FOUND)
