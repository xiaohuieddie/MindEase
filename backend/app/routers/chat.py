from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import openai
import anthropic
from datetime import datetime

from app.database import get_db, User, Session as DBSession, Message
from app.core.security import get_current_user_optional
from app.core.config import settings
from app.services.ai_service import AIService
from app.services.crisis_detection import CrisisDetectionService

router = APIRouter()

# Pydantic models
class ChatMessage(BaseModel):
    content: str
    session_id: str
    session_type: str = "free_form"  # "free_form", "topic_based", "emotion_based"
    emotion_context: Optional[str] = None
    topic_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    session_id: str
    crisis_detected: bool = False
    crisis_resources: Optional[dict] = None

class SessionCreate(BaseModel):
    session_type: str
    emotion_context: Optional[str] = None
    topic_id: Optional[str] = None

class SessionResponse(BaseModel):
    session_id: str
    session_type: str
    emotion_context: Optional[str] = None
    topic_id: Optional[str] = None
    created_at: datetime

# Initialize services
ai_service = AIService()
crisis_service = CrisisDetectionService()

@router.post("/session", response_model=SessionResponse)
def create_chat_session(
    session_data: SessionCreate,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Create a new chat session"""
    if not current_user:
        # Create anonymous user if no authenticated user
        from app.core.security import create_anonymous_user
        current_user = create_anonymous_user(db)
    
    # Create new session
    db_session = DBSession(
        user_id=current_user.id,
        session_type=session_data.session_type,
        emotion_context=session_data.emotion_context,
        topic_id=session_data.topic_id
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return SessionResponse(
        session_id=db_session.id,
        session_type=db_session.session_type,
        emotion_context=db_session.emotion_context,
        topic_id=db_session.topic_id,
        created_at=db_session.created_at
    )

@router.post("/message", response_model=ChatResponse)
async def send_message(
    message_data: ChatMessage,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Send a message and get AI response"""
    if not current_user:
        # Create anonymous user if no authenticated user
        from app.core.security import create_anonymous_user
        current_user = create_anonymous_user(db)
    
    # Check for crisis indicators
    crisis_detected = crisis_service.detect_crisis(message_data.content)
    
    # Save user message
    user_message = Message(
        session_id=message_data.session_id,
        content=message_data.content,
        role="user",
        crisis_detected=crisis_detected
    )
    db.add(user_message)
    db.commit()
    
    # Get AI response
    try:
        ai_response = await ai_service.generate_response(
            message=message_data.content,
            session_type=message_data.session_type,
            emotion_context=message_data.emotion_context,
            topic_id=message_data.topic_id,
            user_id=current_user.id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating AI response: {str(e)}"
        )
    
    # Save AI response
    ai_message = Message(
        session_id=message_data.session_id,
        content=ai_response,
        role="assistant",
        crisis_detected=crisis_detected
    )
    db.add(ai_message)
    db.commit()
    
    response_data = {
        "message": ai_response,
        "session_id": message_data.session_id,
        "crisis_detected": crisis_detected
    }
    
    # Add crisis resources if crisis detected
    if crisis_detected:
        response_data["crisis_resources"] = {
            "hotline": settings.CRISIS_HOTLINE,
            "text_line": settings.CRISIS_TEXT,
            "message": "If you're having thoughts of self-harm, please reach out for help immediately."
        }
    
    return ChatResponse(**response_data)

@router.get("/session/{session_id}/messages")
def get_session_messages(
    session_id: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get all messages for a specific session"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # Verify session belongs to user
    session = db.query(DBSession).filter(
        DBSession.id == session_id,
        DBSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    messages = db.query(Message).filter(
        Message.session_id == session_id
    ).order_by(Message.timestamp).all()
    
    return [
        {
            "id": msg.id,
            "content": msg.content,
            "role": msg.role,
            "timestamp": msg.timestamp,
            "crisis_detected": msg.crisis_detected
        }
        for msg in messages
    ]

@router.post("/session/{session_id}/end")
def end_session(
    session_id: str,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """End a chat session"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    session = db.query(DBSession).filter(
        DBSession.id == session_id,
        DBSession.user_id == current_user.id
    ).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    session.ended_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Session ended successfully"} 