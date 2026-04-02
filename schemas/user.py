"""
Pydantic schemas for User validation and serialization.
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from models.user import UserRole


class UserBase(BaseModel):
    """Base user schema with common fields."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)


class UserRegister(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    full_name: str = Field(None, min_length=1, max_length=100)
    password: str = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    """Schema for user response (never expose password)."""
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserDetail(UserResponse):
    """Extended user detail schema."""
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """Schema for JWT token payload data."""
    email: str
    user_id: int
    role: UserRole
