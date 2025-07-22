#!/bin/bash

# RAG System POC Setup Script

echo "🚀 Setting up RAG System POC..."

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm is required but not installed."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup backend
echo "🔧 Setting up backend..."
cd backend

if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp .env.template .env
    echo "⚠️  Please edit backend/.env and add your OpenAI API key!"
fi

echo "📦 Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    pip install -r requirements.txt
fi

# Create necessary directories
mkdir -p chroma_db
mkdir -p ../data/uploads

cd ..

# Setup frontend
echo "🎨 Setting up frontend..."
cd frontend

echo "📦 Installing Node.js dependencies..."
npm install

cd ..

echo "✅ Setup complete!"
echo ""
echo "📖 Next steps:"
echo "1. Edit backend/.env and add your OpenAI API key"
echo "2. Start the backend: cd backend && python -m uvicorn app.main:app --reload"
echo "3. Start the frontend: cd frontend && npm start"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "📚 For more information, see README.md"
