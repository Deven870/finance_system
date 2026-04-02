"""
Transaction API Routes - Record Money In/Out

This file handles:
- GET /transactions - List all your transactions (with filters)
- GET /transactions/{id} - Get specific transaction details
- POST /transactions - Record a new income/expense
- PUT /transactions/{id} - Edit a transaction (admin only)
- DELETE /transactions/{id} - Remove a transaction (admin only)

Authorization: You can only see/edit your own transactions
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional, List

from database import get_db
from schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse,
)
from models.transaction import Transaction, TransactionType, TransactionCategory
from models.user import User, UserRole
from dependencies import get_current_user, require_admin

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=List[TransactionResponse])
async def list_transactions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    transaction_type: Optional[TransactionType] = None,
    category: Optional[TransactionCategory] = None,
):
    """
    Get your transactions (with optional filtering).
    
    Who can use this?
      All logged-in users can see their own transactions
    
    What it does:
      1. Finds all transactions belonging to you
      2. Applies filters (if provided)
      3. Sorts by date (newest first)
      4. Returns paginated results
    
    Query parameters:
      - start_date: Only show transactions from this date onwards (YYYY-MM-DD)
      - end_date: Only show transactions up to this date (YYYY-MM-DD)
      - transaction_type: Filter by "income" or "expense"
      - category: Filter by specific category (salary, food, etc)
      - skip: Skip this many records (pagination)
      - limit: Return this many records (pagination, max 100)
    
    Examples:
      # Get all your transactions
      GET /transactions
      
      # Get expenses only
      GET /transactions?transaction_type=expense
      
      # Get food expenses from Jan 2024
      GET /transactions?transaction_type=expense&category=food&start_date=2024-01-01&end_date=2024-01-31
      
      # Pagination: skip first 20, get next 10
      GET /transactions?skip=20&limit=10
    
    Returns:
      List of transactions matching your filters
    """
    # Start with user's transactions only
    query = db.query(Transaction).filter(Transaction.user_id == current_user.id)
    
    # Apply filters (if provided)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    
    if transaction_type:
        query = query.filter(Transaction.transaction_type == transaction_type)
    
    if category:
        query = query.filter(Transaction.category == category)
    
    # Sort by date (newest first) and apply pagination
    transactions = query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()
    
    return transactions


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get details of a specific transaction.
    
    Who can use this?
      All logged-in users (can only access their own transactions)
    
    What it does:
      1. Finds transaction by ID
      2. Checks you own it (prevent viewing other users' transactions)
      3. Returns full details
    
    Path parameter:
      - transaction_id: The ID of the transaction (from GET /transactions list)
    
    Errors:
      - 404 Not Found: Transaction doesn't exist or isn't yours
    
    Example:
      GET /transactions/42
      # Returns full details of transaction #42
    """
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id  # Security: only your transactions
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    return transaction


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Record a new transaction (income or expense).
    
    Who can use this?
      - ADMIN: Can create transactions
      - ANALYST: Can create transactions
      - VIEWER: Cannot create transactions (403 Forbidden)
    
    What it does:
      1. Checks your permission level
      2. Creates new transaction record
      3. Associates it with your account
      4. Saves to database
    
    Request body:
      {
        "amount": 50.00,
        "transaction_type": "expense",  # or "income"
        "category": "food",  # salary, food, transport, etc
        "date": "2024-01-15",  # YYYY-MM-DD
        "description": "Lunch",  # optional
        "notes": "Ate at restaurant"  # optional
      }
    
    Returns:
      The created transaction with ID assigned
    
    Errors:
      - 403 Forbidden: You're a viewer (read-only role)
      - 422 Unprocessable Entity: Invalid data
    
    Example:
      POST /transactions
      {
        "amount": 150.00,
        "transaction_type": "expense",
        "category": "transport",
        "date": "2024-01-15",
        "description": "Uber ride"
      }
      
      Returns:
      {
        "id": 42,
        "amount": 150.00,
        "transaction_type": "expense",
        ...
      }
    """
    # Check permission: viewers are read-only
    if current_user.role == UserRole.VIEWER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Viewers cannot create transactions"
        )
    
    # Create the transaction
    new_transaction = Transaction(
        user_id=current_user.id,
        amount=transaction_data.amount,
        transaction_type=transaction_data.transaction_type,
        category=transaction_data.category,
        date=transaction_data.date,
        description=transaction_data.description,
        notes=transaction_data.notes,
    )
    
    # Save to database
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    return new_transaction


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Edit an existing transaction.
    
    Who can use this?
      - ADMIN only (403 Forbidden for non-admins)
    
    What it does:
      1. Checks you're an admin
      2. Finds the transaction
      3. Updates only the fields you provide (others stay the same)
      4. Saves changes to database
    
    Path parameter:
      - transaction_id: The ID of the transaction to edit
    
    Request body (all optional):
      {
        "amount": 100.00,  # Can change any of these
        "transaction_type": "expense",
        "category": "food",
        "date": "2024-01-15",
        "description": "Updated notes",
        "notes": "New description"
      }
    
    Errors:
      - 403 Forbidden: You're not an admin
      - 404 Not Found: Transaction doesn't exist
    
    Example:
      PUT /transactions/42
      {
        "amount": 75.00,  # Changed from 50
        "description": "Updated lunch total"
      }
      
      # Only amount and description are updated
      # Other fields stay the same
    """
    # Check permission: admins only
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can update transactions"
        )
    
    # Find transaction
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id  # Security: only your transactions
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Update only the fields that were provided
    update_data = transaction_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(transaction, field, value)
    
    # Save changes
    db.commit()
    db.refresh(transaction)
    
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a transaction permanently.
    
    Who can use this?
      - ADMIN only (403 Forbidden for non-admins)
    
    What it does:
      1. Checks you're an admin
      2. Finds the transaction
      3. Deletes it from database (cannot undo!)
    
    Path parameter:
      - transaction_id: The ID of the transaction to delete
    
    Errors:
      - 403 Forbidden: You're not an admin
      - 404 Not Found: Transaction doesn't exist
    
    Returns:
      No content (204 success response)
    
    Warning:
      Deletion is permanent! This cannot be undone.
    
    Example:
      DELETE /transactions/42
      
      # Response: 204 No Content (success)
      # Transaction #42 is now deleted
    """
    # Check permission: admins only
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete transactions"
        )
    
    # Find transaction
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == current_user.id  # Security: only your transactions
    ).first()
    
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    
    # Delete it
    db.delete(transaction)
    db.commit()
    
    return None
