from fastapi import FastAPI


app = FastAPI()


#http://127.0.0.1:8000/items/?skip=20&limit=30


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}