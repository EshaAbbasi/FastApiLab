from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

#Association
from .review import ReviewModel
from .base import BaseModel
from .user import UserModel 

class BookModel(BaseModel):
    __tablename__ = "books"

    name = Column(String, unique=True)
    description = Column(String, unique=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserModel", back_populates="books")
    reviews = relationship("ReviewModel", back_populates="book")

    def __str__(self):
        return f"{self.id}: {self.name}"