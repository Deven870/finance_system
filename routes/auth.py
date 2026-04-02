"""
Authentication API Routes - Login & Registration

This file handles:
- POST /auth/register - Sign up for a new account
- POST /auth/login - Login and get a token

These are the "public" endpoints - no login required.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from database import get_db, settings
from schemas.user import UserRegister, UserLogin, UserResponse, Token
from models.user import User, UserRole
from services.auth_service import (
    authenticate_user,
    get_password_hash,
    get_or_create_user,
    create_access_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Sign up for a new account.
    
    What it does:
      1. Checks if email already exists (prevent duplicates)
      2. Hashes the password (for security)
      3. Creates new user account in database
      4. Sets role to "viewer" (basic permission level)
    
    Request body:
      {
        "email": "john@example.com",
        "full_name": "John Doe",
        "password": "SecurePass123!"
      }
    
    Returns:
      {
        "message": "User registered successfully",
        "user": { email, full_name, role, etc },
        "note": "Your account has been created with 'viewer' role..."
      }
    
    Errors:
      - 400 Bad Request: Email already registered
      - 422 Unprocessable Entity: Invalid data (bad email format, short password, etc)
    
    Example:
      # Sign up
      POST /auth/register
      {
        "email": "jane@example.com",
        "full_name": "Jane Smith",
        "password": "MyPassword123!"
      }
      
      # You get back a response with your new user
    """
    # Check if email is already in use
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password (never store plain text)
    hashed_password = get_password_hash(user_data.password)
    
    # Create the new user
    new_user = get_or_create_user(
        db,
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=UserRole.VIEWER  # All new users start as "viewer"
    )
    
    return {
        "message": "User registered successfully",
        "user": UserResponse.from_attributes(new_user),
        "note": "Your account has been created with 'viewer' role. Contact admin to upgrade."
    }


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Log in and get a temporary token.
    
    What it does:
      1. Finds user by email
      2. Verifies password is correct
      3. Creates a JWT token (your login ticket)
      4. Returns token valid for 12 hours
    
    Request body:
      {
        "email": "john@example.com",
        "password": "SecurePass123!"
      }
    
    Returns:
      {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5c...",
        "token_type": "bearer",
        "expires_in": 43200  (seconds, = 12 hours)
      }
    
    How to use the token:
      1. Copy the access_token value
      2. Add it to every request header:
         Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5c...
      3. Token proves you're logged in
      4. After 12 hours, token expires and you must login again
    
    Errors:
      - 401 Unauthorized: Wrong email or password
      - 422 Unprocessable Entity: Invalid data (bad email format, etc)
    
    Example:
      # Login
      POST /auth/login
      {
        "email": "john@example.com",
        "password": "SecurePass123!"
      }
      
      # You get back a token
      {
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "token_type": "bearer",
        "expires_in": 43200
      }
      
      # Use this token:
      # Headers: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """
    # Try to authenticate (find user and verify password)
    user = authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create JWT token (valid for 12 hours by default)
    access_token, expires_at = create_access_token(
        data={
            "sub": user.email,
            "user_id": user.id,
            "role": user.role.value
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60  # Convert to seconds
    }
