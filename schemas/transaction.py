"""
Pydantic Schemas for Transactions - Validating incoming & outgoing data

This file defines:
- What data we accept when creating/updating transactions (validation rules)
- What data we send back to clients (response format)
- What filters are allowed when searching transactions

Think of schemas as "contracts" - "if you give me data in this format, 
I'll accept it and store it. When I send data back, it will look like this."
"""

from pydantic import BaseModel, Field
from datetime import date, datetime
from models.transaction import TransactionType, TransactionCategory
from typing import Optional


class TransactionBase(BaseModel):
    """
    Basic transaction fields that appear in multiple schemas.
    
    Fields:
    - amount: How much money (must be positive - can't have negative money)
    - transaction_type: Is it income or expense?
    - category: What category (salary, food, etc)?
    - date: When did this happen?
    - description: What's this for? (optional)
    - notes: Any extra details? (optional)
    """
    amount: float = Field(..., gt=0, description="Transaction amount (must be positive)")
    transaction_type: TransactionType
    category: TransactionCategory
    date: date
    description: str = Field("", max_length=255)
    notes: str = Field("", max_length=500)


class TransactionCreate(TransactionBase):
    """
    Schema for when someone records a new transaction.
    
    Requires all fields from TransactionBase.
    Example: "I spent $50 on food today"
    """
    pass


class TransactionUpdate(BaseModel):
    """
    Schema for updating an existing transaction.
    
    All fields are optional (can change just one thing, like the amount).
    """
    amount: Optional[float] = Field(None, gt=0)
    transaction_type: Optional[TransactionType] = None
    category: Optional[TransactionCategory] = None
    date: Optional[date] = None
    description: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = Field(None, max_length=500)


class TransactionResponse(TransactionBase):
    """
    Schema for transaction response data.
    
    What we send back when someone asks about transactions.
    Includes:
    - id: Unique transaction ID
    - user_id: Whose transaction is this?
    - created_at: When it was added to the system
    - updated_at: Last time it was changed
    """
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Convert SQLAlchemy model to this schema


class TransactionList(BaseModel):
    """
    Schema for searching/filtering transactions.
    
    Allows optional filters:
    - skip: Skip this many transactions (for pagination)
    - limit: Return this many transactions (page size)
    - start_date: Only show transactions after this date
    - end_date: Only show transactions before this date
    - transaction_type: Only show income or expense?
    - category: Only show specific category (food, salary, etc)?
    
    Example: "Skip 10, get 20 expense transactions from Jan-Mar"
    """
    skip: int = Field(0, ge=0)
    limit: int = Field(10, ge=1, le=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    transaction_type: Optional[TransactionType] = None
    category: Optional[TransactionCategory] = None
