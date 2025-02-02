from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import List


# create a schema for book listing
class BookListingSerializer(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateSerializer(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

# create the fastapi instance
app = FastAPI()


# book list as in memory data
books = [
  {
    "id": 1,
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "publisher": "Prentice Hall",
    "published_date": "2008-08-01",
    "page_count": 464,
    "language": "English"
  },
  {
    "id": 2,
    "title": "The Pragmatic Programmer",
    "author": "Andrew Hunt, David Thomas",
    "publisher": "Addison-Wesley",
    "published_date": "1999-10-20",
    "page_count": 352,
    "language": "English"
  },
  {
    "id": 3,
    "title": "Introduction to the Theory of Computation",
    "author": "Michael Sipser",
    "publisher": "Cengage Learning",
    "published_date": "2012-06-27",
    "page_count": 504,
    "language": "English"
  },
  {
    "id": 4,
    "title": "Design Patterns: Elements of Reusable Object-Oriented Software",
    "author": "Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides",
    "publisher": "Addison-Wesley",
    "published_date": "1994-10-21",
    "page_count": 416,
    "language": "English"
  },
  {
    "id": 5,
    "title": "You Don't Know JS: Scope & Closures",
    "author": "Kyle Simpson",
    "publisher": "O'Reilly Media",
    "published_date": "2014-03-14",
    "page_count": 98,
    "language": "English"
  },
  {
    "id": 6,
    "title": "Python Crash Course",
    "author": "Eric Matthes",
    "publisher": "No Starch Press",
    "published_date": "2015-11-01",
    "page_count": 560,
    "language": "English"
  },
  {
    "id": 7,
    "title": "Fluent Python",
    "author": "Luciano Ramalho",
    "publisher": "O'Reilly Media",
    "published_date": "2015-07-30",
    "page_count": 792,
    "language": "English"
  },
  {
    "id": 8,
    "title": "JavaScript: The Good Parts",
    "author": "Douglas Crockford",
    "publisher": "O'Reilly Media",
    "published_date": "2008-05-01",
    "page_count": 176,
    "language": "English"
  },
  {
    "id": 9,
    "title": "Effective Java",
    "author": "Joshua Bloch",
    "publisher": "Addison-Wesley",
    "published_date": "2017-12-27",
    "page_count": 416,
    "language": "English"
  },
  {
    "id": 10,
    "title": "Structure and Interpretation of Computer Programs",
    "author": "Harold Abelson, Gerald Jay Sussman",
    "publisher": "MIT Press",
    "published_date": "1996-07-25",
    "page_count": 657,
    "language": "English"
  }
]


# get all the books
@app.get('/books', response_model=List[BookListingSerializer], 
         status_code=status.HTTP_200_OK)
async def get_all_books() -> List:
    return books


# get the book by ID
@app.get('/books/{book_id}', response_model=BookListingSerializer, 
         status_code=status.HTTP_200_OK)
async def get_book(book_id: int) -> BookListingSerializer:
    for book in books:
        if book['id'] == book_id:
            return book

    raise HTTPException(detail='Item not found', status_code=status.HTTP_404_NOT_FOUND)


# add a book to the list
@app.post('/books', status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookListingSerializer) -> dict:
    new_book = book_data.model_dump()
    books.append(new_book)
    return new_book


# update a book
@app.patch('/books/{book_id}', response_model=BookListingSerializer, status_code=status.HTTP_200_OK)
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
@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int) -> None:
    for book in books:
        if book['id'] == book_id:
            books.remove(book)

            return {}

    raise HTTPException(detail='Book not found', status_code=status.HTTP_404_NOT_FOUND)
