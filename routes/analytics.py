"""
Analytics routes for financial reports and insights.
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
    Get financial summary: total income, expenses, and balance.
    Available to all authenticated users.
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
    Get breakdown of transactions by category (both income and expenses).
    Available to all authenticated users.
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
    Get monthly income, expenses, and balance trends.
    Available to all authenticated users.
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
    Get the most recent transactions (default 10).
    Available to all authenticated users.
    """
    transactions = get_recent_transactions(db, current_user.id, limit)
    return transactions


@router.get("/trends")
async def get_trends(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get spending trends and insights.
    Includes transaction count, averages, and top categories.
    Available to all authenticated users.
    """
    trends = get_spending_trends(db, current_user.id)
    return {
        "user_id": current_user.id,
        **trends
    }
