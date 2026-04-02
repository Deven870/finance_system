"""
User model with role-based access control.
"""

from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from database import Base


class UserRole(str, Enum):
    """User role enumeration for role-based access control."""
    VIEWER = "viewer"      # Can only view transactions
    ANALYST = "analyst"    # Can view and filter transactions, access analytics
    ADMIN = "admin"        # Full CRUD access + user management


class User(Base):
    """User model for authentication and authorization."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active = Column(Integer, default=1)  # 0 = inactive, 1 = active
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role})>"
