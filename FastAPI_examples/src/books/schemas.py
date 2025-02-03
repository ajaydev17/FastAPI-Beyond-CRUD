from pydantic import BaseModel


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
