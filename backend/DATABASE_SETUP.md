# MindEase Database Setup Guide

## Overview
This guide will help you set up the PostgreSQL database for MindEase on Render.

## Option 1: Automatic Setup (Recommended)

### Step 1: Push Your Code
Make sure your latest code is pushed to GitHub:
```bash
git add .
git commit -m "Add database setup scripts"
git push origin main
```

### Step 2: Deploy on Render
1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Connect your GitHub repository
3. Render will automatically:
   - Create the PostgreSQL database
   - Set up the connection string
   - Run the build script (which includes `create_tables.py`)

## Option 2: Manual Database Setup

### Step 1: Create PostgreSQL Database
1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `mindease-db`
   - **Database**: `mindease`
   - **User**: `mindease_user`
   - **Plan**: Free
4. Click **"Create Database"**

### Step 2: Get Connection String
1. Click on your database
2. Go to **"Connections"** tab
3. Copy the **"External Database URL"**

### Step 3: Update Web Service
1. Go to your `mindease-backend` service
2. Click **"Environment"** tab
3. Add environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the connection string

### Step 4: Redeploy
1. Go to your web service
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

## Database Schema

The following tables will be created:

### Core Tables
- **users**: User accounts (anonymous and registered)
- **sessions**: Chat sessions
- **messages**: Chat messages
- **topics**: Daily conversation topics
- **mood_entries**: User mood tracking
- **wellness_activities**: Wellness activities
- **analytics**: User analytics data

### Sample Data
The setup script will automatically insert:
- 5 sample topics (workplace, social, personal categories)
- Ready for immediate testing

## Testing Database Connection

### Local Testing
```bash
cd backend
python3 create_tables.py
```

### Production Testing
After deployment, test the wellness progress endpoint:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://mindease-gigu.onrender.com/api/v1/analytics/wellness/progress
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Check if `DATABASE_URL` is set correctly
   - Verify the database is created and running
   - Check Render logs for connection errors

2. **Table Creation Failed**
   - Ensure `create_tables.py` is included in the build
   - Check if the database user has proper permissions
   - Review Render build logs

3. **500 Error on Wellness Progress**
   - This usually means database tables aren't created
   - Run the database setup script
   - Check if all tables exist

### Checking Database Status

1. **View Render Logs**
   - Go to your web service
   - Click **"Logs"** tab
   - Look for database-related errors

2. **Test Database Connection**
   ```bash
   # Test health endpoint
   curl https://mindease-gigu.onrender.com/health
   
   # Test authenticated endpoints
   curl -H "Authorization: Bearer YOUR_TOKEN" \
     https://mindease-gigu.onrender.com/api/v1/topics/daily
   ```

## Environment Variables

Make sure these are set in Render:

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `SECRET_KEY` | JWT secret key | Yes |
| `OPENAI_API_KEY` | OpenAI API key | No |
| `ANTHROPIC_API_KEY` | Anthropic API key | No |
| `AI_PROVIDER` | AI provider preference | No |
| `DEBUG` | Debug mode | No |

## Next Steps

After database setup:
1. ✅ Test all API endpoints
2. ✅ Deploy frontend
3. ✅ Configure AI API keys
4. ✅ Set up monitoring
5. ✅ Test end-to-end functionality

## Support

If you encounter issues:
1. Check Render documentation
2. Review application logs
3. Test database connection locally
4. Verify environment variables 