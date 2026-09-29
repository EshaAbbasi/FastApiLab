from typing import Optional

from pydantic import BaseModel


class ReviewSchema(BaseModel):
	id: int
	rating: int
	description: str
	book_id: int

	class Config:
		orm_mode = True


class CreateReviewSchema(BaseModel):
	rating: int
	description: str


class UpdateReviewSchema(BaseModel):
	rating: Optional[int] = None
	description: Optional[str] = None
