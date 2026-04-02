"""
Finance System API - Main Application Entry Point

A FastAPI-based financial transaction tracking system with:
- User authentication via JWT
- Role-based access control (viewer, analyst, admin)
- Transaction CRUD operations
- Advanced analytics and summaries
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from database import engine, Base
from routes import auth, transactions, analytics

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Finance System API",
    description="A robust financial transaction tracking system with role-based access control",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(transactions.router)
app.include_router(analytics.router)


@app.get("/", tags=["Root"])
def read_root():
    """Welcome endpoint with API information."""
    return {
        "message": "Welcome to Finance System API",
        "documentation": "/docs",
        "api_version": "1.0.0",
        "note": "Use /docs to explore the interactive API documentation"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Finance System API"
    }


def custom_openapi():
    """Customize OpenAPI schema for better documentation."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Finance System API",
        version="1.0.0",
        description="""
        A comprehensive financial tracking API with:
        
        **Authentication:**
        - Register new accounts
        - Login with JWT tokens
        - 30-minute token expiration
        
        **Transaction Management:**
        - Create, read, update, delete transactions
        - Filter by date, type, category
        - Support for income and expense tracking
        
        **Role-Based Access:**
        - **Viewer**: Read-only access to own transactions
        - **Analyst**: Can create transactions + analytics
        - **Admin**: Full CRUD + user management
        
        **Analytics:**
        - Balance and summary calculations
        - Category-wise breakdowns
        - Monthly trends
        - Spending insights and trends
        
        **Security:**
        - Password hashing with bcrypt
        - JWT token-based authentication
        - Role-based authorization
        """,
        routes=app.routes,
    )
    
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    
    print("\n")
    print("=" * 60)
    print("Starting Finance System API")
    print("=" * 60)
    print("📖 API Docs:     http://localhost:8000/docs")
    print("🔑 ReDoc:        http://localhost:8000/redoc")
    print("=" * 60)
    print("\n")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
