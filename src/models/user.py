from sqlalchemy import Column, String, Integer
from src.models.base import BaseModel


class User(BaseModel):
    """Base user model"""
    
    __tablename__ = 'user'
    id = Column(type_=Integer, autoincrement=True, primary_key=True, nullable=False)
    wallet_address = Column(type_=String, unique=True, nullable=False)
    