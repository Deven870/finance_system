"""
Dependencies for authentication and authorization.
"""

from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from database import get_db
from services.auth_service import decode_token
from models.user import User, UserRole
from schemas.user import TokenData


def get_current_user(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from token.
    Raises HTTPException(401) if token is invalid or expired.
    """
    try:
        # Extract token from "Bearer <token>" format
        scheme, token = authorization.split(" ")
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (ValueError, IndexError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = decode_token(token)
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    """Guard: Allow only admin users"""
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )
    return user


def require_analyst_or_above(user: User = Depends(get_current_user)) -> User:
    """Guard: Allow admin and analyst users"""
    if user.role not in [UserRole.ANALYST, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analysts and Admins only"
        )
    return user


async def require_role(*roles: UserRole):
    """
    Factory function to create a dependency that checks user role.
    Usage: Depends(require_role(UserRole.ADMIN, UserRole.ANALYST))
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join([r.value for r in roles])}"
            )
        return current_user
    
    return role_checker
