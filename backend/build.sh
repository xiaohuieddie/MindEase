#!/bin/bash
set -e

echo "🚀 Starting MindEase Backend build..."

# Upgrade pip and install build tools
echo "📦 Upgrading pip and build tools..."
pip install --upgrade pip setuptools wheel

# Install packages with specific flags to avoid compilation issues
echo "📥 Installing Python packages..."
pip install -r requirements.txt --no-cache-dir --prefer-binary

# Create database tables
echo "🗄️  Setting up database..."
python3 create_tables.py

echo "✅ Build completed successfully!" 