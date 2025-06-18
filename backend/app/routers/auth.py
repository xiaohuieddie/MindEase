from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid

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
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
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
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id
    )

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password"""
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        anonymous_id=user.anonymous_id
    )

@router.post("/anonymous", response_model=Token)
def create_anonymous_session(user_data: AnonymousUserCreate, db: Session = Depends(get_db)):
    """Create or retrieve anonymous user session"""
    if user_data.anonymous_id:
        # Try to get existing anonymous user
        user = get_or_create_anonymous_user(user_data.anonymous_id, db)
    else:
        # Create new anonymous user
        user = create_anonymous_user(db)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        anonymous_id=user.anonymous_id
    )

@router.get("/me")
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "anonymous_id": current_user.anonymous_id,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at
    } 