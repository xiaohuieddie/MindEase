# MindEase Frontend-Backend Integration Guide

## Overview
The frontend has been successfully updated to integrate with the deployed backend at `https://mindease-gigu.onrender.com`. The system supports both local development and production environments.

## ✅ Integration Status
**All API endpoints are working correctly!** The integration has been tested and verified.

## Configuration

### Environment Variables
The frontend uses environment variables to determine which backend to connect to:

- **Production (Default)**: `https://mindease-gigu.onrender.com`
- **Local Development**: `http://localhost:8000`

### Setting Up Local Development
To use the local backend during development:

1. Create a `.env.local` file in the frontend directory:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

2. Or set the environment variable when running the dev server:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000 pnpm dev
```

## Testing Instructions

### 1. Test with Deployed Backend (Production) ✅ VERIFIED

1. **Start the frontend** (uses deployed backend by default):
```bash
cd frontend
pnpm dev
```

2. **Open your browser** and navigate to `http://localhost:3000`

3. **Test the chat functionality**:
   - Go to the chat page
   - The system will automatically create an anonymous session
   - Try sending messages to test the AI responses

4. **Verify API connection** (optional):
   - Run the test script: `node test-integration.js`
   - Should show all tests passing

### 2. Test with Local Backend (Development)

1. **Start the local backend**:
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Set environment variable for local backend**:
```bash
cd frontend
NEXT_PUBLIC_API_URL=http://localhost:8000 pnpm dev
```

3. **Test the integration**:
   - Open `http://localhost:3000`
   - Navigate to the chat page
   - Send messages to test local backend responses

### 3. Full End-to-End Testing

#### Option A: Production Backend + Frontend ✅ RECOMMENDED
```bash
# Frontend will automatically use deployed backend
cd frontend
pnpm dev
# Open http://localhost:3000
```

#### Option B: Local Backend + Frontend
```bash
# Terminal 1: Start backend
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start frontend with local backend
cd frontend
NEXT_PUBLIC_API_URL=http://localhost:8000 pnpm dev
# Open http://localhost:3000
```

## 🔍 Backend Logging

The backend now includes comprehensive logging to help with debugging and monitoring:

### Log Features
- **Request/Response Logging**: All API calls are logged with timing
- **Authentication Logging**: User sessions and token creation
- **Chat Logging**: Message processing and AI responses
- **Error Logging**: Detailed error information
- **Crisis Detection**: Alerts when crisis indicators are detected

### Log Output
When running the backend locally, you'll see logs like:
```
2024-01-01 12:00:00 - main - INFO - 🚀 Starting MindEase Backend...
2024-01-01 12:00:01 - main - INFO - 📥 POST /api/v1/auth/anonymous - Client: 127.0.0.1
2024-01-01 12:00:01 - app.routers.auth - INFO - 👤 Anonymous session creation - ID: new
2024-01-01 12:00:01 - app.routers.auth - INFO - ✅ Created new anonymous user: abc123
2024-01-01 12:00:01 - app.routers.auth - INFO - 🎫 Anonymous session token created for user: abc123
2024-01-01 12:00:01 - main - INFO - 📤 POST /api/v1/auth/anonymous - Status: 200 - Time: 0.045s
```

### Log Files
- **Console Output**: Real-time logs in the terminal
- **Daily Log Files**: `logs/mindease_YYYYMMDD.log`
- **Log Levels**: INFO, DEBUG, WARNING, ERROR

### Testing Logging
To test the logging functionality:
```bash
cd backend
python test_logging.py
```

## 🔍 Frontend Logging

The frontend now includes comprehensive logging for debugging and monitoring:

### Log Features
- **Component Logging**: All major components log their activities
- **API Call Logging**: Detailed tracking of all API requests and responses
- **User Interaction Logging**: Chat messages, navigation, and user actions
- **Error Logging**: Detailed error information with context
- **Session Management**: Authentication and session creation tracking

### Log Output
When running the frontend in development, you'll see logs like:
```
ℹ️ [API] Testing connection to https://mindease-gigu.onrender.com/health
ℹ️ [API] GET /health successful
ℹ️ [Auth] Anonymous session created successfully
ℹ️ [ChatBot] Initializing chat session
ℹ️ [ChatBot] Sending user message
ℹ️ [Chat] Message sent successfully
```

### Log Viewer Component
A built-in log viewer is available in development mode:
- **Location**: Bottom-right corner of the screen
- **Features**: 
  - Real-time log display
  - Filter by log level (Debug, Info, Warn, Error)
  - Download logs as JSON
  - Clear logs
  - Collapsible data details

### Log Levels
- **Debug**: Detailed debugging information
- **Info**: General information about application flow
- **Warn**: Warning messages for potential issues
- **Error**: Error messages with detailed context

### Memory Management
- Logs are stored in memory (last 1000 entries)
- Automatic cleanup to prevent memory leaks
- Export functionality for debugging

## ✅ Features Tested and Working

### Chat Functionality
- ✅ Anonymous session creation
- ✅ Chat session initialization
- ✅ Real-time message sending
- ✅ AI response generation
- ✅ Error handling
- ✅ Loading states
- ✅ Crisis detection (if triggered)

### API Endpoints
- ✅ `/health` - Health check
- ✅ `/api/v1/auth/anonymous` - Anonymous authentication
- ✅ `/api/v1/chat/session` - Chat session creation
- ✅ `/api/v1/chat/message` - Message sending

## Test Results
```
🧪 Testing MindEase API Integration...

1. Testing basic connection...
✅ Connection successful: healthy

2. Testing anonymous session creation...
✅ Session created: Yes

3. Testing chat session creation...
✅ Chat session created: Yes

4. Testing message sending...
✅ Message sent: Yes
🤖 AI Response: I'm here to listen. Your experiences matter...

🎉 All tests completed successfully!
```

## Troubleshooting

### Common Issues

1. **CORS Errors**: The deployed backend has CORS configured for the frontend domain.

2. **Connection Timeout**: 
   - Check if the backend is running (for local testing)
   - Verify the API URL in the configuration

3. **Environment Variable Not Working**:
   - Restart the Next.js dev server after changing environment variables
   - Ensure the variable name is `NEXT_PUBLIC_API_URL`

4. **Chat Not Initializing**:
   - Check browser console for errors
   - Verify the backend endpoints are responding

5. **Package Manager Issues**:
   - This project uses `pnpm` as the package manager
   - Use `pnpm dev` instead of `npm run dev`
   - Use `pnpm install` instead of `npm install`

6. **Logging Issues**:
   - Check if the `logs/` directory exists (backend)
   - Verify file permissions for log writing
   - Check console output for real-time logs
   - Use the LogViewer component for frontend logs

### Debug Steps

1. **Check API Configuration**:
   - Open browser console
   - Check the `config` object from `@/lib/config`

2. **Test API Connection**:
   - Run: `node test-integration.js`
   - Check the test endpoint response

3. **Verify Backend Status**:
   - Visit `https://mindease-gigu.onrender.com/health` directly
   - Should return: `{"status": "healthy"}`

4. **Clear Next.js Cache** (if needed):
   ```bash
   pnpm run build
   pnpm dev
   ```

5. **Check Backend Logs** (local development):
   - Look at console output for real-time logs
   - Check `logs/mindease_YYYYMMDD.log` for detailed logs
   - Run `python test_logging.py` to test logging

6. **Check Frontend Logs** (development):
   - Open browser console for real-time logs
   - Use the LogViewer component (bottom-right corner)
   - Filter logs by level to focus on specific issues
   - Download logs for detailed analysis

## File Structure

```
frontend/
├── lib/
│   ├── api.ts          # API client functions with logging
│   ├── config.ts       # Environment configuration
│   └── logger.ts       # Frontend logging utility
├── components/
│   ├── ChatBot.tsx     # Main chat interface with logging
│   ├── ApiTest.tsx     # API connection tester
│   └── LogViewer.tsx   # Debug log viewer component
├── test-integration.js # API test script
└── .env.local          # Local environment variables (create this)

backend/
├── main.py             # FastAPI application with logging
├── logging_config.py   # Logging configuration
├── test_logging.py     # Logging test script
└── logs/               # Daily log files
    └── mindease_YYYYMMDD.log
```

## API Response Structure

### Anonymous Session
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user_id": "uuid-string",
  "anonymous_id": "anon-uuid-string"
}
```

### Chat Session
```json
{
  "session_id": "uuid-string",
  "session_type": "free_form",
  "emotion_context": "general_wellness",
  "created_at": "2024-01-01T00:00:00"
}
```

### Message Response
```json
{
  "message": "AI response text",
  "session_id": "uuid-string",
  "crisis_detected": false,
  "crisis_resources": null
}
```

## Package Manager Commands

This project uses `pnpm` as the package manager. Here are the equivalent commands:

| npm Command | pnpm Command |
|-------------|--------------|
| `npm install` | `pnpm install` |
| `npm run dev` | `pnpm dev` |
| `npm run build` | `pnpm build` |
| `npm run start` | `pnpm start` |
| `npm run lint` | `pnpm lint` |

## Next Steps

1. ✅ **Test the chat functionality** with both local and deployed backends
2. ✅ **Verify all API endpoints** are working correctly
3. **Test error scenarios** (network issues, invalid responses)
4. **Deploy the frontend** to a hosting platform if needed
5. **Add more features** like mood tracking, wellness activities, etc.
6. **Monitor logs** for debugging and performance optimization

## Notes

- The frontend automatically handles session management
- Error handling is implemented for network issues
- Loading states provide user feedback
- The system gracefully falls back to error messages on failures
- Crisis detection is built-in and will show resources if triggered
- All API calls include proper authentication headers
- This project uses `pnpm` as the package manager - use `pnpm` commands instead of `npm`
- Comprehensive logging is available for both frontend and backend debugging
- Frontend logs are stored in memory and can be viewed via the LogViewer component
- Backend logs are saved both to console and daily log files for easy access
- The LogViewer component is only available in development mode 