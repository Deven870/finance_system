"""
Analytics API Routes - Financial Reports & Insights

This file handles:
- GET /analytics/summary - Big picture: income, expenses, balance
- GET /analytics/by-category - How much in each category?
- GET /analytics/monthly - Month-by-month trends
- GET /analytics/recent - Last 10 transactions
- GET /analytics/trends - Insights and statistics

Authorization: All logged-in users can see their own analytics
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.user import User, UserRole
from dependencies import get_current_user
from services.analytics_service import (
    get_balance_summary,
    get_category_breakdown,
    get_monthly_summary,
    get_recent_transactions,
    get_spending_trends,
)
from schemas.transaction import TransactionResponse

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
async def get_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get your financial summary (big picture view).
    
    Who can use this?
      All logged-in users can see their own summary
    
    What it returns:
      - total_income: Total money earned
      - total_expenses: Total money spent
      - balance: Money left over (income - expenses)
    
    Example:
      GET /analytics/summary
      
      Returns:
      {
        "user_id": 5,
        "total_income": 5000.00,
        "total_expenses": 3200.50,
        "balance": 1799.50
      }
    
    Use this to quickly answer: "How much money do I have left?"
    """
    summary = get_balance_summary(db, current_user.id)
    return {
        "user_id": current_user.id,
        **summary
    }


@router.get("/by-category")
async def get_by_category(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Breakdown of money by category.
    
    Who can use this?
      All logged-in users can see their own category breakdown
    
    What it returns:
      - income: {category_name: amount, ...}
      - expenses: {category_name: amount, ...}
    
    Example:
      GET /analytics/by-category
      
      Returns:
      {
        "user_id": 5,
        "income": {
          "salary": 4000.00,
          "freelance": 1000.00
        },
        "expenses": {
          "food": 400.00,
          "transport": 150.00,
          "utilities": 100.00
        }
      }
    
    Use this to:
      - See where your money comes from (income breakdown)
      - See where your money goes (expense breakdown)
      - Identify which categories get the most/least money
    """
    breakdown = get_category_breakdown(db, current_user.id)
    return {
        "user_id": current_user.id,
        **breakdown
    }


@router.get("/monthly")
async def get_monthly(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Month-by-month financial summary.
    
    Who can use this?
      All logged-in users can see their own monthly trends
    
    What it returns:
      - months: {month_year: {income, expenses, balance}, ...}
      - Months are sorted chronologically
    
    Example:
      GET /analytics/monthly
      
      Returns:
      {
        "user_id": 5,
        "months": {
          "2024-01": {
            "income": 4500.00,
            "expenses": 3200.00,
            "balance": 1300.00
          },
          "2024-02": {
            "income": 4800.00,
            "expenses": 3500.00,
            "balance": 1300.00
          }
        }
      }
    
    Use this to:
      - Track how finances change month-to-month
      - Identify good months vs rough months
      - Plan for upcoming periods based on patterns
    """
    monthly = get_monthly_summary(db, current_user.id)
    return {
        "user_id": current_user.id,
        "months": monthly
    }


@router.get("/recent", response_model=list[TransactionResponse])
async def get_recent(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10,
):
    """
    Get your most recent transactions.
    
    Who can use this?
      All logged-in users can see their own recent transactions
    
    Query parameters:
      - limit: How many recent transactions to return (default 10)
    
    What it returns:
      Newest transactions first, in full detail
    
    Example:
      GET /analytics/recent?limit=5
      
      Returns:
      [
        {
          "id": 100,
          "amount": 50.00,
          "transaction_type": "expense",
          "category": "food",
          "date": "2024-01-15",
          "created_at": "2024-01-15T14:30:00",
          ...
        },
        ...
      ]
    
    Use this to:
      - See what you just recorded
      - Quickly review your latest spending/income
      - Spot errors you made recently
    """
    transactions = get_recent_transactions(db, current_user.id, limit)
    return transactions


@router.get("/trends")
async def get_trends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get insights and statistics about your finances.
    
    Who can use this?
      All logged-in users can see their own trends
    
    What it returns:
      - total_transactions: How many transactions you've recorded
      - average_transaction_amount: Average money per transaction
      - top_expense_category: Where you spend the most
      - top_income_category: Where you earn the most
    
    Example:
      GET /analytics/trends
      
      Returns:
      {
        "user_id": 5,
        "total_transactions": 75,
        "average_transaction_amount": 92.50,
        "top_expense_category": {
          "category": "food",
          "total": 1200.00
        },
        "top_income_category": {
          "category": "salary",
          "total": 4000.00
        }
      }
    
    Use this to:
      - Understand your financial behavior
      - Identify where you overspend (highest expense category)
      - See your main income sources
      - Track how active you are with recording transactions
    """
    trends = get_spending_trends(db, current_user.id)
    return {
        "user_id": current_user.id,
        **trends
    }
