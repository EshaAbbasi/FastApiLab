from .user import UserModel 

class MeModel(BaseModel):
     __tablename__ = "mes"
    birthdate = Column(String, nullable=True)

    