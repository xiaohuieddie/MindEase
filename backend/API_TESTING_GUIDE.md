# MindEase API Testing Guide

## API Base URL
```
https://mindease-gigu.onrender.com
```

## Quick Test Commands

### 1. Health Check
```bash
curl https://mindease-gigu.onrender.com/health
```

### 2. Root Endpoint
```bash
curl https://mindease-gigu.onrender.com/
```

### 3. Get Authentication Token
```bash
curl -X POST https://mindease-gigu.onrender.com/api/v1/auth/anonymous \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 4. Test Authenticated Endpoints

First, get a token and save it:
```bash
TOKEN=$(curl -s -X POST https://mindease-gigu.onrender.com/api/v1/auth/anonymous \
  -H "Content-Type: application/json" \
  -d '{}' | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
echo "Token: $TOKEN"
```

Then test authenticated endpoints:

#### Daily Topics
```bash
curl -H "Authorization: Bearer $TOKEN" \
  https://mindease-gigu.onrender.com/api/v1/topics/daily
```

#### Topic Categories
```bash
curl -H "Authorization: Bearer $TOKEN" \
  https://mindease-gigu.onrender.com/api/v1/topics/categories
```

#### Wellness Activities
```bash
curl -H "Authorization: Bearer $TOKEN" \
  https://mindease-gigu.onrender.com/api/v1/wellness/activity
```

#### Analytics Insights
```bash
curl -H "Authorization: Bearer $TOKEN" \
  https://mindease-gigu.onrender.com/api/v1/analytics/insights
```

#### Create Chat Session
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"session_type": "free_form"}' \
  https://mindease-gigu.onrender.com/api/v1/chat/session
```

#### Send Chat Message
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your_session_id", "message": "Hello, how are you?"}' \
  https://mindease-gigu.onrender.com/api/v1/chat/message
```

#### Create Mood Entry
```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mood": "happy", "intensity": 8, "notes": "Feeling great today!"}' \
  https://mindease-gigu.onrender.com/api/v1/wellness/mood
```

## Interactive API Documentation

Visit the Swagger UI for interactive testing:
```
https://mindease-gigu.onrender.com/docs
```

## Test Results Summary

✅ **Working Endpoints:**
- Health Check
- Root Endpoint
- Anonymous Authentication
- Daily Topics
- Topic Categories
- Wellness Activities
- Analytics Insights
- Mood Entries
- Wellness Statistics
- Mood Trends
- Session Activity
- Emotion Summary
- Create Chat Session

⚠️ **Endpoints with Issues:**
- Wellness Progress (500 error) - may need database setup

## Frontend Integration

To connect your frontend to the deployed API:

1. Update your frontend API base URL to: `https://mindease-gigu.onrender.com`
2. Ensure CORS is properly configured
3. Test authentication flow
4. Test all major features

## Monitoring

- Check Render dashboard for logs and performance
- Monitor API response times
- Watch for any 500 errors
- Test with real user scenarios

## Common Issues

1. **403 Forbidden**: Missing or invalid authentication token
2. **500 Internal Server Error**: Server-side issue, check logs
3. **CORS Issues**: Frontend domain not in allowed origins
4. **Token Expiry**: JWT tokens expire after 30 minutes

## Next Steps

1. Deploy frontend to production
2. Set up proper environment variables
3. Configure AI API keys
4. Set up monitoring and logging
5. Test end-to-end user flows 