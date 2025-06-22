#!/usr/bin/env python3
"""
Database table creation script for MindEase
This script ensures all tables are created in the production database
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import Base, engine
from app.database import User, Session, Message, Topic, MoodEntry, WellnessActivity, Analytics

def create_tables():
    """Create all database tables"""
    print("🗄️  Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
        # List created tables
        print("\n📋 Created tables:")
        for table_name in Base.metadata.tables.keys():
            print(f"   - {table_name}")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    return True

def insert_sample_data():
    """Insert sample data for testing"""
    print("\n📝 Inserting sample data...")
    
    try:
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
        # Check if topics already exist
        existing_topics = db.query(Topic).count()
        if existing_topics == 0:
            # Insert sample topics
            sample_topics = [
                Topic(
                    id="topic_1",
                    title="Monday Motivation",
                    subtitle="How are you starting your week?",
                    description="Share your thoughts on starting a new week and any goals or challenges you're facing.",
                    category="workplace",
                    is_active=True
                ),
                Topic(
                    id="topic_2",
                    title="Workplace Stress",
                    subtitle="Dealing with deadline pressure",
                    description="Let's talk about managing stress and pressure in the workplace.",
                    category="workplace",
                    is_active=True
                ),
                Topic(
                    id="topic_3",
                    title="Social Connections",
                    subtitle="Feeling isolated lately?",
                    description="Discuss the importance of social connections and how to maintain them.",
                    category="social",
                    is_active=True
                ),
                Topic(
                    id="topic_4",
                    title="Self-Care Sunday",
                    subtitle="What does self-care mean to you?",
                    description="Explore different ways to practice self-care and prioritize your well-being.",
                    category="personal",
                    is_active=True
                ),
                Topic(
                    id="topic_5",
                    title="Digital Wellness",
                    subtitle="Balancing screen time and mental health",
                    description="How do you manage your relationship with technology and social media?",
                    category="personal",
                    is_active=True
                )
            ]
            
            db.add_all(sample_topics)
            db.commit()
            print("✅ Sample topics inserted successfully!")
        else:
            print("ℹ️  Topics already exist, skipping sample data insertion")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error inserting sample data: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🚀 MindEase Database Setup")
    print("=" * 40)
    
    # Check database URL
    database_url = os.getenv("DATABASE_URL", "sqlite:///./mindease.db")
    print(f"📊 Database URL: {database_url}")
    
    # Create tables
    if create_tables():
        # Insert sample data
        insert_sample_data()
        print("\n🎉 Database setup completed successfully!")
    else:
        print("\n❌ Database setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 