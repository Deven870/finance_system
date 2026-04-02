"""
Authentication service with JWT and password hashing.
"""

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.user import User, UserRole
from schemas.user import TokenData
from database import settings
from typing import Optional

# Password hashing configuration - use argon2 for better compatibility
try:
    pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
except:
    # Fallback to simple hashing if argon2 not available
    import hashlib
    pwd_context = None


def get_password_hash(password: str) -> str:
    """Hash a password using argon2 or fallback to SHA256"""
    if pwd_context:
        return pwd_context.hash(password[:72])
    else:
        # Simple fallback hash
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash"""
    if pwd_context:
        return pwd_context.verify(plain_password[:72], hashed_password)
    else:
        # Simple fallback verification
        import hashlib
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> tuple[str, datetime]:
    """
    Create a JWT access token.
    
    Returns:
        tuple: (token, expiration_time)
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    
    return encoded_jwt, expire


def decode_token(token: str) -> Optional[TokenData]:
    """
    Decode and validate a JWT token.
    
    Returns:
        TokenData if valid, None if invalid or expired.
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        role: str = payload.get("role")
        
        if email is None or user_id is None:
            return None
        
        return TokenData(
            email=email,
            user_id=user_id,
            role=UserRole(role)
        )
    except JWTError:
        return None


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user with email and password."""
    user = db.query(User).filter(User.email == email, User.is_active == 1).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


def get_or_create_user(db: Session, email: str, hashed_password: str, full_name: str, role: UserRole = UserRole.VIEWER) -> User:
    """Get existing user or create new one."""
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        return user
    
    user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        role=role,
        is_active=1
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
