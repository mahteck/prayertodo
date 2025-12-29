"""
SalaatFlow Phase II - FastAPI Application

Main application entry point for the SalaatFlow REST API.
Provides endpoints for managing spiritual tasks, masjids, and daily hadith.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from database import create_db_and_tables


# ============================================================================
# Application Lifespan Events
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Handles startup and shutdown events:
    - Startup: Create database tables
    - Shutdown: Cleanup resources
    """
    # Startup: Create database tables
    print("🚀 Starting SalaatFlow API...")
    print(f"📊 Environment: {settings.environment}")
    print(f"🔗 Database: Connected")

    try:
        create_db_and_tables()
        print("✅ Database tables created/verified")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")

    yield

    # Shutdown
    print("👋 Shutting down SalaatFlow API...")


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="REST API for Islamic Prayer & Spiritual Task Management",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# ============================================================================
# CORS Middleware
# ============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# ============================================================================
# Root Endpoints
# ============================================================================

@app.get("/")
async def root():
    """
    API root endpoint with welcome message and links.

    Returns:
        dict: Welcome message and API information
    """
    return {
        "message": "SalaatFlow API - Prayer & Spiritual Task Management",
        "version": settings.app_version,
        "phase": "II - Full-Stack Web Application",
        "docs": "/docs",
        "api": settings.api_v1_prefix,
        "status": "operational",
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns:
        dict: API health status
    """
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": settings.app_version,
    }


# ============================================================================
# API Routers
# ============================================================================

from routers import tasks, masjids, hadith

app.include_router(
    tasks.router,
    prefix=f"{settings.api_v1_prefix}/tasks",
    tags=["Tasks"]
)

app.include_router(
    masjids.router,
    prefix=f"{settings.api_v1_prefix}/masjids",
    tags=["Masjids"]
)

app.include_router(
    hadith.router,
    prefix=f"{settings.api_v1_prefix}/hadith",
    tags=["Daily Hadith"]
)


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,  # Auto-reload on code changes in development
    )
