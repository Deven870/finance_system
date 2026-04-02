"""
Finance System API - Main Application Entry Point

This is where everything starts. Think of this as the "starting gate" for the API.
When someone makes a request, it comes here first.

What this file does:
1. Creates the FastAPI app (web server)
2. Sets up the database tables
3. Connects all the routes (auth, transactions, analytics)
4. Starts the server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from database import engine, Base
from routes import auth, transactions, analytics

# Step 1: Create all database tables if they don't exist
# This runs once on startup and creates the schema
Base.metadata.create_all(bind=engine)

# Step 2: Initialize FastAPI application
# This is the main app that handles HTTP requests
app = FastAPI(
    title="Finance Tracker API",
    description="Track your income and expenses. Built with Python, FastAPI, and SQLite.",
    version="1.0.0",
)

# Step 3: Add CORS middleware
# This allows the API to accept requests from web browsers (frontend apps)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Step 4: Include routers
# Connect all the endpoints (login, transactions, analytics)
# Think of these as different "sections" of the API
app.include_router(auth.router)          # /auth/* routes
app.include_router(transactions.router)  # /transactions/* routes
app.include_router(analytics.router)     # /analytics/* routes


@app.get("/", tags=["Root"])
def read_root():
    """Welcome endpoint - shows that API is running"""
    return {
        "message": "Welcome to Finance Tracker API",
        "documentation": "/docs",
        "api_version": "1.0.0",
        "note": "Use /docs to explore the interactive API documentation"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint - used to verify API is alive"""
    return {
        "status": "healthy",
        "service": "Finance System API"
    }


def custom_openapi():
    """Customize the auto-generated API documentation"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Finance System API",
        version="1.0.0",
        description="""
        A Python backend for tracking personal finances.
        
        **Key Features:**
        - Add and track income/expenses
        - See summaries and trends
        - Role-based access (viewer, analyst, admin)
        - Secure authentication with tokens
        
        **Getting Started:**
        1. Login with the test credentials
        2. Create or view transactions
        3. Check analytics for summaries
        """,
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# This allows running the app directly: python main.py
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
        reload=True,  # Restart when code changes (development only)
        log_level="info"
    )
