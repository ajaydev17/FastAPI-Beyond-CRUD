from fastapi import FastAPI
from src.books.routes import book_router


version = 'v1'

# create the fastapi server
app = FastAPI(
        version=version,
        title='Bookly',
        description='A REST API for book review web service'
    )



# include the router in the app
app.include_router(book_router, prefix=f'/api/{version}/books')
