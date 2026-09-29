from pydantic import BaseModel, Field
# these imports are fromn Python
from typing import Optional, List
from .review import ReviewSchema
from .user import UserSchema 

class BookSchema(BaseModel):
  id: int
  name: str
  description: str
  user: UserSchema # New : returns user info with tea
  reviews: List[ReviewSchema] = Field(default_factory=list)

  class Config:
    orm_mode = True

# NEW: add a new schema for creating teas
class BookCreate(BaseModel):
    name: str
    description: str
# These are Schema Validations for the req.body on Create and Update
class CreateBookSchema(BaseModel):
  name: str
  description: str

class UpdateBookSchema(BaseModel):
  name: str
  description: str