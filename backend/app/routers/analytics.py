from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from app.database import get_db, User, Session as DBSession, Message, MoodEntry, WellnessActivity, Analytics
from app.core.security import get_current_user_optional

router = APIRouter()

# Pydantic models
class AnalyticsResponse(BaseModel):
    user_id: str
    metric_type: str
    value: float
    date: datetime

class UserInsights(BaseModel):
    total_sessions: int
    total_messages: int
    average_session_length: float
    most_active_day: str
    mood_trend: List[Dict[str, Any]]
    wellness_completion_rate: float
    crisis_detections: int

@router.get("/insights", response_model=UserInsights)
def get_user_insights(
    days: int = 30,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get comprehensive user insights and analytics"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get sessions
    sessions = db.query(DBSession).filter(
        and_(
            DBSession.user_id == current_user.id,
            DBSession.created_at >= start_date
        )
    ).all()
    
    # Get messages
    messages = db.query(Message).join(DBSession).filter(
        and_(
            DBSession.user_id == current_user.id,
            Message.timestamp >= start_date
        )
    ).all()
    
    # Get mood entries
    mood_entries = db.query(MoodEntry).filter(
        and_(
            MoodEntry.user_id == current_user.id,
            MoodEntry.created_at >= start_date
        )
    ).order_by(MoodEntry.created_at).all()
    
    # Get wellness activities
    wellness_activities = db.query(WellnessActivity).filter(
        and_(
            WellnessActivity.user_id == current_user.id,
            WellnessActivity.created_at >= start_date
        )
    ).all()
    
    # Calculate insights
    total_sessions = len(sessions)
    total_messages = len(messages)
    
    # Average session length (messages per session)
    avg_session_length = total_messages / total_sessions if total_sessions > 0 else 0
    
    # Most active day
    day_counts = {}
    for session in sessions:
        day = session.created_at.strftime("%A")
        day_counts[day] = day_counts.get(day, 0) + 1
    
    most_active_day = max(day_counts.items(), key=lambda x: x[1])[0] if day_counts else "No activity"
    
    # Mood trend (last 7 days)
    mood_trend = []
    for i in range(7):
        date = datetime.utcnow() - timedelta(days=i)
        day_entries = [entry for entry in mood_entries if entry.created_at.date() == date.date()]
        if day_entries:
            avg_intensity = sum(entry.intensity for entry in day_entries) / len(day_entries)
            mood_trend.append({
                "date": date.strftime("%Y-%m-%d"),
                "average_intensity": round(avg_intensity, 1),
                "entries_count": len(day_entries)
            })
    
    # Wellness completion rate
    total_wellness = len(wellness_activities)
    completed_wellness = len([a for a in wellness_activities if a.completed])
    wellness_completion_rate = (completed_wellness / total_wellness * 100) if total_wellness > 0 else 0
    
    # Crisis detections
    crisis_detections = len([msg for msg in messages if msg.crisis_detected])
    
    return UserInsights(
        total_sessions=total_sessions,
        total_messages=total_messages,
        average_session_length=round(avg_session_length, 1),
        most_active_day=most_active_day,
        mood_trend=mood_trend,
        wellness_completion_rate=round(wellness_completion_rate, 1),
        crisis_detections=crisis_detections
    )

@router.get("/mood/trend")
def get_mood_trend(
    days: int = 7,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get mood trend over time"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get mood entries grouped by date
    mood_data = db.query(
        func.date(MoodEntry.created_at).label('date'),
        func.avg(MoodEntry.intensity).label('avg_intensity'),
        func.count(MoodEntry.id).label('count')
    ).filter(
        and_(
            MoodEntry.user_id == current_user.id,
            MoodEntry.created_at >= start_date
        )
    ).group_by(func.date(MoodEntry.created_at)).order_by(func.date(MoodEntry.created_at)).all()
    
    return [
        {
            "date": str(entry.date),
            "average_intensity": round(float(entry.avg_intensity), 1),
            "entries_count": entry.count
        }
        for entry in mood_data
    ]

@router.get("/sessions/activity")
def get_session_activity(
    days: int = 30,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get session activity over time"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get sessions grouped by date
    session_data = db.query(
        func.date(DBSession.created_at).label('date'),
        func.count(DBSession.id).label('count')
    ).filter(
        and_(
            DBSession.user_id == current_user.id,
            DBSession.created_at >= start_date
        )
    ).group_by(func.date(DBSession.created_at)).order_by(func.date(DBSession.created_at)).all()
    
    return [
        {
            "date": str(entry.date),
            "sessions_count": entry.count
        }
        for entry in session_data
    ]

@router.get("/wellness/progress")
def get_wellness_progress(
    days: int = 30,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get wellness activity progress"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    try:
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get all wellness activities for the user
        activities = db.query(WellnessActivity).filter(
            and_(
                WellnessActivity.user_id == current_user.id,
                WellnessActivity.created_at >= start_date
            )
        ).all()
        
        # Group by activity type and calculate stats
        activity_stats = {}
        for activity in activities:
            if activity.activity_type not in activity_stats:
                activity_stats[activity.activity_type] = {"total": 0, "completed": 0}
            
            activity_stats[activity.activity_type]["total"] += 1
            if activity.completed:
                activity_stats[activity.activity_type]["completed"] += 1
        
        # Format response
        result = []
        for activity_type, stats in activity_stats.items():
            completion_rate = 0.0
            if stats["total"] > 0:
                completion_rate = (stats["completed"] / stats["total"]) * 100
            
            result.append({
                "activity_type": activity_type,
                "total": stats["total"],
                "completed": stats["completed"],
                "completion_rate": round(completion_rate, 1)
            })
        
        return result
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error in wellness progress: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/emotions/summary")
def get_emotion_summary(
    days: int = 30,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Get emotion summary and patterns"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get emotion counts
    emotion_data = db.query(
        MoodEntry.emotion,
        func.count(MoodEntry.id).label('count'),
        func.avg(MoodEntry.intensity).label('avg_intensity')
    ).filter(
        and_(
            MoodEntry.user_id == current_user.id,
            MoodEntry.created_at >= start_date
        )
    ).group_by(MoodEntry.emotion).order_by(func.count(MoodEntry.id).desc()).all()
    
    return [
        {
            "emotion": entry.emotion,
            "count": entry.count,
            "average_intensity": round(float(entry.avg_intensity), 1)
        }
        for entry in emotion_data
    ]

@router.post("/track")
def track_analytics_event(
    metric_type: str,
    value: float,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Track an analytics event"""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )
    
    analytics_entry = Analytics(
        user_id=current_user.id,
        metric_type=metric_type,
        value=value
    )
    db.add(analytics_entry)
    db.commit()
    db.refresh(analytics_entry)
    
    return {"message": "Analytics event tracked successfully"} 