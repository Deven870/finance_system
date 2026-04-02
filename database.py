"""
Database Configuration

This file handles:
1. Database connection (SQLite)
2. Session management (how we talk to the database)
3. Base class for all models

Think of this as the "connection manager" - it handles all database communication.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """
    Application settings from environment variables.
    
    These values come from the .env file.
    Example:
      DATABASE_URL=sqlite:///./finance_system.db
      SECRET_KEY=your-secret-key-here
    """
    database_url: str = "sqlite:///./finance_system.db"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()

# Create database engine
# This is the "bridge" between Python and SQLite
# connect_args for SQLite: allows multiple threads to access same database
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)

# Create session factory
# Sessions are how we query the database
# sessionmaker creates new session instances when needed
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
# All our database models (User, Transaction, etc.) inherit from this
Base = declarative_base()

def get_db():
    """
    Dependency provider for database sessions.
    
    This is used by FastAPI to give each request a database session.
    After the request is done, it closes the session.
    
    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db  # Give the session to the request
    finally:
        db.close()  # Clean up after request is done
