from fastapi import FASTAPI

# create the fastapi app
app = FASTAPI()


# define the roots
@app.get('/')
async def read_root():
    return {"message": "Hello World"}
