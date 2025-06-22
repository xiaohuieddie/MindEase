from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid
import logging

from app.database import get_db, User
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token,
    create_anonymous_user,
    get_or_create_anonymous_user,
    get_current_user
)

router = APIRouter()
logger = logging.getLogger(__name__)

# Pydantic models
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    anonymous_id: Optional[str] = None

class AnonymousUserCreate(BaseModel):
    anonymous_id: Optional[str] = None

@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with email and password"""
    logger.info(f"🔐 Registration attempt for email: {user_data.email}")
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        logger.warning(f"❌ Registration failed - Email already exists: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    logger.info(f"✅ User registered successfully: {user.id} ({user_data.email})")
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user.id)
    )

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password"""
    logger.info(f"🔑 Login attempt for email: {user_data.email}")
    
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, str(user.hashed_password)):
        logger.warning(f"❌ Login failed - Invalid credentials for: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not bool(user.is_active):
        logger.warning(f"❌ Login failed - Inactive user: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    logger.info(f"✅ User logged in successfully: {user.id} ({user_data.email})")
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user.id),
        anonymous_id=str(user.anonymous_id) if user.anonymous_id is not None else None
    )

@router.post("/anonymous", response_model=Token)
def create_anonymous_session(user_data: AnonymousUserCreate, db: Session = Depends(get_db)):
    """Create or retrieve anonymous user session"""
    logger.info(f"👤 Anonymous session creation - ID: {user_data.anonymous_id or 'new'}")
    
    if user_data.anonymous_id:
        # Try to get existing anonymous user
        logger.debug(f"🔍 Looking for existing anonymous user: {user_data.anonymous_id}")
        user = get_or_create_anonymous_user(user_data.anonymous_id, db)
        logger.info(f"✅ Retrieved existing anonymous user: {user.id}")
    else:
        # Create new anonymous user
        logger.debug("🆕 Creating new anonymous user")
        user = create_anonymous_user(db)
        logger.info(f"✅ Created new anonymous user: {user.id}")
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    logger.info(f"🎫 Anonymous session token created for user: {user.id}")
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=str(user.id),
        anonymous_id=str(user.anonymous_id) if user.anonymous_id is not None else None
    )

@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    logger.info(f"👤 User info requested for: {current_user.id}")
    return {
        "id": current_user.id,
        "email": current_user.email,
        "anonymous_id": current_user.anonymous_id,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at
    } 