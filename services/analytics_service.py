"""
Analytics service for financial summaries and insights.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, datetime
from models.transaction import Transaction, TransactionType, TransactionCategory
from models.user import User
from decimal import Decimal


def get_balance_summary(db: Session, user_id: int) -> dict:
    """
    Calculate total income, expenses, and balance.
    
    Returns:
        dict with total_income, total_expenses, balance
    """
    # Get total income
    total_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == TransactionType.INCOME
    ).scalar() or 0
    
    # Get total expenses
    total_expenses = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == TransactionType.EXPENSE
    ).scalar() or 0
    
    balance = total_income - total_expenses
    
    return {
        "total_income": round(float(total_income), 2),
        "total_expenses": round(float(total_expenses), 2),
        "balance": round(float(balance), 2)
    }


def get_category_breakdown(db: Session, user_id: int) -> dict:
    """
    Get spending/income breakdown by category.
    
    Returns:
        dict with category -> amount mapping for both income and expenses
    """
    results = db.query(
        Transaction.transaction_type,
        Transaction.category,
        func.sum(Transaction.amount).label("total")
    ).filter(
        Transaction.user_id == user_id
    ).group_by(
        Transaction.transaction_type,
        Transaction.category
    ).all()
    
    breakdown = {"income": {}, "expenses": {}}
    
    for row in results:
        transaction_type = row[0].value
        category = row[1].value
        total = round(float(row[2]), 2)
        
        if transaction_type == "income":
            breakdown["income"][category] = total
        else:
            breakdown["expenses"][category] = total
    
    return breakdown


def get_monthly_summary(db: Session, user_id: int) -> dict:
    """
    Get monthly income, expenses, and balance.
    
    Returns:
        dict with months and their summaries
    """
    # Query all transactions for the user
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).all()
    
    monthly_data = {}
    
    for transaction in transactions:
        month_key = transaction.date.strftime("%Y-%m")
        
        if month_key not in monthly_data:
            monthly_data[month_key] = {
                "income": 0,
                "expenses": 0,
            }
        
        if transaction.transaction_type == TransactionType.INCOME:
            monthly_data[month_key]["income"] += transaction.amount
        else:
            monthly_data[month_key]["expenses"] += transaction.amount
    
    # Calculate balance for each month and round values
    for month in monthly_data:
        monthly_data[month]["income"] = round(monthly_data[month]["income"], 2)
        monthly_data[month]["expenses"] = round(monthly_data[month]["expenses"], 2)
        monthly_data[month]["balance"] = round(
            monthly_data[month]["income"] - monthly_data[month]["expenses"], 2
        )
    
    return dict(sorted(monthly_data.items()))


def get_recent_transactions(db: Session, user_id: int, limit: int = 10):
    """Get the most recent transactions."""
    return db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).order_by(
        Transaction.date.desc(),
        Transaction.created_at.desc()
    ).limit(limit).all()


def get_spending_trends(db: Session, user_id: int) -> dict:
    """
    Analyze spending trends (highest expense categories, average daily spending, etc.).
    """
    # Total transactions count
    transaction_count = db.query(func.count(Transaction.id)).filter(
        Transaction.user_id == user_id
    ).scalar()
    
    # Average transaction amount
    avg_amount = db.query(func.avg(Transaction.amount)).filter(
        Transaction.user_id == user_id
    ).scalar() or 0
    
    # Highest expense category
    top_expense = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label("total")
    ).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == TransactionType.EXPENSE
    ).group_by(
        Transaction.category
    ).order_by(
        func.sum(Transaction.amount).desc()
    ).first()
    
    # Highest income category
    top_income = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label("total")
    ).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == TransactionType.INCOME
    ).group_by(
        Transaction.category
    ).order_by(
        func.sum(Transaction.amount).desc()
    ).first()
    
    return {
        "total_transactions": transaction_count,
        "average_transaction_amount": round(float(avg_amount), 2),
        "top_expense_category": {
            "category": top_expense[0].value if top_expense else None,
            "total": round(float(top_expense[1]), 2) if top_expense else 0
        },
        "top_income_category": {
            "category": top_income[0].value if top_income else None,
            "total": round(float(top_income[1]), 2) if top_income else 0
        }
    }
