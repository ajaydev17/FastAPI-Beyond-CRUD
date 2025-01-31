from fastapi import FastAPI

# create the fastapi app
app = FastAPI()


# define the roots
@app.get('/')
async def read_root():
    return {"message": "Hello World"}


# route to access the value in the url
@app.get('/greet/{name}')
async def greet_user(name: str):
    return {"message": f"Hello!, {name}"}
