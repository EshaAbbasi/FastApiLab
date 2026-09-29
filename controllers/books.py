from fastapi import APIRouter, Depends, HTTPException

# Models
from models.book import BookModel

# Serializers & Validations
from serializers.book import BookSchema, CreateBookSchema, UpdateBookSchema
from serializers.user import UserSchema
from typing import List

# DB
from sqlalchemy.orm import Session
from database import get_db

# Dependencies
from dependencies.get_current_user import get_current_user


router = APIRouter()

@router.get('/books',response_model=List[BookSchema])
def get_books(db: Session =Depends(get_db)):
    books=db.query(BookModel).all()
    return books
@router.get("/books/{book_id}", response_model=BookSchema)
def get_single_book(book_id: int, db: Session = Depends(get_db)):
  book = db.query(BookModel).filter(BookModel.id == book_id).first()

  if not book:
    raise HTTPException(status_code=404, detail="Cannot find Book")

  return book


@router.post("/books", response_model=BookSchema, status_code=201)
def create_book(
  book: CreateBookSchema,
  db: Session = Depends(get_db),
  current_user: UserSchema = Depends(get_current_user),
):
    new_book = BookModel(**book.dict(),user_id=current_user.id)# Convert Pydantic model to SQLAlchemy model
    db.add(new_book)
    db.commit() # basicallt model.save()
    db.refresh(new_book)

    return new_book

@router.put("/books/{book_id}", response_model=BookSchema)
def update_book(
   book_id: int,
   book: UpdateBookSchema,
   db: Session = Depends(get_db),
   user: UserSchema = Depends(get_current_user)
   ):

    # Find the tea to updates
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()

    # If tea was not found, raise an error
    if not db_book.user_id != current_user.id:
      raise HTTPException(status_code=404, detail="book not found")

    book_data = book.dict(exclude_unset=True)

    # loop thru the dict and replace the value for the key
    for key, value in book_data.items():
       setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)

    return db_book

@router.delete("/books/{book_id}", status_code=204)
def delete_book(
   book_id: int,
   db: Session = Depends(get_db),
   user: UserSchema = Depends(get_current_user)
  ):
    # Delete a tea by ID
    book = db.query(BookModel).filter(BookModel.id == book_id).first()

    # If tea was not found, raise an error
    if not book:
      raise HTTPException(status_code=404, detail="Book not found")
      # Check if the current user is the creator of the tea
    if book.user_id != user.id:
        raise HTTPException(status_code=403, detail="Operation forbidden")
    db.delete(tea)
    db.commit()

    return None
    