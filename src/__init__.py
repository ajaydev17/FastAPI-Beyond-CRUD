from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.reviews.routes import review_router
from contextlib import asynccontextmanager
from src.db.main import init_db


# this gonna run as the first thing when the server starts
@asynccontextmanager
async def init_app(app: FastAPI):
    print("Server is starting...")
    # initialize the database
    await init_db()
    # yield the app
    yield
    print("Server has been stopped...")


version = 'v1'

# create the fastapi server
app = FastAPI(
    version=version,
    title='Bookly',
    description='A REST API for book review web service'
)


# include the router in the app
app.include_router(
    book_router,
    prefix=f'/api/{version}/books',
    tags=['Books']
)
app.include_router(
    auth_router,
    prefix=f'/api/{version}/auth',
    tags=['auth']
)
app.include_router(
    review_router,
    prefix=f'/api/{version}/reviews',
    tags=['Reviews']
)
