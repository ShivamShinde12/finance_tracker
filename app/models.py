from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)  # admin, analyst, viewer


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    type = Column(String)  # income / expense
    category = Column(String)
    date = Column(String)
    notes = Column(String)
