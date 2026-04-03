from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from datetime import date


class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount must be positive")
    type: Literal['income', 'expense']
    category: str = Field(..., min_length=1)
    date: str
    notes: Optional[str] = None

    @validator('notes', pre=True, always=True)
    def set_notes(cls, v):
        return v or ''


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[Literal['income', 'expense']]
    category: Optional[str]
    date: Optional[str]
    notes: Optional[str]

    @validator('notes', pre=True, always=True)
    def set_notes(cls, v):
        return v or ''


class Transaction(TransactionBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str = Field(..., min_length=1)
    role: Literal['admin', 'analyst', 'viewer']


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
