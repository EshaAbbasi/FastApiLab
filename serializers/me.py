from typing import Optional

from pydantic import BaseModel


class MeSchema(BaseModel):
	birthdate = Column(Date, nullable=True)

	class Config:
		orm_mode = True


class CreateMeSchema(BaseModel):
	
    birthdate = str


class UpdateMeSchema(BaseModel):
	
	birthdate: Optional[str] = None
