from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, TIMESTAMP
from src.models.base import BaseModel


class Transaction(BaseModel):
    """Base transaction class"""
    
    __tablename__ = 'transaction'
    id = Column(type_=Integer, autoincrement=True, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    tx_hash = Column(type_=String, unique=True, nullable=False)
    amount = Column(type_=Numeric(10, 5), nullable=True)
    recipient = Column(type_=String, nullable=False)
    tx_type = Column(type_=String, nullable=False)
    tx_timestamp = Column(type_=TIMESTAMP, nullable=False)
    