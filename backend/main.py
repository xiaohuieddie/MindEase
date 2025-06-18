from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.database import engine, Base
from app.routers import chat, auth, wellness, topics, analytics
from app.core.config import settings
from app.core.security import get_current_user_optional

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
    yield
    # Shutdown
    pass

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

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(wellness.router, prefix="/api/v1/wellness", tags=["Wellness"])
app.include_router(topics.router, prefix="/api/v1/topics", tags=["Topics"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])

@app.get("/")
async def root():
    return {
        "message": "MindEase API - AI Mental Wellness Companion",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs",
        "frontend_url": "http://localhost:3000"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting MindEase Backend...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔗 Frontend URL: http://localhost:3000")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 