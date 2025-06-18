#!/usr/bin/env python3
"""
Simple test script for MindEase API endpoints
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_root_endpoint():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_anonymous_auth():
    """Test anonymous authentication"""
    print("Testing anonymous authentication...")
    response = requests.post(f"{BASE_URL}/api/v1/auth/anonymous", json={})
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Anonymous ID: {data.get('anonymous_id')}")
        print(f"Token: {data.get('access_token')[:20]}...")
    else:
        print(f"Error: {response.text}")
    print()

def test_daily_topics():
    """Test daily topics endpoint"""
    print("Testing daily topics...")
    response = requests.get(f"{BASE_URL}/api/v1/topics/daily")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        topics = response.json()
        print(f"Found {len(topics)} topics:")
        for topic in topics[:3]:  # Show first 3
            print(f"  - {topic['title']}: {topic['subtitle']}")
    else:
        print(f"Error: {response.text}")
    print()

def test_topic_categories():
    """Test topic categories endpoint"""
    print("Testing topic categories...")
    response = requests.get(f"{BASE_URL}/api/v1/topics/categories")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Categories: {data.get('categories')}")
    else:
        print(f"Error: {response.text}")
    print()

def main():
    """Run all tests"""
    print("MindEase API Test Suite")
    print("=" * 50)
    
    try:
        test_health_check()
        test_root_endpoint()
        test_anonymous_auth()
        test_daily_topics()
        test_topic_categories()
        
        print("All tests completed!")
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8000")
        print("Run: python start.py or uvicorn main:app --reload")
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    main() 