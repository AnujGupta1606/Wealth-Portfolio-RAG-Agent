#!/bin/bash

# Wealth Portfolio RAG Agent - Setup Script

echo "🚀 Setting up Wealth Portfolio RAG Agent..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if Python is installed
if command -v python3 &> /dev/null; then
    print_status "Python 3 is installed"
else
    print_error "Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if Node.js is installed
if command -v node &> /dev/null; then
    print_status "Node.js is installed"
else
    print_error "Node.js is not installed. Please install Node.js 16+ and try again."
    exit 1
fi

# Setup backend
echo -e "\n📦 Setting up Backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Created Python virtual environment"
fi

# Activate virtual environment
source venv/bin/activate
print_status "Activated virtual environment"

# Install Python dependencies
pip install -r requirements.txt
print_status "Installed Python dependencies"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    cp .env.example .env
    print_warning "Created .env file from template. Please update with your settings."
fi

cd ..

# Setup frontend
echo -e "\n🎨 Setting up Frontend..."
cd frontend

# Install Node.js dependencies
npm install
print_status "Installed Node.js dependencies"

cd ..

# Final instructions
echo -e "\n🎉 Setup complete!"
echo -e "\n📋 Next steps:"
echo -e "1. Update backend/.env with your database URLs and OpenAI API key"
echo -e "2. Start MongoDB: ${YELLOW}docker run -d -p 27017:27017 --name mongodb mongo:latest${NC}"
echo -e "3. Start MySQL: ${YELLOW}docker run -d -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=wealth_transactions mysql:8.0${NC}"
echo -e "4. Start the application:"
echo -e "   Backend: ${YELLOW}cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload${NC}"
echo -e "   Frontend: ${YELLOW}cd frontend && npm start${NC}"
echo -e "\n🌐 Access the application at: ${GREEN}http://localhost:3000${NC}"
echo -e "📚 API documentation at: ${GREEN}http://localhost:8000/docs${NC}"

echo -e "\n💡 Demo credentials:"
echo -e "   Admin: ${YELLOW}admin/admin123${NC}"
echo -e "   Manager: ${YELLOW}manager/manager123${NC}"
echo -e "   Analyst: ${YELLOW}analyst/analyst123${NC}"
