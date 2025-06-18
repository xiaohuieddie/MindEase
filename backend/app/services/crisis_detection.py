import re
from typing import List, Dict, Any
from app.core.config import settings

class CrisisDetectionService:
    def __init__(self):
        self.crisis_keywords = settings.CRISIS_KEYWORDS
        self.crisis_patterns = [
            r'\b(kill\s+myself|end\s+it\s+all|want\s+to\s+die)\b',
            r'\b(suicide|self\s*[-]?\s*harm)\b',
            r'\b(cut\s+myself|hurt\s+myself)\b',
            r'\b(no\s+reason\s+to\s+live|better\s+off\s+dead)\b',
            r'\b(can\'t\s+take\s+it\s+anymore|give\s+up)\b'
        ]
    
    def detect_crisis(self, message: str) -> bool:
        """Detect crisis indicators in a message"""
        if not message:
            return False
        
        message_lower = message.lower()
        
        # Check for crisis keywords
        for keyword in self.crisis_keywords:
            if keyword.lower() in message_lower:
                return True
        
        # Check for crisis patterns
        for pattern in self.crisis_patterns:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return True
        
        # Check for high distress indicators
        distress_indicators = [
            r'\b(hopeless|helpless|worthless)\b',
            r'\b(can\'t\s+go\s+on|can\'t\s+handle\s+this)\b',
            r'\b(everyone\s+would\s+be\s+better\s+off)\b'
        ]
        
        for pattern in distress_indicators:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return True
        
        return False
    
    def get_crisis_severity(self, message: str) -> str:
        """Get crisis severity level"""
        if not self.detect_crisis(message):
            return "none"
        
        message_lower = message.lower()
        
        # High severity indicators
        high_severity = [
            r'\b(kill\s+myself|suicide|end\s+it\s+all)\b',
            r'\b(plan\s+to\s+die|going\s+to\s+end\s+it)\b'
        ]
        
        for pattern in high_severity:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return "high"
        
        # Medium severity indicators
        medium_severity = [
            r'\b(want\s+to\s+die|better\s+off\s+dead)\b',
            r'\b(self\s*[-]?\s*harm|cut\s+myself)\b'
        ]
        
        for pattern in medium_severity:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return "medium"
        
        return "low"
    
    def get_crisis_resources(self, severity: str = "medium") -> Dict[str, Any]:
        """Get crisis resources based on severity"""
        resources: Dict[str, Any] = {
            "hotline": settings.CRISIS_HOTLINE,
            "text_line": settings.CRISIS_TEXT,
            "message": "If you're having thoughts of self-harm, please reach out for help immediately."
        }
        
        if severity == "high":
            resources["message"] = "I'm very concerned about what you're sharing. Please call 988 immediately or go to the nearest emergency room. You're not alone, and help is available."
            resources["urgent"] = True
        elif severity == "medium":
            resources["message"] = "I hear that you're in a lot of pain right now. Please consider reaching out to a crisis counselor at 988 or text HOME to 741741. You deserve support."
            resources["urgent"] = False
        else:
            resources["message"] = "It sounds like you're going through a difficult time. Remember that help is available if you need it. You can call 988 or text HOME to 741741 anytime."
            resources["urgent"] = False
        
        return resources 