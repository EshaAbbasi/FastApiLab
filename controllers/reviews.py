from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.book import BookModel
from models.review import ReviewModel
from models.user import UserModel
from dependencies.get_current_user import get_current_user
from serializers.review import (
    CreateReviewSchema,
    ReviewSchema,
    UpdateReviewSchema,
)

router = APIRouter()


@router.get("/reviews", response_model=list[ReviewSchema])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(ReviewModel).all()


@router.get("/books/{book_id}/reviews", response_model=list[ReviewSchema])
def get_book_reviews(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return db.query(ReviewModel).filter(ReviewModel.book_id == book_id).all()


@router.post(
    "/books/{book_id}/reviews", response_model=ReviewSchema, status_code=201
)
def create_review(
    book_id: int,
    review: CreateReviewSchema,
    db: Session = Depends(get_db),
):
    book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    new_review = ReviewModel(**review.dict(), book_id=book_id)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@router.get("/reviews/{review_id}", response_model=ReviewSchema)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.put("/reviews/{review_id}", response_model=ReviewSchema)
def update_review(
    review_id: int,
    review: UpdateReviewSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db_review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    if db_review.book.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the book owner can update this review")

    for field, value in review.dict(exclude_unset=True).items():
        setattr(db_review, field, value)

    db.commit()
    db.refresh(db_review)
    return db_review


@router.delete("/reviews/{review_id}", status_code=204)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    if review.book.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the book owner can delete this review")

    db.delete(review)
    db.commit()