"""
Analytics Service - Financial insights & calculations

This file handles all the math:
- Calculating total income, expenses, and balance
- Breaking down money by category (how much on food? salary?)
- Monthly summaries (how did we do each month?)
- Finding trends and patterns (what's our biggest expense?)
- Finding recent transactions

Think of this as the "accountant" that runs the numbers.
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
    
    What it does:
      1. Add up all INCOME transactions for this user
      2. Add up all EXPENSE transactions for this user
      3. Calculate balance = income - expenses
    
    Returns:
        dict with:
        - total_income: How much money came in
        - total_expenses: How much money went out
        - balance: Money left over (or negative if spent more than earned)
    
    Example:
      balance = get_balance_summary(db, user_id=5)
      # Returns: {
      #   "total_income": 5000.00,
      #   "total_expenses": 3200.50,
      #   "balance": 1799.50  (you have this much left)
      # }
    """
    # Add up all income transactions
    total_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.transaction_type == TransactionType.INCOME
    ).scalar() or 0
    
    # Add up all expense transactions
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
    Show how much money is in each category.
    
    What it does:
      Groups all transactions by:
      1. Type (income or expense)
      2. Category (salary, food, transport, etc)
      3. Adds up the amounts
    
    Returns:
        dict with structure:
        {
          "income": {
            "salary": 4000.00,
            "freelance": 500.00,
            ...
          },
          "expenses": {
            "food": 400.00,
            "transport": 150.00,
            ...
          }
        }
    
    Example:
      breakdown = get_category_breakdown(db, user_id=5)
      # Ask: "How much did I spend on food?" 
      # Answer: breakdown["expenses"]["food"] = 350.50
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
    Organize transactions by month.
    
    What it does:
      1. Get all transactions for this user
      2. Group by month (Jan 2024, Feb 2024, etc)
      3. Calculate income, expenses, and balance for each month
      4. Return sorted by month
    
    Returns:
        dict with months as keys:
        {
          "2024-01": {
            "income": 4500.00,
            "expenses": 3200.00,
            "balance": 1300.00
          },
          "2024-02": { ... },
          ...
        }
    
    Example:
      summary = get_monthly_summary(db, user_id=5)
      # Ask: "How did we do in January?"
      # Answer: summary["2024-01"]["balance"] = 1300.00
    """
    # Get all this user's transactions
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).all()
    
    monthly_data = {}
    
    # Group transactions by month
    for transaction in transactions:
        month_key = transaction.date.strftime("%Y-%m")  # e.g., "2024-01"
        
        if month_key not in monthly_data:
            monthly_data[month_key] = {
                "income": 0,
                "expenses": 0,
            }
        
        # Add to the appropriate category
        if transaction.transaction_type == TransactionType.INCOME:
            monthly_data[month_key]["income"] += transaction.amount
        else:
            monthly_data[month_key]["expenses"] += transaction.amount
    
    # Calculate balance and round values for each month
    for month in monthly_data:
        monthly_data[month]["income"] = round(monthly_data[month]["income"], 2)
        monthly_data[month]["expenses"] = round(monthly_data[month]["expenses"], 2)
        monthly_data[month]["balance"] = round(
            monthly_data[month]["income"] - monthly_data[month]["expenses"], 2
        )
    
    return dict(sorted(monthly_data.items()))


def get_recent_transactions(db: Session, user_id: int, limit: int = 10):
    """
    Get the most recent transactions.
    
    What it does:
      1. Find all this user's transactions
      2. Sort by date (newest first)
      3. Return the most recent ones (limit = how many)
    
    Args:
      limit: How many to return (default 10)
    
    Returns:
        List of Transaction objects, newest first
    
    Example:
      recent = get_recent_transactions(db, user_id=5, limit=5)
      # Returns the 5 most recent transactions
    """
    return db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).order_by(
        Transaction.date.desc(),  # Newest date first
        Transaction.created_at.desc()  # If same date, newest record first
    ).limit(limit).all()


def get_spending_trends(db: Session, user_id: int) -> dict:
    """
    Analyze spending habits (patterns and insights).
    
    What it does:
      1. Count total number of transactions
      2. Calculate average transaction amount
      3. Find the biggest expense category (where's most money going?)
      4. Find the biggest income category (where's most money coming from?)
    
    Returns:
        dict with:
        - total_transactions: How many transactions recorded
        - average_transaction_amount: Average $$ per transaction
        - top_expense_category: Category where we spend the most
        - top_income_category: Category where we earn the most
    
    Example:
      trends = get_spending_trends(db, user_id=5)
      # Returns: {
      #   "total_transactions": 75,
      #   "average_transaction_amount": 92.50,
      #   "top_expense_category": {
      #     "category": "food",
      #     "total": 1200.00  (spent most on food!)
      #   },
      #   ...
      # }
    """
    # Count all transactions for this user
    transaction_count = db.query(func.count(Transaction.id)).filter(
        Transaction.user_id == user_id
    ).scalar()
    
    # Calculate average amount per transaction
    avg_amount = db.query(func.avg(Transaction.amount)).filter(
        Transaction.user_id == user_id
    ).scalar() or 0
    
    # Find the category where we spend the most
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
    
    # Find the category where we earn the most
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
