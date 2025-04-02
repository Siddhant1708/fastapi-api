from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()

class Book(BaseModel):
    id : UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=30)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=10)

Books = []

@app.get('/')
def read_api():
    return Books

@app.put('/')
def create_book(book: Book):
    Books.append(book)
    return Books[-1]

@app.put('/{book_id}')
def update_books(book_id:UUID,book: Book):
    for i in range(len(Books)):
        if book_id == Books[i].id:
            Books[i]=book
            return Books[i]  

    ## Raising an error if we don't get the book in the Books
    raise HTTPException(
        status_code= 404,
        detail= f"ID {book_id}: Does not exist in the Database"
    ) 

@app.delete('/{book_id}')
def delete_book(book_id: UUID):     
    for i in range(len(Books)):
        if book_id == Books[i].id:
            del Books[i]
            return f'Book with ID {book_id} is deleted'

    raise HTTPException(
        status_code = 404,
        detail = f"ID {book_id}: Does not exist in the Database"
    )    
