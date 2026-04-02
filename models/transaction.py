"""
Transaction Model - The shape of financial records

This file defines:
- What data a transaction (income/expense) stores
- What types of transactions exist
- What categories transactions can have

Think of this as the "blueprint" for storing money records.
"""

from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum, ForeignKey, Date
from database import Base


class TransactionType(str, Enum):
    """Two types of transactions exist"""
    INCOME = "income"      # Money coming in
    EXPENSE = "expense"    # Money going out


class TransactionCategory(str, Enum):
    """Where money comes from or goes to"""
    # Income categories
    SALARY = "salary"              # Regular job
    FREELANCE = "freelance"        # Side work
    INVESTMENT = "investment"      # Returns on investments
    OTHER_INCOME = "other_income"  # Unexpected money
    
    # Expense categories
    FOOD = "food"                  # Groceries and dining
    TRANSPORT = "transport"        # Car, bus, taxi
    UTILITIES = "utilities"        # Electric, water, internet
    ENTERTAINMENT = "entertainment"  # Movies, games, fun
    HEALTHCARE = "healthcare"      # Doctor, medicine
    EDUCATION = "education"        # Courses, books
    OTHER_EXPENSE = "other_expense"  # Miscellaneous


class Transaction(Base):
    """
    Database model for a financial transaction.
    
    Each transaction records:
    - How much money
    - Whether it's income or expense
    - What category
    - When it happened
    - Optional notes
    
    Example:
      amount=50.00, type=expense, category=food
      means: "I spent $50 on food"
    """
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)  # Unique ID for this transaction
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Who does it belong to
    amount = Column(Float, nullable=False)  # How much money (always positive value)
    transaction_type = Column(SQLEnum(TransactionType), nullable=False, index=True)  # Income or expense
    category = Column(SQLEnum(TransactionCategory), nullable=False, index=True)  # What type (food, salary, etc)
    date = Column(Date, nullable=False, index=True)  # When it happened
    description = Column(String, default="")  # What it was for
    notes = Column(String, default="")  # Any extra details
    created_at = Column(DateTime, default=datetime.utcnow)  # When it was added to system
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Last time edited

    def __repr__(self) -> str:
        """Shows transaction as a human-readable string"""
        return f"<Transaction {self.transaction_type} ${self.amount} on {self.date}>"
