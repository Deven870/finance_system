"""
Authentication Service - Login, Password Hashing, & JWT Tokens

This file handles:
- Hashing passwords (converting plain text to secret code)
- Verifying passwords (checking if password is correct)
- Creating JWT tokens (login tickets)
- Decoding JWT tokens (validating login tickets)
- Finding users in the database

Think of this as the "security guard" that issues badges (JWT tokens)
and verifies them.
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
    """
    Hash a password into a secret code.
    
    Why: We never store plain text passwords. We convert them to hashes.
    When user logs in, we hash their input and compare hashes.
    
    Example:
      Input: "MyP@ssw0rd123"
      Output: "$argon2id$v=19$m=65540,t=3,p=4$..." (secret code)
    """
    if pwd_context:
        return pwd_context.hash(password[:72])
    else:
        # Simple fallback hash if argon2 not available
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Check if a plain password matches its hash.
    
    Why: User provides plain password at login.
    We hash it and compare to stored hash.
    If they match, password is correct.
    
    Example:
      plain_password: "MyP@ssw0rd123"
      hashed_password: "$argon2id$v=19$m=65540,t=3,p=4$..."
      Returns: True (passwords match)
    """
    if pwd_context:
        return pwd_context.verify(plain_password[:72], hashed_password)
    else:
        # Simple fallback verification
        import hashlib
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> tuple[str, datetime]:
    """
    Create a JWT token (login badge/ticket).
    
    What it does:
      1. Takes user info (email, user_id, role)
      2. Sets expiration time (12 hours by default)
      3. Signs it cryptographically (proves it's real)
      4. Returns token string and expiration time
    
    The token is sent back to user. They include it in every request
    to prove "I'm logged in as this user".
    
    Returns:
        tuple: (token_string, expiration_datetime)
    
    Example:
      data = {"sub": "john@example.com", "user_id": 5, "role": "analyst"}
      token, expires = create_access_token(data)
      # token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
      # expires: datetime(2024, 1, 15, 14, 30, 0)
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    
    # Sign the token with our secret key
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    
    return encoded_jwt, expire


def decode_token(token: str) -> Optional[TokenData]:
    """
    Read and validate a JWT token.
    
    What it does:
      1. Uses secret key to verify token wasn't tampered with
      2. Checks if token expired
      3. Extracts user info from inside token
      4. Returns TokenData (email, user_id, role) or None if invalid
    
    Returns:
        TokenData if token is valid and not expired
        None if token is invalid, tampered, or expired
    
    Example:
      token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
      data = decode_token(token)
      # data.email: "john@example.com"
      # data.user_id: 5
      # data.role: UserRole.ANALYST
    """
    try:
        # Verify with secret key and check signature
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
        # Token is invalid, expired, or tampered with
        return None


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """
    Attempt to log in a user.
    
    What it does:
      1. Find user by email in database
      2. Check if password is correct
      3. Return user object if both check out, None if either fails
    
    Returns:
        User object if authentication succeeds
        None if user doesn't exist, account is inactive, or password is wrong
    
    Example:
      user = authenticate_user(db, "john@example.com", "MyP@ssw0rd123")
      if user:
          print(f"Logged in as {user.email}")
      else:
          print("Login failed - wrong email or password")
    """
    user = db.query(User).filter(User.email == email, User.is_active == 1).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user


def get_or_create_user(db: Session, email: str, hashed_password: str, full_name: str, role: UserRole = UserRole.VIEWER) -> User:
    """
    Get existing user, or create and return new one.
    
    What it does:
      1. Look for user with this email
      2. If found, return existing user
      3. If not found, create new user and return it
    
    Used by: Seed script to create demo users
    
    Returns:
        User object (either existing or newly created)
    
    Example:
      user = get_or_create_user(
          db, 
          "john@example.com",
          hashed_password_here,  # Use get_password_hash() to create this
          "John Doe",
          role=UserRole.ANALYST
      )
    """
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
