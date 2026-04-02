"""
Pydantic schemas for Transaction validation and serialization.
"""

from pydantic import BaseModel, Field
from datetime import date, datetime
from models.transaction import TransactionType, TransactionCategory
from typing import Optional


class TransactionBase(BaseModel):
    """Base transaction schema with common fields."""
    amount: float = Field(..., gt=0, description="Transaction amount (must be positive)")
    transaction_type: TransactionType
    category: TransactionCategory
    date: date
    description: str = Field("", max_length=255)
    notes: str = Field("", max_length=500)


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""
    pass


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction."""
    amount: Optional[float] = Field(None, gt=0)
    transaction_type: Optional[TransactionType] = None
    category: Optional[TransactionCategory] = None
    date: Optional[date] = None
    description: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = Field(None, max_length=500)


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TransactionList(BaseModel):
    """Schema for list of transactions with optional filters."""
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    transaction_type: Optional[TransactionType] = None
    category: Optional[TransactionCategory] = None
