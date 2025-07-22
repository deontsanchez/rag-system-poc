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

# Create Python virtual environment
echo "🐍 Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "📁 Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

if [ ! -f .env ]; then
    echo "📝 Creating environment file..."
    cp .env.template .env
    echo "⚠️  Please edit backend/.env and add your OpenAI API key!"
fi

echo "📦 Installing Python dependencies in virtual environment..."
pip install --upgrade pip
pip install -r requirements.txt

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
echo "2. Start the backend: cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload"
echo "3. Start the frontend: cd frontend && npm start"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "💡 Note: Always activate the virtual environment before running backend commands:"
echo "   cd backend && source venv/bin/activate"
echo ""
echo "📚 For more information, see README.md"
