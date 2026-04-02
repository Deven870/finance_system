"""
Pydantic Schemas for Users - Validating incoming & outgoing data

This file defines:
- What data we accept when creating/updating users (validation rules)
- What data we send back to clients (response format)
- What data goes into JWT tokens (token payload)

Think of schemas as "contracts" - "if you give me data in this format, 
I'll accept it and store it. When I send data back, it will look like this."
"""

from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from models.user import UserRole


class UserBase(BaseModel):
    """
    Basic user fields that appear in multiple schemas.
    
    Fields:
    - email: Must be a valid email address
    - full_name: 1-100 characters
    """
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)


class UserRegister(UserBase):
    """
    Schema for when someone signs up.
    
    Requires:
    - email
    - full_name  
    - password (8-100 characters, must be secure)
    """
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """
    Schema for when someone logs in.
    
    Requires:
    - email
    - password
    
    If these are correct, they get a JWT token back.
    """
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """
    Schema for updating user information.
    
    All fields are optional (can update just one field).
    """
    full_name: str = Field(None, min_length=1, max_length=100)
    password: str = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    """
    Schema for user response data.
    
    What we send back when someone asks about a user.
    Note: We NEVER send back the password (it's hashed and secret).
    """
    id: int  # Their unique ID
    role: UserRole  # viewer, analyst, or admin
    is_active: bool  # Can they log in?
    created_at: datetime  # When they signed up

    class Config:
        from_attributes = True  # Convert SQLAlchemy model to this schema


class UserDetail(UserResponse):
    """
    Extended user information (includes when they last changed anything).
    """
    updated_at: datetime  # Last time their account changed

    class Config:
        from_attributes = True


class Token(BaseModel):
    """
    Schema for JWT token response (what we send back after login).
    
    Contains:
    - access_token: The actual token string (send this with every request)
    - token_type: Always "bearer" 
    - expires_in: How many seconds until token expires
    """
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    """
    Schema for JWT token payload (what's INSIDE the token).
    
    We extract this when validating the token:
    - email: User's email
    - user_id: User's ID
    - role: Their permission level
    """
    email: str
    user_id: int
    role: UserRole
