#!/bin/bash

# Production startup script for Render deployment
echo "🚀 Starting Wealth Portfolio RAG Agent Backend..."

# Install dependencies if not cached
if [ ! -d "venv" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

# Create necessary directories
mkdir -p chroma_db
mkdir -p logs

# Run database migrations/setup if needed
echo "🗄️ Setting up databases..."
python setup_mysql.py || echo "⚠️ MySQL setup skipped"

# Insert sample data if databases are empty
echo "📊 Checking sample data..."
python insert_sample_data.py || echo "⚠️ Sample data insertion skipped"

# Start the application
echo "✅ Starting FastAPI server..."
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
