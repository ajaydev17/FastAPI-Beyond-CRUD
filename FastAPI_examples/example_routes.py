from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel

# create the fastapi app
app = FastAPI()


class BookSerializer(BaseModel):
    title: str
    author: str


# define the roots
@app.get('/')
async def read_root() -> dict:
    return {"message": "Hello World"}


# route to access the value in the url
@app.get('/greet/{name}')
async def greet_user(name: str) -> dict:
    return {"message": f"Hello!, {name}"}


# query parameter example
@app.get('/greetUser')
async def greet_query_parameter_user(user: str) -> dict:
    return {"message": f"Hello!, {user}"}


# default query parameter example
@app.get('/greetDefaultUser')
async def greet_query_parameter_user(user: Optional[str]= 'user', age: int= 0) -> dict:
    return {"message": f"Hello!, {user}", "age": age}


# create a book post request
@app.post('/createBook')
async def create_book(book_data: BookSerializer) -> dict:
    return {
        "title": book_data.title,
        "author": book_data.author
    }


# get header request
@app.get('/getHeaders')
async def get_headers(
    accept: str= Header(None),
    content_type: str= Header(None),
    user_agent: str= Header(None),
    host: str= Header(None)
    ) -> dict:
    request_headers = {}

    request_headers['Accept'] = accept
    request_headers['Content-Type'] = content_type
    request_headers['User-Agent']= user_agent
    request_headers['Host']= host

    return request_headers

