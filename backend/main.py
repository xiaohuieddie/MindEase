from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import os
import logging
import time
from datetime import datetime
from dotenv import load_dotenv

from app.database import engine, Base
from app.routers import chat, auth, wellness, topics, analytics
from app.core.config import settings
from app.core.security import get_current_user_optional
from logging_config import setup_logging

load_dotenv()

# Setup logging
logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting MindEase Backend...")
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created successfully")
    logger.info("📖 API Documentation: http://localhost:8000/docs")
    logger.info("🔗 Frontend URL: http://localhost:3000")
    yield
    # Shutdown
    logger.info("🛑 Shutting down MindEase Backend...")

app = FastAPI(
    title="MindEase API",
    description="AI Mental Wellness Companion API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - Updated for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js frontend
        "http://127.0.0.1:3000",  # Alternative localhost
        "http://localhost:3001",  # In case port 3000 is busy
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log incoming request
    logger.info(f"📥 {request.method} {request.url.path} - Client: {request.client.host if request.client else 'unknown'}")
    
    # Log request headers (excluding sensitive ones)
    headers = dict(request.headers)
    safe_headers = {k: v for k, v in headers.items() if k.lower() not in ['authorization', 'cookie']}
    logger.debug(f"📋 Headers: {safe_headers}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log response
    logger.info(f"📤 {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.3f}s")
    
    return response

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(wellness.router, prefix="/api/v1/wellness", tags=["Wellness"])
app.include_router(topics.router, prefix="/api/v1/topics", tags=["Topics"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])

@app.get("/")
async def root():
    logger.info("🏠 Root endpoint accessed")
    return {
        "message": "MindEase API - AI Mental Wellness Companion",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs",
        "frontend_url": "http://localhost:3000"
    }

@app.get("/health")
async def health_check():
    logger.info("💚 Health check endpoint accessed")
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 