"""
Seed script to populate database with mock data for testing.

Run this after first setting up: python seed_data.py
"""

from datetime import datetime, date, timedelta
from random import randint, choice, uniform
import sys

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, UserRole, Transaction, TransactionType, TransactionCategory
from services.auth_service import get_password_hash


def create_demo_users(db: Session):
    """Create demo users with different roles."""
    
    demo_users = [
        {
            "email": "viewer@example.com",
            "password": "password123",
            "full_name": "John Viewer",
            "role": UserRole.VIEWER
        },
        {
            "email": "analyst@example.com",
            "password": "password123",
            "full_name": "Jane Analyst",
            "role": UserRole.ANALYST
        },
        {
            "email": "admin@example.com",
            "password": "password123",
            "full_name": "Admin User",
            "role": UserRole.ADMIN
        },
    ]
    
    users = []
    for user_data in demo_users:
        # Check if user already exists
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            print(f"⏭️  User {user_data['email']} already exists, skipping...")
            users.append(existing)
            continue
        
        user = User(
            email=user_data["email"],
            hashed_password=get_password_hash(user_data["password"]),
            full_name=user_data["full_name"],
            role=user_data["role"],
            is_active=1
        )
        db.add(user)
        db.flush()
        users.append(user)
        print(f"✅ Created user: {user_data['email']} ({user_data['role']})")
    
    return users


def create_demo_transactions(db: Session, users: list[User]):
    """Create demo transactions for testing."""
    
    # Define demo transactions
    income_categories = [
        TransactionCategory.SALARY,
        TransactionCategory.FREELANCE,
        TransactionCategory.INVESTMENT,
    ]
    
    expense_categories = [
        TransactionCategory.FOOD,
        TransactionCategory.TRANSPORT,
        TransactionCategory.UTILITIES,
        TransactionCategory.ENTERTAINMENT,
        TransactionCategory.HEALTHCARE,
        TransactionCategory.EDUCATION,
    ]
    
    # Create transactions for last 90 days
    transaction_count = 0
    for user in users:
        for i in range(25):  # 25 transactions per user
            # Random date in last 90 days
            days_ago = randint(0, 90)
            transaction_date = date.today() - timedelta(days=days_ago)
            
            # Decide if income or expense (70% expense, 30% income)
            if uniform(0, 1) < 0.7:
                transaction_type = TransactionType.EXPENSE
                category = choice(expense_categories)
                amount = round(uniform(10, 500), 2)
                description = f"Regular {category.value} expense"
            else:
                transaction_type = TransactionType.INCOME
                category = choice(income_categories)
                amount = round(uniform(500, 5000), 2)
                description = f"{category.value} received"
            
            transaction = Transaction(
                user_id=user.id,
                amount=amount,
                transaction_type=transaction_type,
                category=category,
                date=transaction_date,
                description=description,
                notes=f"Demo transaction #{i + 1}",
            )
            db.add(transaction)
            transaction_count += 1
    
    db.commit()
    print(f"✅ Created {transaction_count} demo transactions")


def seed_database():
    """Main seed function."""
    print("\n" + "=" * 60)
    print("🌱 Finance System - Database Seeding")
    print("=" * 60 + "\n")
    
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created/verified\n")
        
        db = SessionLocal()
        
        # Create demo users
        print("Creating demo users...")
        users = create_demo_users(db)
        print()
        
        # Create demo transactions
        print("Creating demo transactions...")
        create_demo_transactions(db, users)
        print()
        
        db.close()
        
        print("=" * 60)
        print("✨ Database seeded successfully!")
        print("=" * 60)
        print("\n📝 Demo User Credentials:\n")
        
        print("Viewer Account (read-only):")
        print("  Email:    viewer@example.com")
        print("  Password: password123")
        print()
        
        print("Analyst Account (create + analytics):")
        print("  Email:    analyst@example.com")
        print("  Password: password123")
        print()
        
        print("Admin Account (full access):")
        print("  Email:    admin@example.com")
        print("  Password: password123")
        print()
        
        print("🚀 Start the API with: python main.py")
        print("📖 Visit: http://localhost:8000/docs for API documentation\n")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}", file=sys.stderr)
        raise


if __name__ == "__main__":
    seed_database()
