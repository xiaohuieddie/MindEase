#!/usr/bin/env python3
"""
Test script to demonstrate MindEase backend logging functionality
"""

import requests
import json
import time

# Test the deployed backend
API_BASE_URL = "https://mindease-gigu.onrender.com"

def test_backend_logging():
    """Test various endpoints to see logging in action"""
    
    print("🧪 Testing MindEase Backend Logging...")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health check endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.json()}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Anonymous session creation
    print("\n2. Testing anonymous session creation...")
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/auth/anonymous",
            headers={"Content-Type": "application/json"},
            json={}
        )
        print(f"✅ Status: {response.status_code}")
        data = response.json()
        print(f"🎫 Token created: {data.get('access_token', 'None')[:20]}...")
        token = data.get('access_token')
    except Exception as e:
        print(f"❌ Error: {e}")
        token = None
    
    if token:
        # Test 3: Chat session creation
        print("\n3. Testing chat session creation...")
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/v1/chat/session",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                },
                json={
                    "session_type": "free_form",
                    "emotion_context": "test_logging"
                }
            )
            print(f"✅ Status: {response.status_code}")
            data = response.json()
            print(f"💬 Session created: {data.get('session_id', 'None')}")
            session_id = data.get('session_id')
        except Exception as e:
            print(f"❌ Error: {e}")
            session_id = None
        
        if session_id:
            # Test 4: Send a test message
            print("\n4. Testing message sending...")
            try:
                response = requests.post(
                    f"{API_BASE_URL}/api/v1/chat/message",
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {token}"
                    },
                    json={
                        "content": "Hello! This is a test message to check logging functionality.",
                        "session_id": session_id,
                        "session_type": "free_form"
                    }
                )
                print(f"✅ Status: {response.status_code}")
                data = response.json()
                print(f"🤖 AI Response: {data.get('message', 'None')[:100]}...")
                if data.get('crisis_detected'):
                    print("🚨 Crisis detected!")
            except Exception as e:
                print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Logging test completed!")
    print("\n📝 To see the actual logs when running locally:")
    print("1. Start the backend: python -m uvicorn main:app --reload")
    print("2. Check the console output for real-time logs")
    print("3. Check the logs/ directory for daily log files")

if __name__ == "__main__":
    test_backend_logging() 