import openai
import anthropic
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
import json

from app.core.config import settings
from app.database import get_db, Message, Session as DBSession

class AIService:
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        
        if settings.OPENAI_API_KEY:
            try:
                self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
                print("✅ OpenAI client initialized successfully")
            except Exception as e:
                print(f"❌ Error initializing OpenAI client: {e}")
        else:
            print("⚠️  OPENAI_API_KEY not set - using fallback responses")
        
        # Initialize Anthropic client
        if settings.ANTHROPIC_API_KEY:
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
                print("✅ Anthropic client initialized successfully")
            except Exception as e:
                print(f"❌ Error initializing Anthropic client: {e}")
        else:
            print("⚠️  ANTHROPIC_API_KEY not set - using fallback responses")
    
    async def generate_response(
        self,
        message: str,
        session_type: str = "free_form",
        emotion_context: Optional[str] = None,
        topic_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> str:
        """Generate AI response based on user message and context"""
        
        # Build system prompt based on context
        system_prompt = self._build_system_prompt(
            session_type=session_type,
            emotion_context=emotion_context,
            topic_id=topic_id
        )
        
        # Get conversation history if user_id provided
        conversation_history = []
        if user_id:
            conversation_history = await self._get_conversation_history(user_id)
        
        # Prepare messages for AI
        messages = self._prepare_messages(system_prompt, conversation_history, message)
        
        try:
            if settings.AI_PROVIDER == "anthropic" and self.anthropic_client:
                return await self._generate_anthropic_response(messages)
            elif self.openai_client:
                return await self._generate_openai_response(messages)
            else:
                return self._generate_fallback_response(message)
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return self._generate_fallback_response(message)
    
    def _build_system_prompt(
        self,
        session_type: str,
        emotion_context: Optional[str] = None,
        topic_id: Optional[str] = None
    ) -> str:
        """Build system prompt based on session context"""
        
        base_prompt = """You are MindEase, a warm, thoughtful AI mental wellness companion. Your goal is to help users feel heard, understood, and supported.

Guidelines:
- Always mirror their emotions with empathy: "Sounds like you've been holding a lot today."
- Avoid direct advice. Use reflective prompts: "What do you think helped you get through that moment?"
- Keep your tone casual, sincere, and encouraging
- Be non-judgmental and supportive
- Help users explore their feelings without pushing them
- If they seem to be in crisis, acknowledge their pain and gently suggest professional help
- Keep responses conversational and not too long (2-3 sentences typically)"""

        if emotion_context:
            base_prompt += f"\n\nUser's current emotional state: {emotion_context}. Acknowledge this feeling and respond accordingly."
        
        if session_type == "topic_based" and topic_id:
            base_prompt += f"\n\nThis is a topic-based conversation. Focus on the specific topic area."
        
        return base_prompt
    
    async def _get_conversation_history(self, user_id: str) -> List[Dict[str, str]]:
        """Get recent conversation history for context"""
        db = next(get_db())
        try:
            # Get recent sessions and messages
            recent_sessions = db.query(DBSession).filter(
                DBSession.user_id == user_id
            ).order_by(DBSession.created_at.desc()).limit(3).all()
            
            history = []
            for session in recent_sessions:
                messages = db.query(Message).filter(
                    Message.session_id == session.id
                ).order_by(Message.timestamp).all()
                
                for msg in messages:
                    history.append({
                        "role": msg.role,
                        "content": msg.content
                    })
            
            return history[-10:]  # Keep last 10 messages for context
        finally:
            db.close()
    
    def _prepare_messages(
        self,
        system_prompt: str,
        conversation_history: List[Dict[str, str]],
        current_message: str
    ) -> List[Dict[str, str]]:
        """Prepare messages for AI API call"""
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": current_message
        })
        
        return messages
    
    async def _generate_openai_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate response using OpenAI API"""
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=300,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    
    async def _generate_anthropic_response(self, messages: List[Dict[str, str]]) -> str:
        """Generate response using Anthropic API"""
        # Convert messages to Anthropic format
        prompt = ""
        for msg in messages:
            if msg["role"] == "system":
                prompt += f"System: {msg['content']}\n\n"
            elif msg["role"] == "user":
                prompt += f"Human: {msg['content']}\n\n"
            elif msg["role"] == "assistant":
                prompt += f"Assistant: {msg['content']}\n\n"
        
        prompt += "Assistant:"
        
        response = self.anthropic_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=300,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text.strip()
    
    def _generate_fallback_response(self, message: str) -> str:
        """Generate a fallback response when AI services are unavailable"""
        fallback_responses = [
            "I hear you, and I want you to know that your feelings are valid. Would you like to tell me more about what's on your mind?",
            "Thank you for sharing that with me. It sounds like you're going through a challenging time. How are you feeling right now?",
            "I appreciate you opening up to me. Sometimes just talking about our feelings can help. What do you think might be helpful for you right now?",
            "I'm here to listen. Your experiences matter, and I want to understand what you're going through. Can you tell me more?",
            "It sounds like you're dealing with a lot. Remember that it's okay to feel this way. What would be most helpful for you right now?"
        ]
        
        import random
        return random.choice(fallback_responses) 