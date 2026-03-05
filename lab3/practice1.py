from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
app = FastAPI()

# Mock database of books
books = [
    {"id": 1, "title": "1984", "author": "George Orwell", "year": 1949},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925}
]


# TODO: Define a Pydantic model for the book
# Include:
# - title
# - author
# - year
class BookInfo(BaseModel):
    title: str
    author: str
    year: int

# TODO: Define a GET endpoint receiving the id and use the response model
# Use the URL: /books/{book_id}
    # Finding the book in books
    
    
@app.get( "/book/{book_id}", response_model= BookInfo)
async def read_book_info(book_id : int):
    for book in books:
        if book["id"] == book_id:
            return book