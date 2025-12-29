"""
SalaatFlow API - Phase II
FastAPI backend for Islamic task management

Author: Claude Code
Date: 2025-12-27
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager - runs on startup and shutdown"""
    print("🚀 Starting SalaatFlow API...")
    print(f"📍 Environment: {settings.environment}")
    print(f"🔌 Database: {settings.database_url[:20]}...")

    # Create database tables on startup
    create_db_and_tables()
    print("✅ Database tables ready")

    yield

    print("👋 Shutting down SalaatFlow API...")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Islamic Task Management API for tracking spiritual activities",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "As-salamu alaykum! Welcome to SalaatFlow API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SalaatFlow API",
        "version": settings.app_version,
    }


# Include routers
from routers import tasks, masjids, hadith

app.include_router(
    tasks.router,
    prefix=f"{settings.api_v1_prefix}/tasks",
    tags=["Tasks"],
)

app.include_router(
    masjids.router,
    prefix=f"{settings.api_v1_prefix}/masjids",
    tags=["Masjids"],
)

app.include_router(
    hadith.router,
    prefix=f"{settings.api_v1_prefix}/hadith",
    tags=["Daily Hadith"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
