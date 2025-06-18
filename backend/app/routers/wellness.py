from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, timedelta

from app.database import get_db, User, MoodEntry, WellnessActivity
from app.core.security import get_current_user_optional

router = APIRouter()

# Pydantic models
class MoodEntryCreate(BaseModel):
    emotion: str
    intensity: int  # 1-10 scale
    notes: Optional[str] = None

class MoodEntryResponse(BaseModel):
    id: str
    emotion: str
    intensity: int
    notes: Optional[str] = None
    created_at: datetime

class WellnessActivityCreate(BaseModel):
    activity_type: str  # "breathing", "affirmations", "reframing"
    duration: int  # in minutes

class WellnessActivityResponse(BaseModel):
    id: str
    activity_type: str
    duration: int
    completed: bool
    feedback_rating: Optional[int] = None
    created_at: datetime

class WellnessActivityComplete(BaseModel):
    feedback_rating: Optional[int] = None  # 1-5 scale

@router.post("/mood", response_model=MoodEntryResponse)
def create_mood_entry(
    mood_data: MoodEntryCreate,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Create a new mood entry"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required for mood tracking"
        )
    
    if not 1 <= mood_data.intensity <= 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Intensity must be between 1 and 10"
        )
    
    mood_entry = MoodEntry(
        user_id=current_user.id,
        emotion=mood_data.emotion,
        intensity=mood_data.intensity,
        notes=mood_data.notes
    )
    db.add(mood_entry)
    db.commit()
    db.refresh(mood_entry)
    
    return MoodEntryResponse(
        id=mood_entry.id,
        emotion=mood_entry.emotion,
        intensity=mood_entry.intensity,
        notes=mood_entry.notes,
        created_at=mood_entry.created_at
    )

@router.get("/mood", response_model=List[MoodEntryResponse])
def get_mood_entries(
    days: int = 7,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get mood entries for the specified number of days"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    entries = db.query(MoodEntry).filter(
        MoodEntry.user_id == current_user.id,
        MoodEntry.created_at >= start_date
    ).order_by(MoodEntry.created_at.desc()).all()
    
    return [
        MoodEntryResponse(
            id=entry.id,
            emotion=entry.emotion,
            intensity=entry.intensity,
            notes=entry.notes,
            created_at=entry.created_at
        )
        for entry in entries
    ]

@router.post("/activity", response_model=WellnessActivityResponse)
def create_wellness_activity(
    activity_data: WellnessActivityCreate,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Create a new wellness activity"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required for wellness activities"
        )
    
    valid_activities = ["breathing", "affirmations", "reframing"]
    if activity_data.activity_type not in valid_activities:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Activity type must be one of: {valid_activities}"
        )
    
    activity = WellnessActivity(
        user_id=current_user.id,
        activity_type=activity_data.activity_type,
        duration=activity_data.duration
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    
    return WellnessActivityResponse(
        id=activity.id,
        activity_type=activity.activity_type,
        duration=activity.duration,
        completed=activity.completed,
        feedback_rating=activity.feedback_rating,
        created_at=activity.created_at
    )

@router.post("/activity/{activity_id}/complete", response_model=WellnessActivityResponse)
def complete_wellness_activity(
    activity_id: str,
    completion_data: WellnessActivityComplete,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Mark a wellness activity as completed"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    activity = db.query(WellnessActivity).filter(
        WellnessActivity.id == activity_id,
        WellnessActivity.user_id == current_user.id
    ).first()
    
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found"
        )
    
    activity.completed = True
    if completion_data.feedback_rating:
        if not 1 <= completion_data.feedback_rating <= 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feedback rating must be between 1 and 5"
            )
        activity.feedback_rating = completion_data.feedback_rating
    
    db.commit()
    db.refresh(activity)
    
    return WellnessActivityResponse(
        id=activity.id,
        activity_type=activity.activity_type,
        duration=activity.duration,
        completed=activity.completed,
        feedback_rating=activity.feedback_rating,
        created_at=activity.created_at
    )

@router.get("/activity", response_model=List[WellnessActivityResponse])
def get_wellness_activities(
    days: int = 30,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get wellness activities for the specified number of days"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    activities = db.query(WellnessActivity).filter(
        WellnessActivity.user_id == current_user.id,
        WellnessActivity.created_at >= start_date
    ).order_by(WellnessActivity.created_at.desc()).all()
    
    return [
        WellnessActivityResponse(
            id=activity.id,
            activity_type=activity.activity_type,
            duration=activity.duration,
            completed=activity.completed,
            feedback_rating=activity.feedback_rating,
            created_at=activity.created_at
        )
        for activity in activities
    ]

@router.get("/stats")
def get_wellness_stats(
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get wellness statistics for the user"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    # Get last 30 days
    start_date = datetime.utcnow() - timedelta(days=30)
    
    # Mood stats
    mood_entries = db.query(MoodEntry).filter(
        MoodEntry.user_id == current_user.id,
        MoodEntry.created_at >= start_date
    ).all()
    
    # Wellness activity stats
    wellness_activities = db.query(WellnessActivity).filter(
        WellnessActivity.user_id == current_user.id,
        WellnessActivity.created_at >= start_date
    ).all()
    
    # Calculate stats
    total_mood_entries = len(mood_entries)
    avg_mood_intensity = sum(entry.intensity for entry in mood_entries) / total_mood_entries if total_mood_entries > 0 else 0
    
    total_activities = len(wellness_activities)
    completed_activities = len([a for a in wellness_activities if a.completed])
    completion_rate = (completed_activities / total_activities * 100) if total_activities > 0 else 0
    
    # Most common emotions
    emotion_counts = {}
    for entry in mood_entries:
        emotion_counts[entry.emotion] = emotion_counts.get(entry.emotion, 0) + 1
    
    most_common_emotion = max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else None
    
    return {
        "mood_stats": {
            "total_entries": total_mood_entries,
            "average_intensity": round(avg_mood_intensity, 1),
            "most_common_emotion": most_common_emotion
        },
        "wellness_stats": {
            "total_activities": total_activities,
            "completed_activities": completed_activities,
            "completion_rate": round(completion_rate, 1)
        }
    } 