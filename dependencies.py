"""
Dependencies - Permission Guards & Authentication

This file defines:
- How to check if someone is logged in (validate their token)
- How to check if they have permission (are they admin? analyst?)
- What to do if they don't have permission (deny access)

Think of this as the "security checkpoint" that validates credentials
and permissions.
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
    Validate the user's login token and return their user object.
    
    What it does:
      1. Looks for "Authorization: Bearer <token>" in request header
      2. Decodes the JWT token (checks it's real and not expired)
      3. Finds the user in database
      4. Checks if account is active
      5. Returns the User object or raises error
    
    Raises:
      - 401 Unauthorized: No token, invalid token, or token expired
      - 403 Forbidden: Account is deactivated
      - 404 Not Found: User doesn't exist in database
    
    Used by: All protected endpoints (any endpoint that needs login)
    
    Example:
      @app.get("/me")
      def get_profile(user: User = Depends(get_current_user)):
          # At this point, 'user' is guaranteed valid
          return {"email": user.email}
    """
    try:
        # Parse "Bearer <token>" from header
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
    
    # Validate the JWT token
    token_data = decode_token(token)
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Find user in database
    user = db.query(User).filter(User.id == token_data.user_id).first()
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    """
    Permission guard: Allow ONLY ADMIN users.
    
    What it does:
      1. Gets the current user (validates login via get_current_user)
      2. Checks if their role is ADMIN
      3. Denies access (403 Forbidden) if not admin
      4. Allows and returns user if admin
    
    Raises:
      - 403 Forbidden: User is not an admin
    
    Used by: Admin-only endpoints (like delete transaction)
    
    Example:
      @app.delete("/transactions/{id}")
      def delete_transaction(id: int, user: User = Depends(require_admin)):
          # Only admins can reach here
          # Non-admins get 403 Forbidden
    """
    if user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )
    return user


def require_analyst_or_above(user: User = Depends(get_current_user)) -> User:
    """
    Permission guard: Allow ADMIN and ANALYST users (deny VIEWER).
    
    What it does:
      1. Gets the current user (validates login)
      2. Checks if role is ANALYST or ADMIN
      3. Denies access (403 Forbidden) if VIEWER
      4. Allows and returns user if ANALYST or ADMIN
    
    Raises:
      - 403 Forbidden: User is a VIEWER
    
    Used by: Analytics and advanced feature endpoints
    
    Example:
      @app.get("/analytics/summary")
      def get_summary(user: User = Depends(require_analyst_or_above)):
          # Viewers get 403 Forbidden
          # Analysts and Admins can access
    """
    if user.role not in [UserRole.ANALYST, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analysts and Admins only"
        )
    return user


async def require_role(*roles: UserRole):
    """
    Generic permission guard: Check for specific roles.
    
    What it does:
      1. Creates a reusable permission checker
      2. Allows any user with one of the specified roles
      3. Denies others with 403 Forbidden
    
    This is a "factory" - it returns a permission checker function
    that you can customize with any roles you want.
    
    Used by: Custom permission requirements
    
    Example:
      # Allow editors and admins only
      @app.put("/posts/{id}")
      def edit_post(
          id: int,
          user: User = Depends(require_role(UserRole.EDITOR, UserRole.ADMIN))
      ):
          # Only editors and admins can edit
          pass
    
    Example:
      # Allow only exact role match
      @app.delete("/users/{id}")
      def delete_user(
          id: int,
          user: User = Depends(require_role(UserRole.ADMIN))
      ):
          # Only admins can delete users
          pass
    """
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join([r.value for r in roles])}"
            )
        return current_user
    
    return role_checker
