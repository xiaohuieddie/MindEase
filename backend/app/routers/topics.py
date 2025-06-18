from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

from app.database import get_db, User, Topic
from app.core.security import get_current_user_optional

router = APIRouter()

# Pydantic models
class TopicResponse(BaseModel):
    id: str
    title: str
    subtitle: str
    description: str
    category: str
    is_active: bool
    created_at: datetime

class TopicCreate(BaseModel):
    title: str
    subtitle: str
    description: str
    category: str

# Sample daily topics (in production, these would come from a database or external API)
SAMPLE_TOPICS = [
    {
        "id": "topic_1",
        "title": "Monday Motivation",
        "subtitle": "How are you starting your week?",
        "description": "Share your thoughts on starting a new week and any goals or challenges you're facing.",
        "category": "workplace",
        "is_active": True
    },
    {
        "id": "topic_2", 
        "title": "Workplace Stress",
        "subtitle": "Dealing with deadline pressure",
        "description": "Let's talk about managing stress and pressure in the workplace.",
        "category": "workplace",
        "is_active": True
    },
    {
        "id": "topic_3",
        "title": "Social Connections", 
        "subtitle": "Feeling isolated lately?",
        "description": "Discuss the importance of social connections and how to maintain them.",
        "category": "social",
        "is_active": True
    },
    {
        "id": "topic_4",
        "title": "Self-Care Sunday",
        "subtitle": "What does self-care mean to you?",
        "description": "Explore different ways to practice self-care and prioritize your well-being.",
        "category": "personal",
        "is_active": True
    },
    {
        "id": "topic_5",
        "title": "Digital Wellness",
        "subtitle": "Balancing screen time and mental health",
        "description": "How do you manage your relationship with technology and social media?",
        "category": "personal",
        "is_active": True
    }
]

@router.get("/daily", response_model=List[TopicResponse])
def get_daily_topics(
    category: Optional[str] = None,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get daily conversation topics"""
    # In a real implementation, you might:
    # 1. Get topics from database
    # 2. Rotate topics based on date
    # 3. Personalize based on user preferences
    
    topics = SAMPLE_TOPICS
    
    if category:
        topics = [t for t in topics if t["category"] == category]
    
    return [
        TopicResponse(
            id=topic["id"],
            title=topic["title"],
            subtitle=topic["subtitle"],
            description=topic["description"],
            category=topic["category"],
            is_active=topic["is_active"],
            created_at=datetime.utcnow()
        )
        for topic in topics
    ]

@router.get("/daily/random", response_model=TopicResponse)
def get_random_daily_topic(
    category: Optional[str] = None,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get a random daily topic"""
    import random
    
    topics = SAMPLE_TOPICS
    
    if category:
        topics = [t for t in topics if t["category"] == category]
    
    if not topics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No topics found for the specified category"
        )
    
    topic = random.choice(topics)
    
    return TopicResponse(
        id=topic["id"],
        title=topic["title"],
        subtitle=topic["subtitle"],
        description=topic["description"],
        category=topic["category"],
        is_active=topic["is_active"],
        created_at=datetime.utcnow()
    )

@router.get("/categories")
def get_topic_categories(
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """Get available topic categories"""
    categories = list(set(topic["category"] for topic in SAMPLE_TOPICS))
    return {"categories": categories}

@router.get("/{topic_id}", response_model=TopicResponse)
def get_topic_by_id(
    topic_id: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get a specific topic by ID"""
    # In a real implementation, this would query the database
    topic = next((t for t in SAMPLE_TOPICS if t["id"] == topic_id), None)
    
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found"
        )
    
    return TopicResponse(
        id=topic["id"],
        title=topic["title"],
        subtitle=topic["subtitle"],
        description=topic["description"],
        category=topic["category"],
        is_active=topic["is_active"],
        created_at=datetime.utcnow()
    )

# Admin endpoints (for managing topics)
@router.post("/", response_model=TopicResponse)
def create_topic(
    topic_data: TopicCreate,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Create a new topic (admin only)"""
    if not current_user or not current_user.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin access required"
        )
    
    # In a real implementation, you'd check if user is admin
    # For now, we'll just create the topic in the database
    
    topic = Topic(
        title=topic_data.title,
        subtitle=topic_data.subtitle,
        description=topic_data.description,
        category=topic_data.category
    )
    db.add(topic)
    db.commit()
    db.refresh(topic)
    
    return TopicResponse(
        id=topic.id,
        title=topic.title,
        subtitle=topic.subtitle,
        description=topic.description,
        category=topic.category,
        is_active=topic.is_active,
        created_at=topic.created_at
    )

@router.get("/", response_model=List[TopicResponse])
def get_all_topics(
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get all topics (admin only)"""
    if not current_user or not current_user.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin access required"
        )
    
    topics = db.query(Topic).filter(Topic.is_active == True).all()
    
    return [
        TopicResponse(
            id=topic.id,
            title=topic.title,
            subtitle=topic.subtitle,
            description=topic.description,
            category=topic.category,
            is_active=topic.is_active,
            created_at=topic.created_at
        )
        for topic in topics
    ] 