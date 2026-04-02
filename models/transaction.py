"""
Transaction model for financial records.
"""

from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum as SQLEnum, ForeignKey, Date
from database import Base


class TransactionType(str, Enum):
    """Transaction type enumeration."""
    INCOME = "income"
    EXPENSE = "expense"


class TransactionCategory(str, Enum):
    """Transaction category enumeration."""
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENT = "investment"
    OTHER_INCOME = "other_income"
    FOOD = "food"
    TRANSPORT = "transport"
    UTILITIES = "utilities"
    ENTERTAINMENT = "entertainment"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    OTHER_EXPENSE = "other_expense"


class Transaction(Base):
    """Transaction model representing income or expense records."""
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)  # Positive value
    transaction_type = Column(SQLEnum(TransactionType), nullable=False, index=True)
    category = Column(SQLEnum(TransactionCategory), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)  # Transaction date
    description = Column(String, default="")
    notes = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Transaction {self.transaction_type} {self.amount} on {self.date}>"
