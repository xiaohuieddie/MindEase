# MindEase Backend API

A FastAPI-based backend service for the MindEase AI Mental Wellness Companion application.

## Features

- **AI Chat Integration**: Support for OpenAI GPT-4 and Anthropic Claude
- **Anonymous User Support**: Users can start conversations without registration
- **Crisis Detection**: Automatic detection of crisis indicators with appropriate resources
- **Mood Tracking**: Track emotional states and intensity over time
- **Wellness Activities**: Breathing exercises, affirmations, and stress reframing
- **Daily Topics**: Curated conversation starters for different categories
- **Analytics**: User insights and progress tracking
- **JWT Authentication**: Secure user authentication and session management

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (production) / SQLite (development)
- **ORM**: SQLAlchemy
- **Authentication**: JWT with Python-Jose
- **AI Services**: OpenAI GPT-4, Anthropic Claude
- **Deployment**: Render

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/anonymous` - Create anonymous session
- `GET /api/v1/auth/me` - Get current user info

### Chat
- `POST /api/v1/chat/session` - Create new chat session
- `POST /api/v1/chat/message` - Send message and get AI response
- `GET /api/v1/chat/session/{session_id}/messages` - Get session messages
- `POST /api/v1/chat/session/{session_id}/end` - End chat session

### Wellness
- `POST /api/v1/wellness/mood` - Create mood entry
- `GET /api/v1/wellness/mood` - Get mood entries
- `POST /api/v1/wellness/activity` - Create wellness activity
- `POST /api/v1/wellness/activity/{activity_id}/complete` - Complete activity
- `GET /api/v1/wellness/activity` - Get wellness activities
- `GET /api/v1/wellness/stats` - Get wellness statistics

### Topics
- `GET /api/v1/topics/daily` - Get daily topics
- `GET /api/v1/topics/daily/random` - Get random daily topic
- `GET /api/v1/topics/categories` - Get topic categories
- `GET /api/v1/topics/{topic_id}` - Get specific topic

### Analytics
- `GET /api/v1/analytics/insights` - Get user insights
- `GET /api/v1/analytics/mood/trend` - Get mood trends
- `GET /api/v1/analytics/sessions/activity` - Get session activity
- `GET /api/v1/analytics/wellness/progress` - Get wellness progress
- `GET /api/v1/analytics/emotions/summary` - Get emotion summary
- `POST /api/v1/analytics/track` - Track analytics event

## Setup

### Local Development

1. **Clone the repository**
   ```bash
   cd backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | Database connection string | Yes |
| `SECRET_KEY` | JWT secret key | Yes |
| `OPENAI_API_KEY` | OpenAI API key | No (if using Anthropic) |
| `ANTHROPIC_API_KEY` | Anthropic API key | No (if using OpenAI) |
| `AI_PROVIDER` | AI provider preference | No (default: openai) |
| `DEBUG` | Debug mode | No (default: True) |

## Database Schema

### Users
- Anonymous and registered users
- JWT authentication
- Session management

### Sessions
- Chat session tracking
- Session types (free_form, topic_based, emotion_based)
- Start/end timestamps

### Messages
- Chat message storage
- Crisis detection flags
- User/assistant role tracking

### Mood Entries
- Emotional state tracking
- Intensity scale (1-10)
- Optional notes

### Wellness Activities
- Activity types (breathing, affirmations, reframing)
- Completion tracking
- Feedback ratings

### Topics
- Daily conversation starters
- Category organization
- Active/inactive status

## Deployment

### Render Deployment

1. **Connect your repository to Render**
2. **Create a new Web Service**
3. **Configure environment variables**
4. **Deploy automatically on push**

The `render.yaml` file provides the configuration for automatic deployment.

### Environment Variables for Production

Set these in your Render dashboard:

- `DATABASE_URL`: PostgreSQL connection string (auto-generated)
- `SECRET_KEY`: Secure random string
- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key (optional)
- `AI_PROVIDER`: openai or anthropic
- `DEBUG`: false

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt password hashing
- **CORS Configuration**: Configurable CORS settings
- **Crisis Detection**: Automatic detection and escalation
- **Input Validation**: Pydantic model validation
- **Rate Limiting**: Built-in FastAPI rate limiting

## Crisis Detection

The system automatically detects crisis indicators in user messages and provides appropriate resources:

- **Keywords Detection**: Suicide, self-harm, etc.
- **Pattern Matching**: Regular expression patterns
- **Severity Assessment**: High, medium, low risk levels
- **Resource Provision**: Crisis hotlines and text lines
- **Escalation**: Appropriate messaging based on severity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License. 