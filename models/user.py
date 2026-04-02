"""
User Model - Who can use the system

This file defines:
- What fields a user account has (email, password, role, etc)
- What permissions each user has (viewer, analyst, admin)
- How to identify users in the database

Think of this as the "blueprint" for user accounts.
"""

from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from database import Base


class UserRole(str, Enum):
    """
    Three permission levels exist:
    
    VIEWER - Read-only access to their own transactions
    ANALYST - View transactions + financial analytics and insights  
    ADMIN - Full access (manage data, users, everything)
    """
    VIEWER = "viewer"      # Can only view transactions
    ANALYST = "analyst"    # Can view and filter transactions, access analytics
    ADMIN = "admin"        # Full CRUD access + user management


class User(Base):
    """
    Database model for a user account.
    
    Stores:
    - Their email address (used to log in)
    - Their password hash (password is never stored in plain text)
    - Their name
    - Their role/permission level (what they can do)
    - Whether they can currently log in (is_active)
    
    Example:
      email="john@example.com", role=ANALYST
      means: "John can see his transactions and get financial insights"
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Unique user ID
    email = Column(String, unique=True, index=True, nullable=False)  # Email (must be unique, used for login)
    hashed_password = Column(String, nullable=False)  # Password encrypted (never stored plain text)
    full_name = Column(String)  # Their name (optional)
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER, nullable=False)  # What they can do
    is_active = Column(Integer, default=1)  # 1 = can log in, 0 = cannot log in
    created_at = Column(DateTime, default=datetime.utcnow)  # When account was created
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Last time account changed

    def __repr__(self) -> str:
        """Shows user as a human-readable string"""
        return f"<User {self.email} ({self.role})>"
