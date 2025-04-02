from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

#when this gets run, it will create a Database or Table if it does not already exist
models.Base.metadata.create_all(bind=engine)


#what this do is, it creates sessionLocal instance or we can say DB instance
#and we are also going to be closing the instance  
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()    


class Book(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=30)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=10)

Books = []

@app.get('/')
def read_api(db : Session = Depends(get_db)):
    return db.query(models.Books).all()

@app.put('/')
def create_book(book : Book, db: Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title = book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.rating = book.rating

    db.add(book_model)
    db.commit()

    return book

@app.put('/{book_id}')
def update_books(book_id : int, book : Book, db : Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    ## Raising an error if we don't get the book with id = book_id in db
    if book_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"ID {book_id}: Does not exist in the Database"
        )
    else:
        book_model.title = book.title
        book_model.author = book.author
        book_model.description = book.description
        book_model.rating = book.rating
        
        db.add(book_model)
        db.commit()
        return book


@app.delete('/{book_id}')
def delete_book(book_id: int, db : Session = Depends(get_db)):     
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

    if book_model is None:
        raise HTTPException(
            status_code = 404,
            detail = f"ID {book_id}: Does not exist in the Database"
        )
    else:
        db.query(models.Books).filter(models.Books.id == book_id).delete()
        db.commit()    
